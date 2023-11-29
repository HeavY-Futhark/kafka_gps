from fastapi import FastAPI

def create_api(DataBaseClass: Class) -> FastAPI:
    """ Create the API
    Contains
    
    Parameters:
        DataBaseClass (Class): Class that will be used to get the data
        Has to contain the following methods:
        - read_all(),
        - read_ip(),
        - read_id().

    Returns:
        (FastAPI): API with requests to get the coordinates of the database.
    """
    bdd = DataBaseClass()
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"message": "Hello, FastAPI"}

    @app.get("/all_coordinates/")
    def get_all_coordinates():
        return bdd.read_all()

    @app.get("/coordinate_ip/{ip_address}")
    def get_coordinate_ip(ip_address: str):
        return {"ip_address": ip_address, "coordinates": bdd.read_ip(ip_address)}

    return app
