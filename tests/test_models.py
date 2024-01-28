import pytest
from datetime import datetime
from models.coordinate_model import Coordinate

def test_dms():
  my_coordinate = Coordinate(
    'ip',
    datetime.fromtimestamp(1000),
    15.2,
    -3.1
  )
  assert my_coordinate.get_latitude_dms() == "15°11'59\"N"
  assert my_coordinate.get_longitude_dms() == "03°06'00\"E"

def test_json():
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
  assert my_coordinate.to_json() == ("{"
    "\"ip\":\"ip\","
    "\"time\":\"1000.0\","
    "\"latitude\":\"15.2\","
    "\"longitude\":\"-3.1\""
    "}")
