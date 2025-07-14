from datetime import datetime

class TimeHelper:
    @staticmethod
    def get_current_time():
        """Returns the current time as a string in the format YYYY-MM-DD HH:MM:SS."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date():
        """Returns the current date as a string in the format YYYY-MM-DD."""
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_current_year():
        """Returns the current year as an integer."""
        return datetime.now().year

    @staticmethod
    def get_current_month():
        """Returns the current month as an integer."""
        return datetime.now().month

    @staticmethod
    def get_current_day():
        """Returns the current day as an integer."""
        return datetime.now().day
