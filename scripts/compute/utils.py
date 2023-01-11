def late_penalty(days_late):
    from math import floor
    days_late = float(days_late)
    days = floor(days_late)
    hours = floor((days_late - days) * 24)
    minutes = floor((days_late - days - hours/24)*24*60)
    return days * 5 + (hours+4)//6 + 0.25 * (minutes//15)
