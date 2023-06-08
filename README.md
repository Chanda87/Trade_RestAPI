# Trade_RestAPI
A restAPI for trade details has been created using FastAPI in Python.
some neccessary modules have been imported fastAPI,pydantic,datetime,typing [refer to code for their detail].
A variable named app is used to create the instance of fastAPI.
This code contains two pydantic model 'TradeDetails' and 'Trade' where 'TradeDetails' contais information about buysellIndicator, price and quantity . 'Trade' contains detail about asset class,counterparty,instrument_id,instrument_name,trade_date_time,trade_details, trade_id and trader.
An empty list of variable name 'trade_database' is created to store is data temporarily and in the absence of database.
@app.post is used for creating the trade of route '/trades/' A function is created using def function of name create_trade which will return the data of 'trade'.append() is used to store the data of trade in the created list of name - 'trade_database'. The trade will be created with a return message -A new  trade is  successfully created.
An endpoint is created to retreive the trade information on '/trades/' route. This also allows to retrieve list of trades, filter, sort and paginate.
@app.get("/trades/") is endpoint to to fetch a list of trades based on various query parameters.
filtered_trades is an empty list to store the filtered trades based on the query parameters.
if search: checks whether the search parameter has non-null value. search.lower() is used to convert the parameter to lowercase which will allow case sensitive searching. If the search value is found in the fields , it will be stored in the filtered_trades.
In next line , it filters the trades based on additional criteria specified by the query parameters.Iteratition is performed  over each trade in the filtered_trades list and a set of conditions are applied to filter the trades based on the query parameters.
The logical operator 'and' is used to combine the different conditions.Each condition checks if any specific query parameter is None or matches an attribute of the trade.  Trades that matches the criteria are updated in the filtered_trades list.
Next block of codes perform the sorting function using sort and order parameters.
sort() method is used to set a lambda function that retrieves the specified attribute for each trade. The getattr() function retrieves the  value dynamically from each trade object based on the sort parameter value. 
if order == 'desc': this checks whether the 'order' query parameter is set to desc, if the condition is true , filered_trades are reversed by using the reverse().
The next set of codes performs pagination by dividing the list of trades into pages based on the page and size query parameters. It calculates the starting and ending indices for the trades to be included on the current page and returns a response containing the total number of trades and the trades for the current page.
The function then returns two keys - "total_trades": The total number of trades in the filtered_trades list and "trades": The sublist of trades (paged_trades) representing the current page.
In the last set of code an endpoint is created to fetch a single trade by its id using trade_id.get_trade function is created to get the value . If the trade is present it will return the value else it will return a message - "Trade not found".
All the above code is run in pycharm using "uvicorn main:app --reload" in the terminal.

