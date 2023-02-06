import requests
from twilio.rest import Client

API_STOCK_URL = "https://www.alphavantage.co/query"
API_STOCK_KEY = "getyouralphavantageapikey"
API_STOCK_COM = "IBM"
API_NEWS_COM = "IBM"
API_NEWS_URL = "https://newsapi.org/v2/everything"
API_NEWS_KEY = "getyournewsapikey"
account_sid = "getyourtwiliosid"
auth_token = "getyourtwilioauthkey"

#GET STOCKS INFO (you have to pay to access other companies)
stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": API_STOCK_COM,
    "apikey": API_STOCK_KEY
}
response = requests.get(API_STOCK_URL, params=stock_params)
stocks_data = response.json()["Time Series (Daily)"]
print("Stocks data: ", stocks_data)
stocks_data_list = [value for(key, value) in stocks_data.items()]
friday_data_latestWeek = stocks_data_list[0]['4. close']
thursday_data_latestWeek = stocks_data_list[1]['4. close']
diff = abs(float(friday_data_latestWeek) - float(thursday_data_latestWeek))
print("Stocks diff: ", diff)
#GET PERCENTAGE
diff_percent = (diff / float(friday_data_latestWeek)) * 100
print("Stocks diff percentage: ", diff_percent)
#IF PERCENTAGE IS > 5 GET NEWS (OR FORCE THE CHECKING VALUE FOR TESTING)
if diff_percent > 5:
    news_params = {
        "q": API_NEWS_COM,
        "apiKey": API_NEWS_KEY
    }
    response = requests.get(API_NEWS_URL, params=news_params)
    news_data = response.json()
    first_three_news = news_data["articles"][:3]
    formatted_news = [f"Headline: {articles['title']}, \nBrief: {articles['description']}" for articles in first_three_news]
    print("Text Mesg :", formatted_news)
    #SEND TEXT VIA TWILIO
    client = Client(account_sid, auth_token)
    for article in formatted_news:
        message = client.messages.create(
            body=article,
            #change these numbers with your twilio registered numbers
            from_='+16180000000',
            to='+639980000000'
        )