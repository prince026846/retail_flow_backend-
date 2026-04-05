from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client : AsyncIOMotorClient = None
    db = None

db_manager = Database()

async def connect_to_mongo():
    global db_manager
    import os
    
    # Check if we're in production environment
    is_production = os.getenv("RAILWAY_ENVIRONMENT") == "production" or os.getenv("ENVIRONMENT") == "production" or os.getenv("RENDER") == "true"
    
    # For both development and production, try Atlas first
    try:
        mongo_url = settings.MONGO_URL
        print(f"Attempting Atlas connection: {mongo_url[:50]}...")
        
        # Atlas connection with proper SSL settings for production compatibility
        db_manager.client = AsyncIOMotorClient(
            mongo_url,
            serverSelectionTimeoutMS=30000,
            socketTimeoutMS=30000,
            connectTimeoutMS=30000,
            retryWrites=True,
            retryReads=True,
            w=1,
            maxPoolSize=50,
            minPoolSize=5,
            # Use MongoDB Atlas's recommended SSL settings
            tls=True,
            tlsAllowInvalidCertificates=False,
            tlsAllowInvalidHostnames=False
        )
        
        # Test connection
        db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.DATABASE_NAME]
        print(f"[OK] Connected to Mongo Atlas: {settings.DATABASE_NAME}")
        
        # Test actual database operation to verify write access
        from datetime import datetime
        test_doc = {
            "connection_test": True, 
            "timestamp": datetime.now().isoformat(), 
            "env": "production" if is_production else "development"
        }
        result = await db_manager.db["connection_test"].insert_one(test_doc)
        await db_manager.db["connection_test"].delete_one({"_id": result.inserted_id})
        print("[OK] Atlas database operation test: SUCCESS")
        return
        
    except Exception as e:
        print(f"[FAIL] Atlas connection failed: {e}")
        
        # Only fallback to local if NOT in production
        if not is_production:
            print("[retry] Falling back to local MongoDB for development...")
            try:
                local_url = "mongodb://localhost:27017"
                db_manager.client = AsyncIOMotorClient(
                    local_url,
                    serverSelectionTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    connectTimeoutMS=5000
                )
                db_manager.db = db_manager.client["Retail_Flow_Dev"]
                print("[OK] Connected to Local MongoDB (fallback): Retail_Flow_Dev")
            except Exception as local_error:
                print(f"[FAIL] Local MongoDB fallback failed: {local_error}")
                raise Exception(f"[FAIL] All database connection attempts failed. Atlas error: {e}, Local error: {local_error}")
        else:
            # In production, we don't fallback to local. Re-raise Atlas error.
            raise Exception(f"[FAIL] Production Atlas connection failed: {e}")

async def close_mongo_connection():
    if db_manager.client:
        db_manager.client.close()
        print("MongoDB connection closed")

async def connect():
    """Main connect method that tries both Atlas and local"""
    await connect_to_mongo()
