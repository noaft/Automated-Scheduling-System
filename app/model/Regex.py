import re
from datetime import datetime

def extract_recurrence(time_string):
    """
    Extract recurrence of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] : List of string recurrence detected.
    """
    pattern = r'\b(everytime|every time|any time|any day|everyday|every day|each day|every weekday|all week|every single day|daily)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def extract_part_recurrence(time_string):
    """
    Extract recurrence of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] : List of string [art recurrence detected.
    """
    pattern = r'\b(everymorning|every morning|everyafternoon|every afternoon|everyevening|every evening|every night|everynight)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def extract_day(time_string):
    """
    Extract  days of week from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        [List] :List of string days of week detected.
    """

    pattern = r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
    match = re.findall(pattern, time_string.lower(), re.IGNORECASE)
    
    if match:
        return match
    else:
        return None

def clean_time(time_string):
    """
    Clean string time extracted.
    Args:
        time_string (str): str contain time.
    Result:
        time (str): time add " " pre ['pm', 'am'] and clear space last string if have.
    """
    ar_ = []
    words = time_string.split()
    
    for word in words: 
        # Check if have 'am'or 'pm' in code
        if 'am' in word.lower() and word.lower() != 'am':
            number_part = word.lower().split('am')[0]
            ar_.append(number_part.strip())  # add to list
            ar_.append('am')  # add to list
        # Example: 3pm
        elif 'pm' in word.lower() and word.lower() != 'pm':
            number_part = word.lower().split('pm')[0]
            ar_.append(number_part.strip()) 
            ar_.append('pm')  
        # Remove last space in text if have
        elif word.strip(): 
            ar_.append(word)
    
    result = " ".join(ar_).strip()  # Kết hợp lại và loại bỏ khoảng trắng ở đầu và cuối

    return result


def get_start_end(time_string):
    """
    Get start and end time in string.
    Args:
        time_string (str): str contain time.
    Result:
        start_time: Start time in string.
        end_time: End time in string.
    """
    ar_ = clean_time(time_string).split(" ")

    # Example: 11 am to 12 am
    if ar_[1] in ['am', 'pm'] and len(ar_) == 5:
        start_time = ar_[0] + " " + ar_[1]
        end_time = ar_[3] + " " + ar_[4]
    # Example : 11 am to 12
    elif ar_[1] in ['am', 'pm']:
        start_time = ar_[0] + " " + ar_[1]
        end_time = ar_[3] + " " + ar_[1]
    # Example : 11 to 12 am
    else:
        start_time = ar_[0] + " " + ar_[3]
        end_time = ar_[2] + " " + ar_[3]
    
    return start_time, end_time


def extract_time(time_string):
    """
    Extract time from string.
    Args:
        time_string (str): string contain hours.
    Return: 
        Return string strt and end time detected.
    """
    
    # Regex to check valid time in 12-hour format
    pattern = r"((([1-9]|1[0-2])(:[0-5][0-9])?\s?(am|pm)?)\s?to\s(([1-9]|1[0-2])(:[0-5][0-9])?\s?(am|pm)?\s))"
    # add space for fit pattern
    time = time_string.split('.')[0]
    time = time_string.split(',')[0]
    time += " "
    # Search for the time pattern in the string
    match = re.findall(pattern, time.lower(), re.IGNORECASE)
    list_day= []
    SE_ = []
    if match:
        for time_str in match:
            list_day.append(get_start_end(time_str[0]))
            SE_.append(time_str[0])
    if match:
        return list_day, SE_
    else:
        return [None, None], None

def caculate_time(start_time):
    """
    Transform str to int time
    Args:
        start_time (str): time needed tranform
    return:
        Time (int): time to tranform second
    """
    time = start_time.split(" ")[0]
    time = time.split(":")
    if len(time) == 2:
        time = int(time[0]) * 3600 + int(time[1]) * 60
    elif len(time) == 3:
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
    else:
        time = int(time[0]) * 3600
    
    if 'pm' in start_time:
        time += 12 * 3600
    
    return time

    
if __name__ == '__main__':
    # test for hours
    time_string = "every morning from 2 to 10:11 am."
    start_time, end_time = extract_time(time_string)
    print("Start time:", start_time, "\nEnd time:", end_time)
    # test for day
    time_string = "Monday and sunday from 2 to 10:11 am."
    day = extract_day(time_string)
    print(day)
    # test for day
    time_string = "everytime from 2 to 10:11 am."
    recurrence = extract_recurrence(time_string)
    print(recurrence)
    # test for day
    time_string = "i am avaiable Monday 2 to 10:11 am and Tuesday 1 to 10 pm."
    recurrence = extract_part_recurrence(time_string)
    print(recurrence)