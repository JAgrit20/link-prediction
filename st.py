import datetime
import pytz
import yfinance as yf
import json

# Assuming request.body and request.POST['symbol'] are provided, 
# here's a stub to simulate a request for the purpose of this code

# Current date
dtobj1 = datetime.datetime.utcnow()
dtobj3 = dtobj1.replace(tzinfo=pytz.UTC)
dtobj_india = dtobj3.astimezone(pytz.timezone("Asia/Calcutta"))

# Different time frames
dates = {
    "15_days_ago": dtobj_india - datetime.timedelta(days=15),
    "30_days_ago": dtobj_india - datetime.timedelta(days=30),
    "90_days_ago": dtobj_india - datetime.timedelta(days=90),
    "1_year_ago": dtobj_india - datetime.timedelta(days=365),
    "2_years_ago": dtobj_india - datetime.timedelta(days=2*365)
}

for key, value in dates.items():
    dates[key] = value.strftime("%Y-%m-%d")

for key, value in dates.items():
    print(f"{key}: {value}")

# Add month-wise data for the current year
current_year = dtobj_india.year
current_month = dtobj_india.month

for month in range(1, current_month):
    month_key = datetime.date(current_year, month, 1).strftime('%B')
    dates[month_key] = datetime.date(current_year, month, 1).strftime('%Y-%m-%d')

# Add month-wise data for the previous year
for month in range(1, 13):
    month_key = datetime.date(current_year - 1, month, 1).strftime('%B') + "_last_year"
    dates[month_key] = datetime.date(current_year - 1, month, 1).strftime('%Y-%m-%d')

for key, value in dates.items():
    print(f"{key}: {value}")

# Convert stock_data index to string format if it's not
st_name = "TCS"

# Fetching stock data
stock_data = yf.download(st_name+".NS", period='20y', interval='1d')
stock_data.index = stock_data.index.strftime('%Y-%m-%d')
perf_data = {}

def find_closest_previous_date(target_date, stock_data):
    target_date_dt = datetime.datetime.strptime(target_date, "%Y-%m-%d").date()
    while target_date not in stock_data.index and target_date_dt > datetime.datetime.strptime(stock_data.index[0], "%Y-%m-%d").date():
        target_date_dt = target_date_dt - datetime.timedelta(days=1)
        target_date = target_date_dt.strftime('%Y-%m-%d')
    if target_date in stock_data.index:
        print(target_date)
        return target_date
    return None


for key, dt in dates.items():
    actual_dt = find_closest_previous_date(dt, stock_data)
    if actual_dt:
        opening_price = stock_data.loc[actual_dt]['Open']
        current_price = stock_data.iloc[-1]['Close']
        change_percentage = ((current_price - opening_price) / opening_price) * 100
        perf_data[key] = change_percentage
    else:
        print(f"No available data for date close to {key} ({dt})")

# Printing the results
for key, value in perf_data.items():
    print(f"{key}: {value:.2f}%")
