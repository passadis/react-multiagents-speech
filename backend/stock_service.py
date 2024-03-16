import requests

def fetch_stock_quote(api_key, symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        data = response.json()

        quote = data.get("Global Quote", {})
        if not quote:
            return "Stock information not available."

        # Parsing relevant information
        stock_symbol = quote.get("01. symbol", "N/A")
        open_price = quote.get("02. open", "N/A")
        high_price = quote.get("03. high", "N/A")
        low_price = quote.get("04. low", "N/A")
        current_price = quote.get("05. price", "N/A")
        volume = quote.get("06. volume", "N/A")
        latest_trading_day = quote.get("07. latest trading day", "N/A")
        previous_close = quote.get("08. previous close", "N/A")
        change = quote.get("09. change", "N/A")
        change_percent = quote.get("10. change percent", "N/A")

        # Constructing descriptive text
        descriptive_text = (
            f"Here is the latest stock information for {stock_symbol}. "
            f"On the latest trading day, {latest_trading_day}, "
            f"the stock opened at {open_price}, "
            f"with a high of {high_price} and a low of {low_price}. "
            f"The closing price was {current_price}. "
            f"The stock saw a change of {change}, which is {change_percent}. "
            f"The volume of shares traded was {volume}."
        )
        return descriptive_text
    except requests.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return "Error fetching stock information."
