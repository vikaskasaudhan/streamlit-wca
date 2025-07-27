import re
import pandas as pd
def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}(?:\u202F|\s)?[AP]M\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M\u202f%p - ")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'^([^:]+):\s', message)
        if len(entry) > 2:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hours'] = df['date'].dt.hour
    df['day_name'] = df['date'].dt.day_name()
    df['minutes'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hours']]['hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df