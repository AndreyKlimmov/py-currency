import requests, json, time, schedule
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import date, datetime
from functions import *

database = "currency_rate"
collection = "USD(US)_UAH_temp"

def job():
    date = mongo_last(database, collection)

    if is_updated(date):
        print("Updated\n")
    else:
        temp = day_add(date)
        res = format_date(temp)
        data = bank_gov_ua(res, format_today(), "usd", "exchangedate", "asc")
        # data = bank_gov_ua(res, res, "usd", "exchangedate", "asc")

        if not data or data == [{'message': 'Wrong parameters format'}]:
            print("No data on the date or Wrong request parameters\n")
        else:
            print("Data received\n")
            mongo_add(data, database, collection)

schedule.every(0.25).minutes.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().hour.at(":00").do(job)
while True:
    schedule.run_pending()
    time.sleep(31)