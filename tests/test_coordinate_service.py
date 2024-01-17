from datetime import datetime
from models.coordinate_model import Coordinate
from services.coordinate_service import DatabaseManager

coord_entry = Coordinate(
    latitude=12.987, longitude=45.678, time=datetime.now(), ip="127.0.0.1"
)

def test_insert():
    db_manager = DatabaseManager()
    res = db_manager.insert_data(coord_entry)
    assert res

def test_read_all():
    db_manager = DatabaseManager()
    db_manager.insert_data(coord_entry)
    all_data = db_manager.read_all()
    assert len(all_data) > 0

def test_read_one():
    db_manager = DatabaseManager()
    
    db_manager.insert_data(coord_entry)
    db_manager.insert_data(coord_entry)
    insert_id = db_manager.insert_data(coord_entry)
    db_manager.insert_data(coord_entry)
    db_manager.insert_data(coord_entry)
    all_data = db_manager.readOne(insert_id)
    
    assert insert_id != -1
    assert all_data == coord_entry
    
