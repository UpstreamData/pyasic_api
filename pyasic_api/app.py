from fastapi import FastAPI
from pyasic_api import get, post

desc = """
Pyasic API is a REST API implementation of the functions exposed by
[`pyasic`](https://github.com/UpstreamData/pyasic), designed to make
interacting with miners easier and more standard by moving all miner
data through a central hub and cleaning it into a consistent format.

## GET
Items in the **GET** category are readable data, which mostly will
be handled by `get_data` in pyasic.

## POST
Items in the **POST** category are either writable commands on the miner,
or are more advanced data functions, such as selecting specific data
from `get_data` or selecting data from groups of miners at a time.
"""

app = FastAPI(title="pyasic-API", description=desc)
app.include_router(get.router)
app.include_router(post.router)
