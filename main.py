# import FastAPI will help to create the API  and query function is used to declare the query parameters
from fastapi import FastAPI, Query
# list is a class of typing module that represent the data type list
from typing import List
# datetime is imported for using date and time
from datetime import datetime
# pydantic is used for data validation and it reduces the chances of error
from pydantic import BaseModel, Field
# instance of FastAPI is created where app is a variable name
app = FastAPI()
# First Pydantic model
class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")
    price: float = Field(description="The price of the Trade.")
    quantity: int = Field(description="The amount of units traded.")
# Second pydantic model
class Trade(BaseModel):
    asset_class: str = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")
    counterparty: str = Field(default=None, description="The counterparty the trade was executed with. May not always be available")
    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")
    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")
    trade_date_time: datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")
    trade_details: TradeDetails = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")
    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")
    trader: str = Field(description="The name of the Trader")
# An empty list is created to store the data temporary
trade_database = []
# create trade
@app.post("/trades/")
def create_trade(trade: Trade):
    trade_database.append(trade)
    return {"message": "A new trade is successfully created."}
# endpoint for the HTTP get method on "/trades/" route. This also allows to retrieve list of trades, filter, sort and paginate
@app.get("/trades/")
def get_trades(
    search: str = Query(None),
    assetClass: str = Query(None),
    end: datetime = Query(None),
    maxPrice: float = Query(None),
    minPrice: float = Query(None),
    start: datetime = Query(None),
    tradeType: str = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    sort: str = Query(None, regex=r"^(trade_date_time|instrument_id|instrument_name|trader)$"),
    order: str = Query("asc", regex=r"^(asc|desc)$")
):
    filtered_trades = []

    # This for to perform search function using search query parameter
    if search:
        search = search.lower()
        for trade in trade_database:
            if (
                search in trade.counterparty.lower() or
                search in trade.instrument_id.lower() or
                search in trade.instrument_name.lower() or
                search in trade.trader.lower()
            ):
                filtered_trades.append(trade)
    else:
        filtered_trades = trade_database

    # filtering the trade
    filtered_trades = [
        trade for trade in filtered_trades
        if (assetClass is None or trade.asset_class == assetClass) and
           (end is None or trade.trade_date_time <= end) and
           (maxPrice is None or trade.trade_details.price <= maxPrice) and
           (minPrice is None or trade.trade_details.price >= minPrice) and
           (start is None or trade.trade_date_time >= start) and
           (tradeType is None or trade.trade_details.buySellIndicator == tradeType)
    ]

    # trade sorting
    if sort:
        filtered_trades.sort(key=lambda trade: getattr(trade, sort))
        if order == 'desc':
            filtered_trades.reverse()

    # pagination
    total_trades = len(filtered_trades)
    start_index = (page - 1) * size
    end_index = start_index + size
    paged_trades = filtered_trades[start_index:end_index]

    return {
        "total_trades": total_trades,
        "trades": paged_trades
    }
# Endpoint to get the trade and if not found a message will be displayed
@app.get("/trades/{trade_id}")
def get_trade(trade_id: str):
    for trade in trade_database:
        if trade.trade_id == trade_id:
            return trade
    return {"message": "Trade not found"}
