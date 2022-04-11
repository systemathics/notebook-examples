namespace Benchmarker
{
    public class Planning
    {
        public JSON_Identifier[] Identifiers { get; set; }
        public JSON_Constraint[] Constraints { get; set; }
        public JSON_Task[] Tasks { get; set; }
    }

    public class JSON_Identifier
    {
        public string Ticker { get; set; }
        public string Exchange { get; set; }
    }

    public class JSON_Constraint
    {
        public string Name { get; set; }
        public Dates Date { get; set; }
        public Time Time { get; set; }
    }

    public class Dates
    {
        public Startdate StartDate { get; set; }
        public Enddate EndDate { get; set; }
    }

    public class Startdate
    {
        public int Year { get; set; }
        public int Month { get; set; }
        public int Day { get; set; }
    }

    public class Enddate
    {
        public int Year { get; set; }
        public int Month { get; set; }
        public int Day { get; set; }
    }

    public class Time
    {
        public Starttime StartTime { get; set; }
        public Endtime EndTime { get; set; }
    }

    public class Starttime
    {
        public int Hours { get; set; }
        public int Minutes { get; set; }
        public int Seconds { get; set; }
    }

    public class Endtime
    {
        public int Hours { get; set; }
        public int Minutes { get; set; }
        public int Seconds { get; set; }
    }

    public class JSON_Task
    {
        public string Name { get; set; }
        public string API { get; set; }
        public string[] Constraints { get; set; }
        public Options Options { get; set; }
    }

    public class Options
    {
        public int MaxDepth { get; set; }
        public int BookUpdates { get; set; }
        public bool Adjustements { get; set; }
        public int Level { get; set; }
    }

}
