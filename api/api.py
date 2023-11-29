import os
import sys
project_directory = os.path.abspath('.')
sys.path.append(project_directory)
from src.api_coordinates import create_api
from services.coordinate_services import DataBaseManager

if __name__ == "__main__":
    import uvicorn
    app = create_api(DataBaseManager)
    uvicorn.run(app, host="127.0.0.1", port=8000)
