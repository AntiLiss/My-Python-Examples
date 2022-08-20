import time, datetime, ntplib


def today_sched():
    # For the bot to work correctly, the time on the device must match the real time
    con_status = False  # Trying to connect to the server with time
    try:
        ntpClient = ntplib.NTPClient()
        resp = ntpClient.request('pool.ntp.org')
        con_status = True
    except:
        return 'Network error.'


    if con_status:   # if connected True, then do:
        ntp_time = time.ctime(resp.tx_time).split()  # take time from the server and split it into a list
        ntp_time_dict = {}  # for convenience, create a dictionary where we lay out the time in parts

        i = 0
        for item in ['day_name', 'month_name', 'day', 'time', 'year']:  # filling dict
            ntp_time_dict[item] = ntp_time[i]
            i += 1

        # bring the time from the server to this format 30-09-2099 23 (hours)
        ntp_time_formatted = ntp_time_dict['day'] + '-' + ntp_time_dict['month_name'] + '-' + ntp_time_dict['year'] + ' ' + ntp_time_dict['time'][:ntp_time_dict['time'].index(':')]
        device_time = datetime.datetime.now().strftime('%d-%b-%Y %H') # take the gadget time in the same format

        def group_sched():  # group interleaving function
            # find difference in days between schedule start date and today date
            # I found out that:
            # if difference is even number, today is 1-st group
            # else if it is odd number, today is 2-nd group
            diff = datetime.date(2022, 8, 15) - datetime.datetime.now().date()

            if datetime.datetime.now().date().strftime('%d-%b-%Y') == '15-Aug-2022': # schedule start date and group is 1-st
                return 1
              
            # In this block ff today is a holiday, we show the schedule for next Monday
            elif ntp_time_dict['day_name'] == 'Sat' and diff.days % 2 != 0: 
                return 'holiday, next 2 group'
            elif ntp_time_dict['day_name'] == 'Sat' and diff.days % 2 == 0:  
                return 'holiday, next 1 group'  

            elif ntp_time_dict['day_name'] == 'Sun' and diff.days % 2 == 0: 
                return 'holiday, next 2 group' 
            elif ntp_time_dict['day_name'] == 'Sun' and diff.days % 2 != 0: 
                return 'holiday, next 1 group' 
            #------------------------------------------------------------------------
            
            elif diff.days % 2 == 0:  # here we set schedule for work weekdays
                return 1
            elif diff.days % 2 != 0:
                return 2
                
        if device_time != ntp_time_formatted:  # check equality of the real time and the gadget time
            return 'For the bot to work correctly, set the correct time on your device!'
        else:
            # take groups schedule from source
            # actually you should create database and take data from it
            # but for the sake of simplicity, I used simple txt files
            with open('group 1.txt', 'r', encoding='utf-8') as group_1:
                group_1_sched = group_1.read()
            with open('group 2.txt', 'r', encoding='utf-8') as group_2:
                group_2_sched = group_2.read()

            if group_sched() == 1:
                return f'Today is I-st group\n\n{group_1_sched}'
            elif group_sched() == 2:
                return f'Today is II-nd group\n\n{group_2_sched}'
            elif group_sched() == 'holiday, next 1 group':
                return f'Saturday and Sunday are holidays. But in Monday there is I-st group:\n\n{group_1_sched}'
            elif group_sched() == 'holiday, next 2 group':
                return f'Saturday and Sunday are holidays. But in Monday there is II-st group:\n\n{group_2_sched}'

def full_sched():  # show schedule for both groups
    full = ''
    with open('group 1.txt', 'r', encoding='utf-8') as grp1:
        full = 'Group I\n\n' + grp1.read()
    with open('group 2.txt', 'r', encoding='utf-8') as grp2:
        full = full + '\n\n\nGroup II\n\n' + grp2.read()
    return full
