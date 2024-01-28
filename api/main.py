from src.api_coordinates import create_api
from services.coordinate_service import DatabaseManager
from fastapi.middleware.cors import CORSMiddleware

app = create_api(DatabaseManager)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
