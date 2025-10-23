"""
MongoDB Atlas database connection and collections
"""

import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env from the backend directory
backend_dir = Path(__file__).parent
env_path = backend_dir / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")
load_dotenv(env_path)

# MongoDB Atlas connection string
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "grant-evaluator")
print(f"Loaded MONGODB_URL: {MONGODB_URL[:50]}...") 

# Global client instance
client: AsyncIOMotorClient = None
database = None
evaluations_collection = None
settings_collection = None


async def connect_to_mongo():
    """Initialize MongoDB connection"""
    global client, database, evaluations_collection, settings_collection
    
    # Configure client with timeouts and server selection
    client = AsyncIOMotorClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=5000,  # 5 second timeout
        connectTimeoutMS=10000,  # 10 second connection timeout
        socketTimeoutMS=10000,  # 10 second socket timeout
    )
    
    database = client[DATABASE_NAME]
    evaluations_collection = database["evaluations"]
    settings_collection = database["settings"]
    
    # Test the connection
    try:
        await client.admin.command('ping')
        print(f"Successfully connected to MongoDB Atlas: {DATABASE_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise
    
    # Create indexes
    try:
        await evaluations_collection.create_index("created_at")
        await evaluations_collection.create_index("file_name")
        print("Database indexes created")
    except Exception as e:
        print(f"Warning: Could not create indexes: {e}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database():
    """Dependency for FastAPI routes"""
    return database
