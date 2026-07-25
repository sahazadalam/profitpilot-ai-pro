import os
import sys
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import time

def test_connection():
    """Test MongoDB connection using synchronous pymongo."""
    load_dotenv()
    
    mongodb_url = os.getenv('MONGODB_URL')
    db_name = os.getenv('MONGODB_DB_NAME', 'profitpilot_db')
    
    print("=" * 60)
    print("🔍 Testing MongoDB Connection")
    print("=" * 60)
    print(f"📡 URL: {mongodb_url}")
    print(f"📚 Database: {db_name}")
    print("-" * 60)
    
    if not mongodb_url:
        print("❌ MONGODB_URL not found in .env file!")
        print("Please add MONGODB_URL to your .env file")
        return False
    
    try:
        # Connect to MongoDB with timeout
        print("⏳ Connecting...")
        client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=10000,  # 10 second timeout
            socketTimeoutMS=10000,
            connectTimeoutMS=10000,
        )
        
        # Ping to test connection
        print("⏳ Pinging server...")
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        # Get database
        db = client[db_name]
        
        # List collections
        collections = db.list_collection_names()
        print(f"📚 Collections found: {collections if collections else 'None'}")
        
        # Check if users collection exists
        if 'users' in collections:
            users_count = db.users.count_documents({})
            print(f"👥 Users in database: {users_count}")
        else:
            print("ℹ️ Users collection doesn't exist yet (this is normal for new databases)")
        
        print("-" * 60)
        print("✅ MongoDB connection test PASSED!")
        client.close()
        return True
        
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"❌ Server selection timeout: {str(e)}")
        print("\n⚠️ Possible issues:")
        print("1. Check if MongoDB Atlas IP whitelist includes your IP")
        print("2. Check if the connection string is correct")
        print("3. Check if username/password are correct")
        print("4. Check if network allows connection to MongoDB Atlas")
        return False
        
    except pymongo.errors.OperationFailure as e:
        print(f"❌ Authentication failed: {str(e)}")
        print("\n⚠️ Possible issues:")
        print("1. Check username and password")
        print("2. Check if the database user exists")
        return False
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_connection()
