from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(
    title="Crypto Market & Orderbook Tracker",
    description="Returns real-time price action and orderbook depth for digital assets.",
    version="1.0.0"
)

@app.get("/v1/crypto/market")
def get_market_data(symbol: str = "BTCUSDT"):
    """
    Pass in a trading pair to retrieve current market metrics and orderbook depth.
    """
    # Strip accidental spaces and convert to uppercase
    formatted_symbol = symbol.strip().upper()
    
    ticker_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={formatted_symbol}"
    depth_url = f"https://api.binance.com/api/v3/depth?symbol={formatted_symbol}&limit=5"
    
    try:
        ticker_response = requests.get(ticker_url, timeout=5)
        depth_response = requests.get(depth_url, timeout=5)
        
        if ticker_response.status_code != 200:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid symbol '{formatted_symbol}' or data currently unavailable."
            )
            
        ticker_data = ticker_response.json()
        depth_data = depth_response.json()
        
        return {
            "symbol": formatted_symbol,
            "current_price": ticker_data.get("lastPrice"),
            "price_change_24h": ticker_data.get("priceChange"),
            "percent_change_24h": ticker_data.get("priceChangePercent"),
            "volume_24h": ticker_data.get("volume"),
            "top_bids": depth_data.get("bids", []),
            "top_asks": depth_data.get("asks", [])
        }
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"External network error: {str(e)}")