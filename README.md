# Ganymede | on-demand financial data

# About Ganymede

Built as cloud native, Ganymede is a fully managed platform, continuously updated with high-quality, curated,
and cross validated data. Ganymede is purpose built for the financial data markets ever increasing data volumes,
allowing clients to query against large data sets, including tick-by-tick, sampled, daily, corporate actions,
ESG and reference data. Packed with a broad range of analytics, the solution is optimized for fast response times,
supports full order book natively and allows fine grained/customizable trade and quote conditions mapping and filtering.

# About this repository 

This repository contains Jupyter notebooks to request analytics and retrieve bespoke datasets by calling Ganymede gRPC API. Samples and building blocks are available to help you designing your bespoke analytics and data requests:

- Reference data
- Corporate actions
- Historical financial data and calculations: daily, intraday and tick data
- Best execution
- Future roll strategies and trading strategies
- Monitoring dashboards including data storage and normalization metrics

Example are organized in a per language per topic way:
- [Python](/python/)
- [C#](/csharp/)
- [F#](/fsharp/)

There also are a few helpers to plug common development environments to Ganymede:
- Have a look [here](/remoteaccess/)

## Current Ganymede API version

[![PyPI version](https://badge.fury.io/py/systemathics.apis.svg)](https://badge.fury.io/py/systemathics.apis) [![NuGet version](https://badge.fury.io/nu/systemathics.apis.svg)](https://badge.fury.io/nu/systemathics.apis)

## Useful links

- [Ganymede](https://dev.systemathics.eu/) portal (registered users logon page is [here](https://dev.systemathics.eu/data/))
- Have a look at the [documentation](https://dev.systemathics.eu/api-documentation.html) (API reference and tutorials)

## About us

[Systemathics](https://systemathics.com) is a French fintech founded in 2008 developing its innovative products with the highest quality standards 100% in France.
Our main mission is to provide global investors with a complete end-to-end solution to systematize alpha generation in a robust way.
From data pre and post trade analysis, back-testing, risk assessment and signal generation to day-to-day execution in production and everything in between.
