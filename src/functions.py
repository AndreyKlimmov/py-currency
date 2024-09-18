import requests, json, time, tzlocal, pytz
from dotenv import dotenv_values
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

cred = dict(dotenv_values("../.env"))
user = cred['USER_MONGO_DB']
password = cred['PASSWORD_MONGO_DB']
uri = f'mongodb+srv://{user}:{password}@cluster0.psnbsei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(uri, server_api=ServerApi('1'))
tz_info = tzlocal.get_localzone()

def bank_gov_ua(start, end, valcode, sort, order):
    try:
        response = requests.get(f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={start}&end={end}&valcode={valcode}&sort={sort}&order={order}&json')
        rate = json.loads(response.text)
        return rate
    except Exception as e:
        raise Exception("Exception raised in bank_gov_ua function: ", e)

def mongo_last(db, col):
    try:
        database = client.get_database(db)
        collection = database.get_collection(col)
        item = list(collection.find().sort({"_id": -1}).limit(1));
        last_date = item[0]['exchangedate']
        # client.close()
        return last_date
    except Exception as e:
        raise Exception("Exception raised in mongo_last function: ", e)

def mongo_add(items, db, col):
    try:
        database = client.get_database(db)
        collection = database.get_collection(col)
        collection.insert_many(items)
        # client.close()
    except Exception as e:
        raise Exception("Exception raised in mongo_add function: ", e)

def day_add(date):
    date = datetime.strptime(date, "%d.%m.%Y") + timedelta(days=1)
    date = datetime.strftime(date, "%d.%m.%Y")
    return date

def format_date(date):
    temp = date.split(".")
    temp.reverse()
    date = ''.join(temp)
    return date

def format_today():
    today = datetime.now(pytz.timezone("Europe/Kiev"))
    today_str = datetime.strftime(today, "%d.%m.%Y")
    date = format_date(today_str)
    return date

def is_updated(last_date):
    delta = datetime.now().replace(tzinfo=ZoneInfo(str(tz_info))) - datetime.strptime(last_date, "%d.%m.%Y").replace(tzinfo=ZoneInfo("Europe/Kiev"))
    
    if delta.days > 0:
        return False
    else:
        return True