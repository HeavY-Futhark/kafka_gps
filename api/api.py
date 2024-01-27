from src.api_coordinates import create_api
from services.coordinate_services import DataBaseManager

if __name__ == "__main__":
    import uvicorn
    app = create_api(DataBaseManager)
    uvicorn.run(app, host="0.0.0.0", port=80)
