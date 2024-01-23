from __future__ import annotations
from typing import Type
from datetime import datetime
from json import loads as load_json

class Coordinate:
  """ Describes the coordinate of a machine

  Attributes:
    ip (str): Ip address of the machine that sended the coordinate.
    time (datetime): Time when the message was sended
    latitude (float): Latitude of the machine
    longitude (float): Longitude of the machine

  Methods:
    to_json(self): Convert the current instance to a JSON string
    from_json(str): Convert a JSON string to a new instance
    get_latitude_dms(self): Returns the latitude in degree-minute-seconds
    format
    get_longitude_dms(self): Returns the longitude in degree-minute-seconds
    format

  """
  def __init__(
    self: Self,
    ip: str,
    time: datetime,
    latitude: float,
    longitude: float,
  ):
    """ Create a new Coordinate with the given attributes

    Parameters:
      self (Self): Current instance
      ip (str): Ip Address of the object
      time (datetime): Time of the localisation
      latitude (float): Latitude of the object
      longitude (float): Longitude of the object
    """
    self.ip = ip
    self.time = time
    self.latitude = latitude
    self.longitude = longitude

  def to_json(self: Self) -> str:
    """ Convert the current instance to a JSON string
    
    Arguments:
      self (Self): Current instance

    Returns:
      (str): Attributes of the instance in a JSON file

    Example:
    ```python
    my_coordinate = Coordinate(
      'ip',
      datetime.fromtimestamp(1000),
      15.2,
      -3.1
    )
    assert my_coordinate.to_json() == ("{"
      "\"ip\":\"ip\","
      "\"time\":\"1000.0\","
      "\"latitude\":\"15.2\","
      "\"longitude\":\"-3.1\""
      "}")
    ```
    """
    return (
      '{'
      f'\"ip\":\"{self.ip}\",'
      f'\"time\":\"{self.time.timestamp()}\",'
      f'\"latitude\":\"{self.latitude}\",'
      f'\"longitude\":\"{self.longitude}\"'
      '}'
    )

  @staticmethod
  def from_json(attributes: str) -> Self:
    """ Convert a JSON string to a new instance
    
    Arguments:
      attributes (str): JSON string describing a new instance

    Returns:
      (Self): New instance corresponding to the received data

    Example:
    ```python
    my_coordinate = Coordinate.from_json("{"
      "\"ip\":\"ip\","
      "\"time\":\"1000\","
      "\"latitude\":\"15.2\","
      "\"longitude\":\"-3.1\""
      "}"
    )
    
    assert my_coordinate == Coordinate(
      'ip',
      datetime.fromtimestamp(1000),
      15.2,
      -3.1
    )
    ```
    """
    data: dict[str, str] = load_json(attributes)
    return Coordinate(
      data["ip"],
      datetime.fromtimestamp(int(data["time"])),
      float(data["latitude"]),
      float(data["longitude"])
    )

  def get_latitude_dms(self: Self) -> str:
    """ Returns the latitude in degree-minute-seconds format

    Arguments:
      self (Self): Current instance

    Returns:
      (str): latitude as dd°mm'ss"{N|S}

    Example:
    ```python
    my_coordinate = Coordinate(
      'ip',
      datetime.fromtimestamp(1000),
      15.2,
      -3.1
    )
    assert my_coordinate.get_latitude_dms() == "15°11'59\"N"
    ```
    """
    orientation = 'N' if self.latitude >= 0 else 'S'
    value = abs(self.latitude)
    degree = int(value)
    value = (value - degree) * 60
    minutes = int(value)
    value = (value - minutes) * 60
    seconds = int(value)
    return f'{degree:02d}°{minutes:02d}\'{seconds:02d}\"{orientation}'

  def get_longitude_dms(self: Self) -> str:
    """ Returns the longitude in degree-minute-seconds format

    Arguments:
      self (Self): Current instance

    Returns:
      (str): latitude as dd°mm'ss"{N|S}

    Example:
    ```python
    my_coordinate = Coordinate(
      'ip',
      datetime.fromtimestamp(1000),
      15.2,
      -3.1
    )
    assert my_coordinate.get_longitude_dms() == "03°06'00\"E"
    ```
    """
    orientation = 'E' if self.latitude >= 0 else 'W'
    value = abs(self.longitude)
    degree = int(value)
    value = (value - degree) * 60
    minutes = int(value)
    value = (value - minutes) * 60
    seconds = int(value)
    return f'{degree:02d}°{minutes:02d}\'{seconds:02d}\"{orientation}'

  def __eq__(self: Self, other: Self) -> bool:
    """ Check for equality between two instances

    Attributes:
      self (Self): Current instance
      other (Self): Other instance

    Returns:
      (bool): true iff the two instances have the same data
    """
    return (
      self.ip == other.ip and 
      self.time == other.time and
      self.latitude == other.latitude and
      self.longitude == other.longitude
    )

if __name__ == '__main__':
  pass
