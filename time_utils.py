import ntptime
import time

def sync_time():
    # Set the NTP server
    ntptime.host = "1.europe.pool.ntp.org"
    # Sync UTC time from the NTP server
    ntptime.settime()

# Function to determine if DST is in effect in Europe
def is_dst_europe(year, month, day):
    # DST starts last Sunday in March
    dst_start = (31 - ((5 * year // 4 + 4) % 7), 3)  # Last Sunday of March
    # DST ends last Sunday in October
    dst_end = (31 - ((5 * year // 4 + 1) % 7), 10)   # Last Sunday of October
    
    # Check if we're in the DST period
    if (month > 3 and month < 10) or (month == 3 and day >= dst_start[0]) or (month == 10 and day < dst_end[0]):
        return True
    return False

def get_local_time():
    utc_time = time.localtime()
    # Add 1 hour for Central European Time (CET)
    offset = 1 * 3600
    if is_dst_europe(utc_time[0], utc_time[1], utc_time[2]):
        # Add 2 hours for Central European Summer Time (CEST)
        offset = 2 * 3600
    
    return time.localtime(time.mktime(utc_time) + offset)

def local_time_formatted():
    lt = get_local_time()
    return f"{lt[0]:04}-{lt[1]:02}-{lt[2]:02} {lt[3]:02}:{lt[4]:02}:{lt[5]:02}"