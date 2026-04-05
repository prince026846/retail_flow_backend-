import asyncio
import os
from pymongo import MongoClient

async def seed_barcodes():
    # Use the connection string from your .env
    MONGO_URL = "mongodb+srv://princedi502:Prince123@cluster0.hbe3i.mongodb.net/retailflow?retryWrites=true&w=majority"
    
    print(f"🚀 Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URL)
    db = client.get_database("retailflow")
    products_col = db.get_collection("products")
    
    # Products from user's list
    new_products = [
        {
            "name": "27-inch Monitor",
            "category": "Electronics",
            "price": 399.99,
            "stock": 63,
            "barcode": "123456789004",
            "low_stock_threshold": 8,
            "supplier": "Nexus Global Logistics",
            "cost_price": 280.00
        },
        {
            "name": "Wireless Mouse",
            "category": "Electronics",
            "price": 29.99,
            "stock": 10,
            "barcode": "123456789002",
            "low_stock_threshold": 25,
            "supplier": "Nexus Global Logistics",
            "cost_price": 12.00
        },
        {
            "name": "Mechanical Keyboard",
            "category": "Electronics",
            "price": 89.99,
            "stock": 32,
            "barcode": "123456789003",
            "low_stock_threshold": 15,
            "supplier": "Nexus Global Logistics",
            "cost_price": 45.00
        },
        {
            "name": "Office Paper A4",
            "category": "Office Supplies",
            "price": 12.99,
            "stock": 124,
            "barcode": "123456789005",
            "low_stock_threshold": 50,
            "supplier": "Nexus Global Logistics",
            "cost_price": 5.00
        }
    ]
    
    print(f"📦 Seeding {len(new_products)} products...")
    
    for product in new_products:
        # Check if already exists by barcode
        existing = products_col.find_one({"barcode": product["barcode"]})
        if existing:
            print(f"⚠️ Updating existing product: {product['name']} ({product['barcode']})")
            products_col.update_one({"barcode": product["barcode"]}, {"$set": product})
        else:
            print(f"✅ Inserting new product: {product['name']}")
            products_col.insert_one(product)
            
    print(f"🎉 Barcodes Successfully Seeded!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed_barcodes())
