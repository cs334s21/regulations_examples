from datetime import datetime, timedelta

def clean_date(date_):
    return date_.replace("T", " ").replace("Z", "")

def to_eastern_time(date_):
    """Expects date in this format yyyy-mm-dd hh:mm:ss"""
    return str(datetime.fromisoformat(date_) + timedelta(hours=-4))

