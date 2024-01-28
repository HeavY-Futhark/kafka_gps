from fastapi import FastAPI
from typing import Type

def create_api(DataBaseClass: Type) -> FastAPI:
    """ Create the API
    Contains the requests:
    - GET /all_coordinates: Read all the coordinates and returns a map
    id/coordinate in the "data" field,
    - GET /coordinate_id/{id}: Read the coordinates for the given id and
    returns it in the "data" field.
    - GET /latest_coordinates: Read the latest coordinates for each ip
    
    Parameters:
        DataBaseClass (Class): Class that will be used to get the data
        Has to contain the following methods:
        - readAll(): Returns a map "id: coordinate" of all the data,
        - readOne(int): Returns the coordinate for the given id.

    Returns:
        (FastAPI): API with requests to get the coordinates of the database.
    """
    bdd = DataBaseClass()
    app = FastAPI()

    @app.get("/all_coordinates")
    def get_all_coordinates() -> dict[str,any]:
        """ Read all the coordinates and returns a map id/coordinate in the
        "data" field

        Returns:
            (dict[str,any]): "data" as key and array of coordinates as
            value
        """
        return {"data": bdd.readAll()}

    @app.get("/coordinate_id/{id}")
    def get_coordinate_id(id_: int):
        """ Read the coordinates for the given id and returns it in the "data"
        field

        Parameters:
            id (int): Id of the wanted coordinate

        Returns:
            (dict[str,any]): Confirms the id and send "data" as key and the
            coordinate as a value
        """
        return {"id": id_, "data": bdd.readOne(id_)}

    @app.get("/latest_coordinates")
    def get_latest_coordinates() -> dict[str, any]:
        """ Reads the latest coordinates for each ip address and returns it

        Returns:
            (dict[str, any]): "data" and array of latest coordinates as value
        """
        data = bdd.readAll()
        data_map = {}
        for line in data.values():
            if line.ip not in data_map:
                data_map[line.ip] = []
            data_map[line.ip].append(line)
        data_latest = [
            max(
                data_map[value_ip],
                key = lambda x:x.time
            )
            for value_ip in data_map.keys()
        ]
        return data_latest

    return app
