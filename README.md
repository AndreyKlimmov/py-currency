### Notes
------------
`pip install schedule`
`pip install pymongo`
`pip install python-dotenv`

.env file:
USER_MONGO_DB=\<username\>
PASSWORD_MONGO_DB=\<password\>

### API [bank.gov.ua](https://bank.gov.ua/ua/open-data/api-dev)
------------
Server response if wrong parameters:
```python
[{'message': 'Wrong parameters format'}]
```
  `<class 'list'>`

Server response if  **empty** or **future** date
```python
[]
```
 `<class 'list'> `

==Create first row in mongodb:==
```python
data = bank_gov_ua("19970101", "19970101", "usd", "exchangedate", "asc")
```
 
### Time calculation according timezone
------------
**Cloud Run function (server local timezone "UTC") example:**

Delta should be at least 1 day to run code for updating db
```python
delta = datetime.now().replace(tzinfo=ZoneInfo(str(tz_info))) - datetime.strptime(last_date, "%d.%m.%Y").replace(tzinfo=ZoneInfo("Europe/Kiev"))
```
where
```python
tz_info = tzlocal.get_localzone() #server local timezone is "UTC"
```

### [Cloud Run functions](https://console.cloud.google.com/functions)
------------
Scheduler https://console.cloud.google.com/cloudscheduler
`5 0 * * *` - every day at 00:05:00
The quick and simple editor for cron schedule expressions https://crontab.guru/

Add libs to **requirements.txt**:
`functions-framework==3.*` (automaticly created first row )
`pymongo==4.8.0`
`Requests==2.32.3`
`schedule==1.2.2`
Also see how [[#To generate requirements.txt]]

### Docker
------------
##### To generate requirements.txt:
Install
`pip3 install pipreqs` 

Run in current directory
`python3 -m pipreqs.pipreqs .`

Platform might be necessary:
`FROM **--platform=linux/amd64** python:3.9.20-slim`

Terminal useful commands:
`docker build -t currency:0.0 .`
`docker images`
`docker run --name **currency** -d 00cd1e30cae0`

### Open ISSUES:
------------
* `client.close()` - is it necessary for mongodb?
* https://www.pythonanywhere.com/:
	`pip install -U --ignore-installed pymongo`
*    Is the except necessary?
```python
	try:
	...
    except Exception as e:
    ```


