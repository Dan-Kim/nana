from datetime import datetime
import pytz

pst = pytz.timezone('US/Pacific')
jst = pytz.timezone('Asia/Tokyo')


def get_time_from_epoch(epoch, tz=pst):
  dt = datetime.fromtimestamp(epoch, tz)
  hour = dt.hour
  AMPM = 'PM' if hour >= 12 else 'AM'
  hour = hour - 12 if hour > 12 else hour
  hour = hour + 12 if hour == 0 else hour
  minute = '0{0}'.format(dt.minute) if dt.minute < 10 else str(dt.minute)
  return '{0}:{1} {2}'.format(hour, minute, AMPM)


def get_date_from_epoch(epoch, tz=pst):
  dt = datetime.fromtimestamp(epoch, tz)
  return '{0}/{1}'.format('0{0}'.format(dt.month) if dt.month < 10 else dt.month,
                          '0{0}'.format(dt.day) if dt.day < 10 else dt.day)


def get_weekday(dt):
  num = dt.weekday()
  day_dic = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
  }
  return day_dic[num]


def get_current_japan_time():
  jp_dt = datetime.now()
  return '{0}, {1}, {2}'.format(get_weekday(jp_dt), get_date_from_epoch(jp_dt.timestamp(), tz=jst),
                                get_time_from_epoch(datetime.now().timestamp(), tz=jst))
