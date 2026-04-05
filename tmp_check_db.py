import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient

async def check_db():
    print("Checking products in DB...")
    # Get MONGODB_URL from env or default
    # Assuming standard localhost for now based on context
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongodb_url)
    db = client["retailflow"]
    
    # Check products
    products = await db["products"].find({}, {"name": 1, "stock": 1}).to_list(100)
    print(f"Total products: {len(products)}")
    for p in products:
        print(f" - {p.get('name')} (Stock: {p.get('stock')})")
        
    # Check orders
    orders_count = await db["orders"].count_documents({})
    print(f"Total orders: {orders_count}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_db())
