from datetime import datetime
import pandas as pd
import requests
from requests.exceptions import RequestException

def resample_ohlc_df(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    try:
        df.sort_values(by='date', inplace=True)

        # Group by the timestamp (day and time) and resample directly
        resample_cols = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last"
        }
        if "volume" in df.columns:
            resample_cols["volume"] = "sum"

        resampled_df = df.set_index('date').groupby(pd.Grouper(freq=timeframe)).agg(resample_cols)

        # Handle missing data with forward fill
        resampled_df.fillna(method='ffill', inplace=True)

        return resampled_df.reset_index()

    except Exception as e:
        print(f"Error occurred while resampling OHLC df: {str(e)}")
        return pd.DataFrame()

# resampled_data = resample_ohlc_df(input_df, '5T')  # Resample to 5-minute intervals



def get_all_expiry_info(index: str) -> list[dict]:
    try:
        with requests.Session() as session:
            url = f"{utils.BACKEND_URL}/nse/get_expiry/{index}"
            response = session.get(url)

            if response.status_code == 307:
                redirect_url = response.headers.get('Location')
                response = session.get(redirect_url)

            response.raise_for_status()  # Raise an exception for any HTTP error status codes

            data = response.json().get("data", [])
            return data

    except RequestException as e:
        print(f"Error fetching expiry dates: {str(e)}")
        return []

# expiry_info = get_all_expiry_info("BANKNIFTY")


import pandas as pd
import requests
from requests.exceptions import RequestException
from datetime import datetime

def get_expiry_comp_dict(list_of_expiry_info_dict):
    try:
        expiry_comp_dict = {
            datetime.strptime(d['expiry_date'], '%Y-%m-%d').date(): d['expiry_comp']
            for d in list_of_expiry_info_dict
        }
        return expiry_comp_dict
    except Exception as e:
        print(f"Error in get_expiry_comp_dict: {str(e)}")
        return {}

def fetch_options_data_and_resample(opt_symbol, start_date, end_date, timeframe):
    try:
        url = f"{utils.BACKEND_URL}/instruments/historical/{opt_symbol}/{start_date}/{end_date}/"
        response = requests.get(url, params={"spot": "false"})

        if response.status_code == 307:
            redirect_url = response.headers.get('Location')
            response = requests.get(redirect_url, params={"spot": "false"})

        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            print(f"No data found for: {opt_symbol}")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        resampled_df = resample_ohlc_df(df, timeframe)
        resampled_df = resampled_df.rename(columns={
            "close": f"{opt_symbol}_close",
            "open": f"{opt_symbol}_open",
            "high": f"{opt_symbol}_high",
            "low": f"{opt_symbol}_low",
            "volume": f"{opt_symbol}_volume"
        })
        return resampled_df

    except RequestException as e:
        print(f"Error fetching data for {opt_symbol}: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in fetch_options_data_and_resample: {str(e)}")
        return pd.DataFrame()

def get_trading_days():
    try:
        url = f"{utils.BACKEND_URL}/nse/get_trading_days/"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json().get("data", [])
        trading_days = [datetime.strptime(x["Date"], "%Y-%m-%d").date() for x in data]
        return trading_days

    except RequestException as e:
        print(f"Error fetching trading days: {str(e)}")
        return []
    except Exception as e:
        print(f"Error in get_trading_days: {str(e)}")
        return []
