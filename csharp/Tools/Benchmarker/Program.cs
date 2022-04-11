using System;
using Systemathics.Apis.Helpers;
using Systemathics.Apis.Type.Shared.V1;
using Google.Protobuf.WellKnownTypes;
using Google.Type;
using Grpc.Net.Client;
using Grpc.Core;

using TickTradesAndBookService = Systemathics.Apis.Services.Tick.V1.TickTradesAndBookService;
using TickTradesAndBookRequest = Systemathics.Apis.Services.Tick.V1.TickTradesAndBookRequest;
using TickTradesAndBookResponse = Systemathics.Apis.Services.Tick.V1.TickTradesAndBookResponse;
using Trade = Systemathics.Apis.Type.Shared.V1.Trade;
using Book = Systemathics.Apis.Type.Shared.V1.Book;
using BookUpdates = Systemathics.Apis.Type.Shared.V1.BookUpdates;

using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace Benchmarker
{

    class Program
    {
        public static async Task<int> Main(string[] args)
        {
            using FileStream stream = File.OpenRead("Tasks.json");
            var planning = JsonSerializer.Deserialize<Planning>(stream);

            if (planning is null)
            {
                Console.WriteLine("Error with the benchmark planning !");
                return -1;
            }

            // Get token as metadata
            var headers = new Grpc.Core.Metadata();
            try { headers = TokenHelpers.GetTokenAsMetaData(); } catch { }

            // Create communication channel
            var channel = ChannelHelpers.GetChannel();

            Console.WriteLine(planning.Tasks.Length);

            for (int i = 0; i < planning.Identifiers.Length; i++)
            {
                JSON_Identifier[] ids = planning.Identifiers.Take(i + 1).ToArray(); // Represents the array of the indexes which we want data
                for (int taskID = 0; taskID < planning.Tasks.Length; taskID++)
                {
                    var currentTask = planning.Tasks[taskID];
                    for (int constraintID = 0; constraintID < currentTask.Constraints.Length; constraintID++)
                    {
                        string currentConstraintName = currentTask.Constraints[constraintID];
                        var constraint = new Constraints();
                        var currentConstraints = planning.Constraints.Where(c => c.Name == currentConstraintName).ToArray();
                        if (currentConstraints.Length == 1) // If only one JSON constraint exists with the name of the current constraint
                        {
                            var c = currentConstraints[0];

                            var dateIntervals = new DateInterval();
                            if (c.Date.StartDate is not null && c.Date.EndDate is not null)
                            {
                                var start = c.Date.StartDate;
                                var end = c.Date.EndDate;
                                dateIntervals.StartDate = new Date { Year = start.Year, Month = start.Month, Day = start.Day };
                                dateIntervals.EndDate = new Date { Year = end.Year, Month = end.Month, Day = end.Day };
                            }
                            else
                            {
                                Console.WriteLine($"One of the dates in \"{currentConstraintName}\" is not defined, please review the planning !");
                                return -1;
                            }

                            var timeInterval = new TimeInterval();
                            if (c.Time.StartTime is not null && c.Time.EndTime is not null)
                            {
                                var start = c.Time.StartTime;
                                var end = c.Time.EndTime;
                                timeInterval.StartTime = new TimeOfDay { Hours = start.Hours, Minutes = start.Minutes, Seconds = start.Seconds };
                                timeInterval.EndTime = new TimeOfDay { Hours = end.Hours, Minutes = end.Minutes, Seconds = end.Seconds };
                            }
                            else
                            {
                                Console.WriteLine($"One of the times in \"{currentConstraintName}\" is not defined, please review the planning !");
                                return -1;
                            }

                            constraint.DateIntervals.Add(dateIntervals);
                            constraint.TimeIntervals.Add(timeInterval);


                            // A faire 3 fois pour avoir no-cache, cache1, cache2

                            // Process Task for an array of id and a specific type of constraint
                            var data = await Process(headers, channel, constraint, ids, currentTask);
                            Console.WriteLine($"({i}, {taskID}, {constraintID}, no-cache)\"{currentTask.Name}\" made {data.Item3} requests and took {data.Item2.Milliseconds} ms ({data.Item2.Ticks} ticks)");

                            //var data2 = await Process(headers, channel, constraint, ids, currentTask);
                            //Console.WriteLine($"({i}, {taskID}, {constraintID}, cache-1)\"{currentTask.Name}\" made {data2.Item3} requests and took {data2.Item2.Milliseconds} ms ({data2.Item2.Ticks} ticks)");

                            //var data3 = await Process(headers, channel, constraint, ids, currentTask);
                            //Console.WriteLine($"({i}, {taskID}, {constraintID}, cache-2)\"{currentTask.Name}\" made {data3.Item3} requests and took {data3.Item2.Milliseconds} ms ({data3.Item2.Ticks} ticks)");
                        }
                        else
                        {
                            Console.WriteLine("There are multiple constraints woth the same name, please review the planning !");
                            return -1;
                        }
                    }
                }
            }
            return 0;
        }

        public static async Task<(List<long>, TimeSpan, long)> Process(Grpc.Core.Metadata headers, GrpcChannel channel, Constraints constraints, JSON_Identifier[] json_ids, JSON_Task task)
        {
            var stamps = new List<long>();
            Stopwatch chrono = new Stopwatch();
            long requests = 0;
            switch (task.API)
            {
                case "TickTradesAndBook":
                    // Generate the tick trades and book request
                    var request = new TickTradesAndBookRequest
                    {
                        Constraints = constraints,
                        MaxDepth = task.Options.MaxDepth,
                        BookUpdates = (BookUpdates)task.Options.BookUpdates,
                        Adjustment = task.Options.Adjustements
                    };
                    var identifiers = json_ids.Select(id => new IdentifierAndLevel { Exchange = id.Exchange, Ticker = id.Ticker, Level = (Level)task.Options.Level });
                    request.Identifiers.Add(identifiers);

                    // Instantiate the tick trades and book service
                    var service = new TickTradesAndBookService.TickTradesAndBookServiceClient(channel);

                    // Get the trades and the book limits
                    var trades = new List<Tuple<Timestamp, Trade>>();
                    var books = new List<Tuple<Timestamp, Book>>();

                    var call = service.TickTradesAndBook(request, headers);

                    chrono.Start();
                    await foreach (var current in call.ResponseStream.ReadAllAsync())
                    {
                        if (current.Mapping != null)
                        {
                            // Skip the mapping data
                            continue;
                        }

                        // Get the time stamp for the current data
                        var ts = current.Data.TimeStamp;

                        // Trade
                        if (current.Data.Trade != null)
                        {
                            trades.Add(new Tuple<Timestamp, Trade>(ts, current.Data.Trade));
                            requests++;
                            stamps.Add(chrono.ElapsedTicks);
                        }

                        // Book
                        if (current.Data.Book != null)
                        {
                            books.Add(new Tuple<Timestamp, Book>(ts, current.Data.Book));
                            requests++;
                            stamps.Add(chrono.ElapsedTicks);
                        }


                    }
                    chrono.Stop();
                    break;
            }

            return (stamps, chrono.Elapsed, requests);
        }
    }
}