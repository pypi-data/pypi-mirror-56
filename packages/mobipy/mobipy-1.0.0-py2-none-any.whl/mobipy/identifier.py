class Identifier:
  """
  A class that encapsulates the column names of a dataset for use in Mobipy functions.
  ...

  Attributes
  ----------
  lat_name : str
      the latitude column name
  lon_name : str
      the longitude column name
  timestamp : str
      the timestamp column name, used in some mobipy functions
  start_time : str
      the start_time column name, used in some mobipy functions
  end_time : str
      the end_time column name, used in some mobipy functions
  item_id : str
      the item or user/group id column name, used in some mobipy functions
  """
  
  def __init__(self, lat_name, lon_name, timestamp, start_time, end_time, item_id):
    """
    Parameters
    ----------
    lat_name : str
        the latitude column name
    lon_name : str
        the longitude column name
    timestamp : str
        the timestamp column name, used in some mobipy functions
    start_time : str
        the start_time column name, used in some mobipy functions
    end_time : str
        the end_time column name, used in some mobipy functions
    item_id : str
        the item or user/group id column name, used in some mobipy functions
    """

    self.latitude = lat_name
    self.longitude = lon_name
    self.timestamp = timestamp
    self.start_time = start_time
    self.end_time = end_time
    self.item_id = item_id