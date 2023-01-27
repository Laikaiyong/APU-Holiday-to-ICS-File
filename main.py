import requests
import json
from datetime import datetime, date
from dateutil import parser
from icalendar import Calendar, Event
from pytz import timezone

year = date.today().year

api_active_token = "ST-9965183-ZVwdDpT-fbc-v38mgAf-u9CLWPYip-172-32-54-57"
api_url = f"https://2o7wc015dc.execute-api.ap-southeast-1.amazonaws.com/dev/v2/transix/holiday/active?ticket={api_active_token}"

response = requests.get(url=api_url)

holidays = json.loads(response.text)[1]['holidays']
kl_timezone = timezone('Asia/Kuala_Lumpur')

calendar = Calendar()
calendar.add('prodid', '-//My calendar product//example.com//')
calendar.add('version', '2.0')

index = 0
for holiday in holidays:
    if holiday["holiday_people_affected"] in ["staffs", "all"]:
        event = Event()
        event.add('summary', holiday['holiday_name'] + " " + str(year))
        # date = datetime.strptime(holiday['holiday_start_date'][:-4], '%a, %d %b %Y %H:%M:%S')
        date = parser.parse(holiday['holiday_start_date'])
        # end_date = parser.parse(holiday['holiday_end_date'][:-4])
        event.add('dtstart', date)
        event.add('dtend', date)
        event.add('dtstamp', date)

        # print(holiday['holiday_name'])
        # if holiday['holiday_name'].startswith("Christmas Day") or holiday['holiday_name'].startswith("New Year"):
        #     event.extra.append(ContentLine(
        #         name="RRULE", value=f"FREQ=YEARLY;BYMONTH={date.month};BYMONTHDAY={date.day}"
        #     ))
        calendar.add_component(event)

f = open(f"ics_files/holiday-{year}.ics", 'wb')
f.write(calendar.to_ical())
f.close()