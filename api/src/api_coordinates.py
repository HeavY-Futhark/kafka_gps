from fastapi import FastAPI
from typing import Type

def create_api(DataBaseClass: Type) -> FastAPI:
    """ Create the API
    Contains the requests:
    - GET /all_coordinates: Read all the coordinates and returns a map
    id/coordinate in the "data" field,
    - GET /coordinate_ip/{ip}: Read all the coordinates for the given ip and
    returns it as a map in the "data" field,
    - GET /coordinate_id/{id}: Read the coordinates for the given id and
    returns it in the "data" field.
    
    Parameters:
        DataBaseClass (Class): Class that will be used to get the data
        Has to contain the following methods:
        - read_all(): Returns a map "id: coordinate" of all the data,
        - read_ip(str): Returns a map "id: coordinate" for the given ip
        address,
        - read_id(str): Returns the coordinate for the given id.

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
        return {"data": bdd.read_all()}

    @app.get("/coordinate_ip/{ip}")
    def get_coordinate_ip(ip: str):
        """ Read all the coordinates for the given ip and returns it as a map
        in the "data" field

        Parameters:
            ip (str): Ip of the device whose coordinates are wanted

        Returns:
            (dict[str,any]): Confirms the ip and send "data" as key and array
            of coordinates as value
        """
        return {"ip": ip, "data": bdd.read_ip(ip)}

    @app.get("/coordinate_id/{id}")
    def get_coordinate_id(id_: str):
        """ Read the coordinates for the given id and returns it in the "data"
        field

        Parameters:
            id (str): Id of the wanted coordinate

        Returns:
            (dict[str,any]): Confirms the id and send "data" as key and the
            coordinate as a value
        """
        return {"id": id_, "data": bdd.read_id(id_)}

    return app
