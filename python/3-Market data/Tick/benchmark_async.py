#!/usr/bin/python

# pip install googleapis-common-protos protobuf grpcio pandas

import grpc
import asyncio
from datetime import datetime
import google.type.date_pb2 as date
import google.type.timeofday_pb2 as timeofday
import systemathics.apis.type.shared.v1.identifier_pb2 as identifier
import systemathics.apis.type.shared.v1.constraints_pb2 as constraints
import systemathics.apis.type.shared.v1.date_interval_pb2 as dateinterval
import systemathics.apis.type.shared.v1.time_interval_pb2 as timeinterval
import systemathics.apis.services.tick.v1.tick_trades_and_book_pb2 as tick_trades_and_book
import systemathics.apis.services.tick.v1.tick_trades_and_book_pb2_grpc as tick_trades_and_book_service
import systemathics.apis.helpers.token_helpers as token_helpers
import systemathics.apis.helpers.channel_helpers as channel_helpers

token = token_helpers.get_token()
print(token)

my_identifier = identifier.Identifier(exchange = 'XNGS', ticker = 'INTC')

my_date_interval = dateinterval.DateInterval(
    start_date = date.Date(year = 2022, month = 1, day = 14), 
    end_date = date.Date(year = 2022, month = 1, day = 14)
)

my_time_interval = timeinterval.TimeInterval(
    start_time = timeofday.TimeOfDay(hours = 15, minutes = 0, seconds = 0), 
    end_time = timeofday.TimeOfDay(hours = 15, minutes = 5, seconds = 0)
)

my_constraints = constraints.Constraints(
    date_intervals = [my_date_interval],
    time_intervals = [my_time_interval]
)

request = tick_trades_and_book.TickTradesAndBookRequest(
    identifiers = [my_identifier],
    constraints = my_constraints
)

def get_grpc_aio_channel() -> grpc.aio.Channel:
    credentials = channel_helpers.get_channel_credentials()
    return grpc.aio.secure_channel(channel_helpers.get_grpc_api_endpoint(), credentials)

# async
async def run() -> int:
    async with get_grpc_aio_channel() as channel:
        stub = tick_trades_and_book_service.TickTradesAndBookServiceStub(channel)
        stream = stub.TickTradesAndBook(request = request, metadata = [('authorization', token)])
        i = 0

        #async for item in stream:
        #    i += 1
        #
        async for item in stream.__aiter__():
            i += 1

        return i

loop = asyncio.get_event_loop()
n = loop.run_until_complete(run())
loop.close()
print(n)