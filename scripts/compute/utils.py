import datetime

def late_penalty_old(days_late):
    from math import floor
    days_late = float(days_late)
    days = floor(days_late)
    hours = floor((days_late - days) * 24)
    minutes = floor((days_late - days - hours/24)*24*60)
    return days * 5 + (hours+4)//6 + 0.25 * (minutes//15)

def late_penalty(O):
    if not O["info"]["Due Date"]:
        return 0
    due_date:datetime.datetime = O["info"]["Due Date"]
    if type(due_date) == str:
        # Invalid entry
        print(due_date)
    due_date = f"{due_date.date().strftime('%a, %d %b %Y')}" + " 23:59:59 " + (("+1100" if due_date.month == 3 else "+1000") if O["info"]["Campus"] == "CL" else "+0800")
    dt_format = "%a, %d %b %Y %H:%M:%S %z"

    if not O["ed"]["submitted"]:
        return 0

    submit_time = datetime.datetime.strptime(O["ed"]["submitted"].replace("AEST", "+1000").replace("AEDT", "+1100"), dt_format)
    due_date = datetime.datetime.strptime(due_date, dt_format)

    diff = submit_time - due_date

    if diff.total_seconds() <= 0:
        return 0

    ts = diff.total_seconds()
    tm = ts // 60
    th = tm // 60
    td = th // 24

    # Days late is total days + 1 if th > 1 or th > 0 and tm > 30
    if th >= 1 or (tm > 30):
        td += 1
    return min(35, td * 5)

def late_penalty_with_moodle_fuckery(O):
    if not O["info"]["Due Date"]:
        return 0
    due_date:datetime.datetime = O["info"]["Due Date"]

    moodle = O["override"]["Moodle Due Date"]
    if type(moodle) == str:
        # Wrong format (extrapolated from a comment)
        # Sunday, 27 August 2023, 11:55 PM
        # %A, %d %B %Y, %I:%M %p
        if moodle == "#N/A":
            moodle = due_date
        else:
            moodle = datetime.datetime.strptime(moodle, "%A, %d %B %Y, %I:%M %p")
    elif type(moodle) == datetime.datetime:
        pass
    else:
        moodle = due_date

    if type(due_date) == str:
        # Invalid entry
        print(due_date)


    due_date = max(due_date, moodle)
    # TODO: Fix timezone
    due_date = f"{due_date.date().strftime('%a, %d %b %Y')}" + " 23:59:59 " + (("+1100" if due_date.month == 3 else "+1000") if O["info"]["Campus"] == "CL" else "+0800")
    dt_format = "%a, %d %b %Y %H:%M:%S %z"

    if not O["ed"]["submitted"]:
        return 0

    submit_time = datetime.datetime.strptime(O["ed"]["submitted"].replace("AEST", "+1000").replace("AEDT", "+1100"), dt_format)
    due_date = datetime.datetime.strptime(due_date, dt_format)

    diff = submit_time - due_date

    if diff.total_seconds() <= 0:
        return 0

    ts = diff.total_seconds()
    tm = ts // 60
    th = tm // 60
    td = th // 24

    # Days late is total days + 1 if th > 1 or th > 0 and tm > 30
    if th >= 1 or (tm > 30):
        td += 1
    return min(35, td * 5)
