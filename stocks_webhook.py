#!/usr/bin/env python
# coding=utf-8

## imports
import sys
import requests
import os
from dotenv import load_dotenv
import yfinance as yf


####### Params ############
n = len(sys.argv)
if n < 2:
    print("Usage: python stocks_webhook.py <TICKER>")
    sys.exit(1)

TICKER = sys.argv[1]

############## Prepare the webhook ####################
# take environment variables from .env.
load_dotenv()
wh_id = os.getenv('WEBHOOK_ID')
wh_token = os.getenv('WEBHOOK_TOKEN')
url = "https://discord.com/api/webhooks/{}/{}".format(wh_id, wh_token)


############## Gather the data ####################

tsla = yf.Ticker(TICKER)
stock_info = tsla.info
#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data_content_raw = "Aquí va la información de hoy para {} ({})"
data_content_filled = data_content_raw.format(stock_info["longName"],stock_info["symbol"])
data = {
    "content" : data_content_filled,
    "username" : "Elon Musk"
}

#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
previous_str = ":closed_umbrella: {} {}".format(stock_info["previousClose"], stock_info["currency"]) 
open_str = ":checkered_flag: {} {}".format(stock_info["open"], stock_info["currency"])
current_str = ":money_with_wings: {} {}".format(stock_info["currentPrice"], stock_info["currency"])
fifty2_value = stock_info["52WeekChange"]
if fifty2_value > 0:
    emoji_str = ":thumbsup:"
else:
    emoji_str = ":thumbsdown:"

## the 0s thing is for a percentage
## see here https://stackoverflow.com/a/23764798 
fifty2 = "{} {:.1%}".format(emoji_str, fifty2_value)

## max won in last 52
fifty2_low = stock_info["fiftyTwoWeekLow"]
to_fifty2_low = stock_info["currentPrice"]/fifty2_low - 1
if to_fifty2_low > 0:
    emoji_str2 = ":green_apple:"
else:
    emoji_str2 = ":apple:"
to_fifty2_low_str = "{} {:.1%}".format(emoji_str2, to_fifty2_low)

## max lost in last 52
fifty_2_high = stock_info["fiftyTwoWeekHigh"]
to_fifty2_high = stock_info["currentPrice"]/fifty_2_high
emoji_str3 = ":thermometer:"
to_fifty2_high_str = "{} {:.1%}".format(emoji_str3, to_fifty2_high)

data["embeds"] = [
    {
        "title" : stock_info["symbol"],
        "image": {
            "url" : stock_info["logo_url"]
        } ,
        "fields": [
            {"name" : "Prev. Close", 
            "value": previous_str,
            "inline": True},
            {"name" : "Open", 
            "value": open_str,
            "inline": True},
            {"name" : "Current", 
            "value": current_str,
            "inline": True},
            {"name" : "52WeekChange", 
            "value": fifty2,
            "inline": True},
            {"name" : "From 52 Low", 
            "value": to_fifty2_low_str,
            "inline": True},
            {"name" : "From 52 High", 
            "value": to_fifty2_high_str,
            "inline": True},
        ]
    }
]

print(data)
result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
