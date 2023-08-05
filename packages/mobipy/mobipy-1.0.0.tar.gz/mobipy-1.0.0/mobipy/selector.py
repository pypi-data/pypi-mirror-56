class Selector:
  """
  A class that encapsulates the dataset row selector.
  ...

  Attributes
  ----------
  start_date : str
      the start date in dateformat string YYYY-MM-DD
  end_date : str
      the end date in dateformat string YYYY-MM-DD
  week_days : str
      the week days to be considered, format "XXXXXXX" (7 days), where
      X can be 1 (true) and 0 (false). Starts on sunday.
      Examples:
        1110000 - sunday, monday and tuesday will be selected
        0000001 - only saturday will be selected
  day_hours : str
      similar to week_days but with 24-hour string, 
      format "XXXXXXXXXXXXXXXXXXXXXXXX". Starts at 0h.
      Examples:
        110001110000011110000000 - select rows from 0-2h, 5-8h, 13-17h
        100000000001000000000001 - select rows from 0-1h, 11-12h, 23-0h

  """
    
  def __init__(self, start_date=None, end_date=None, week_days=None, day_hours=None):
    """
    Parameters
    ----------
    start_date : str
        the start date in dateformat string YYYY-MM-DD
    end_date : str
        the end date in dateformat string YYYY-MM-DD
    week_days : str
        the week days to be considered, format "XXXXXXX" (7 days), where
        X can be 1 (true) and 0 (false). Starts on sunday.
        Examples:
          1110000 - sunday, monday and tuesday will be selected
          0000001 - only saturday will be selected
    day_hours : str
        similar to week_days but with 24-hour string, 
        format "XXXXXXXXXXXXXXXXXXXXXXXX". Starts at 0h.
        Examples:
          110001110000011110000000 - select rows from 0-2h, 5-8h, 13-17h
          100000000001000000000001 - select rows from 0-1h, 11-12h, 23-0h
    """
    
    self.start_date = start_date
    self.end_date = end_date
    self.week_days = week_days
    self.day_hours = day_hours