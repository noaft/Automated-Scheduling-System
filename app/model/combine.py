from model.Regex import extract_recurrence, extract_part_recurrence, extract_day, extract_time
from datetime import datetime
from model.QA_model import QA_model as model

def detect_time(start_time, end_time, recurrence, day_week, part_recurrence):
    """
    Extract all time and format it.
    Args:
        start_time (str): start time in text
        end_time (str): end time in text
        recurrence (str): recurrence in text
        day_week (str): each weekday mentioned in the text
    Returns:
        List: A list binary where each inner list represents a day.
        If a day has availability, the first element is 1, and the second element is a list of time ranges.
    """

    Time= [[0,[]] for _ in range(7)]

    map_ = {
        'morning': (6 * 60, 11 * 60 + 59),      # 6:00 AM to 11:59 AM
        'afternoon': (12 * 60, 17 * 60 + 59),    # 12:00 PM to 5:59 PM
        'evening': (18 * 60, 20 * 60 + 59),      # 6:00 PM to 8:59 PM
        'night': (21 * 60, 23 * 60 + 59)         # 9:00 PM to 11:59 PM
    }

    # Map days of the week to indices
    days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    # If recurrence is true, mark all days as available
    if recurrence or part_recurrence:
        for i in range(7):
            Time[i][0] = 1
    else:
        # If specific days are mentioned, mark only those as available
        for day in day_week:
            if day in days_map:
                Time[days_map[day]][0] = 1
    
    # Add specific start and end times if provided
    if start_time:
        st = time_to_seconds(start_time)
        et = time_to_seconds(end_time)
        for i in range(7):
            if Time[i][0] == 1:
                Time[i][1].append((st, et))

    # Add predefined time ranges based on part recurrence (morning, afternoon, etc.)
    if part_recurrence:
        for part in map_.keys():
            if part in part_recurrence:    
                for i in range(7):
                    if Time[i][0] == 1:
                        Time[i][1].append(map_[part])

    if start_time is None:
        for i in range(7):
            if Time[i][0] == 1:
                Time[i][1].append((0, 1440))

    return Time

def subtract_intervals(free, busy):
    """
    Subtracts intervals from a list of available (free) intervals using a list of unavailable (not_free) intervals.
    Args:
        free (list of tuples): A list of available time.
        not_free (list of tuples): A list of unvaiable time.

    Returns:
        list of binary: A list of non-overlapping intervals from the `free` list after subtracting intervals from 
                        the `not_free` list.
    """

    all_frees = [0 for _ in range(10080)]

    for i in range(10080):
        all_frees[i] = free[i] - busy[i]
    return all_frees

def time_to_seconds(time_str):
    """
    Convert a time string in the format 'hh:mm:ss AM/PM' or 'hh:mm AM/PM' to seconds.
    
    Args:
        time_str (str): The time string to convert.
        
    Returns:
        int: The time in seconds from midnight.
    """
    try:
        # Parse the time string to a datetime object
        len_ = len(time_str.split(":"))
        if len_ == 3:
            time_obj = datetime.strptime(time_str.strip(), '%I:%M:%S %p')  # Format with seconds
        elif len_ == 2:
            time_obj = datetime.strptime(time_str.strip(), '%I:%M %p')  # Format without seconds
        else:
            time_obj = datetime.strptime(time_str.strip(), '%I %p')  # Format without seconds    
        # Convert hours, minutes, and seconds to seconds
        seconds = time_obj.hour * 60 + time_obj.minute
        return seconds
    except ValueError:
        print("Invalid time format. Please use 'hh:mm:ss AM/PM' or 'hh:mm AM/PM'.")
        return None

def extract_one(message, model, full_text):
    """
    Extract availability and free time in text for each day of the week.
    Args:
        message (str): message from user
    Return:
        List[List[int]]: 2D list with day availability and free time in seconds
    """
    # Map days of the week to indices
    
    avaiable_time = [[0,[]] for _ in range(7)]
    avaiable_time_fake = []
    days_map = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }
    
    # Extract recurrence and part recurrence
    # recurrence = extract_recurrence(message)
    part_recurrence = extract_part_recurrence(message)
    # day_week = extract_day(message)
    list_time, full_time = extract_time(message)
    if list_time != [None , None]:
        for i in range(len(list_time)):
            start_time = list_time[i][0]
            end_time = list_time[i][1]
            day_week = extract_day(model.get_day(full_text, full_time[i]))
            if day_week:
                recurrence = extract_recurrence(message)
                avaiable_time_fake.append(detect_time(start_time, end_time, recurrence, day_week, part_recurrence))
            else:
                recurrence = extract_recurrence(message)
                avaiable_time_fake.append(detect_time(start_time, end_time, recurrence, None, part_recurrence))
    else:
        recurrence = extract_recurrence(message)
        day_week = extract_day(message)
        avaiable_time_fake.append(detect_time(None, None, recurrence, day_week, part_recurrence))

    for avaiables in avaiable_time_fake:
        for i in range(7):
            if avaiables[i][0] == 1:
                for j in avaiables[i][1]:
                    avaiable_time[i][0] = 1
                    avaiable_time[i][1].append(j)                   
    
    return transform_binary(avaiable_time)

def detect_avaiable(free, busy, model, context):
    """
    Get free time onion busy time:
    Args:
        free (List[[]]): free time.
        busy (List[[]]): busy time.
        model (class): model Nlp
        context (str): context
    Return:
        List of free time in test
    """
    if free and busy is None:
        result = extract_one(free, model, context)
        r_ = result[540:1020] # 9 am -> 5 pm
        for i in range(1, 7):
            start = i * 1440 + 540
            end = i * 1440 + 1020
            r_ += result[start:end]
        return r_
    elif free and busy:
        print(busy)
        free_avaiable = extract_one(free, model, context)
        busy_time = extract_one(busy, model, context)
        result = subtract_intervals(free_avaiable, busy_time)
        r_ = result[540:1020] # 9 am -> 5 pm
        for i in range(1, 7):
            start = i * 1440 + 540
            end = i * 1440 + 1020
            r_ += result[start:end]
        return r_
    if free is None and busy is None:
        r_ = [[0] for _ in range(3360)]
        return r_
    free_avaiable = [[1,[(0, 10080)]] for _ in range(7) ]
    result = subtract_intervals(free_avaiable, busy_time)
    print(result)
    r_ = result[540:1020] # 9 am -> 5 pm
    for i in range(1, 7):
        start = i * 1440 + 540
        end = i * 1440 + 1020
        r_ += result[start:end]
    return r_

def transform_binary(Time):
    """
    Transform all list to array binary.
    Args:
        time (List[[]]): list time avaiable
    Return:
        Return (List): [0,1,1,...] binary array
    """
    List = [0 for _ in range(10080)]
    for i in range(7):
        if Time[i][0] == 1:
            for (start, end) in Time[i][1]:
                for j in range(start + i * 1440, end + i * 1440):
                    List[j] = 1
    return List

def multi_user(model, messages, time):
    """
    Extract and combine time of all user
    Args: 
        messages List(str): all message of user
    Return:
        Return combine time list
    """
    list_time = []
    len_user = len(messages)
    for message in messages:
        free, busy = get_free_busy(model, message)
        list_time.append(detect_avaiable(free, busy, model, message))
    return find(time, all_time(list_time), len_user)
    

def get_free_busy(model, context):
    """
    Get time free and busy of user
    Args:
        model (class): model NLU
        context: message of user
    Return:
        List free time and busy time
    """
    free, busy = model.get_time(context)
    return free, busy

def all_time(list_time):
    """
    Detect and solotion conflict
    Args:
        arg: all of list time
    return:
        return all time not conflict and number can join
    """
    result = list_time[0]
    print(result)
    for i in range(1, len(list_time)):
        for j in range(3360):
            result[j] +=  list_time[i][j]
    return result

def find(time, list_time, len_user):
    """
    Get time match metting time in free time.
    Args:
        time (int): time meeting.
        list_time (list(int)): List time avaiable.
    Reuturn
        list time list([index]).
        index of start time invaiable.
    """
    result = [[] for _ in range(7)]
    len_user_ = len_user
    st = 0
    ed = 480
    list_time_ = []
    for i in range(7):
        list_time_.append((list_time[st:ed]))
        st = ed
        ed += 480
    print(list_time_)
    while len_user_ > 0:
        for list in range(len(list_time_)):
            flag = 0
            for i in range(480 - time):
                for j in range(time):
                    if list_time_[list][i + j] < len_user_:
                        flag = 1
                        break
                if flag == 0:
                    result[list].append(i)

        if result != [[] for _ in range(7)]:
            return result
        len_user -= 1

    return result 

if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = model(model_name, model_name)
    context1 = "I'm avaiable every morning."
    context2 = "I'm avaiable every morning, except on Tuesday"
    list= [context1, context2]
    r = multi_user(model, list, 300)
    print(r)