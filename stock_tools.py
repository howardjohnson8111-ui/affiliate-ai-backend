# Stock Market Tools for Stock Analyst Persona
# This file contains tool definitions and handlers for stock market queries

STOCK_TOOLS = [
    {
        "name": "get_stock_quote",
        "description": "Fetch a live stock quote for a given symbol. Returns current price, daily change, and key metrics.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol (e.g., 'AAPL', 'MSFT', 'TSLA') (required)"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_penny_stocks",
        "description": "Retrieve a list of penny stocks (stocks under $5) with current prices and daily percentage changes. Great for day trading.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_stock_intraday",
        "description": "Get intraday stock trading data (price movements throughout the day) for a given symbol.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol (required)"
                },
                "interval": {
                    "type": "string",
                    "enum": ["1min", "5min", "15min", "30min", "60min"],
                    "description": "Time interval for data points (default: 5min)"
                }
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "get_stock_daily",
        "description": "Get daily stock data for the past year. Useful for longer-term analysis and trend spotting.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol (required)"
                }
            },
            "required": ["symbol"]
        }
    }
]

def handle_stock_tool(tool_name, tool_input):
    """Handle stock market tool calls and route to backend API."""
    import requests
    
    base_url = "http://localhost:3001/api"
    
    try:
        if tool_name == "get_stock_quote":
            symbol = tool_input.get("symbol")
            response = requests.get(f"{base_url}/external-stocks/quote/{symbol}")
            return response.json()
        
        elif tool_name == "get_penny_stocks":
            response = requests.get(f"{base_url}/external-stocks/penny-stocks")
            return response.json()
        
        elif tool_name == "get_stock_intraday":
            symbol = tool_input.get("symbol")
            interval = tool_input.get("interval", "5min")
            response = requests.get(f"{base_url}/external-stocks/intraday/{symbol}?interval={interval}")
            return response.json()
        
        elif tool_name == "get_stock_daily":
            symbol = tool_input.get("symbol")
            response = requests.get(f"{base_url}/external-stocks/daily/{symbol}")
            return response.json()
        
        else:
            return {"error": f"Unknown stock tool: {tool_name}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch stock data: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
