import pymongo
import certifi
import ssl

print(f"Certifi version: {certifi.__version__}")
print(f"PyMongo version: {pymongo.__version__}")
print(f"SSL version: {ssl.OPENSSL_VERSION}")

uri = "mongodb+srv://tbartfalvi:4B5GsC2X5IhYY0Qx@airondb.mxhvpku.mongodb.net/?retryWrites=true&w=majority&appName=AIronDB"
print("Connecting to MongoDB...")

# Try with tlsInsecure=true
try:
    print("\nAttempt 1: Using tlsInsecure=true")
    client = pymongo.MongoClient(
        uri + "&tlsInsecure=true", 
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    print("Connected with tlsInsecure=true")
    
    # Test the connection
    db_names = client.list_database_names()
    print(f"Available databases: {db_names}")
    client.close()
except Exception as e:
    print(f"Error with tlsInsecure=true: {e}")

# Try with tlsAllowInvalidCertificates=true
try:
    print("\nAttempt 2: Using tlsAllowInvalidCertificates=true")
    client = pymongo.MongoClient(
        uri, 
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    print("Connected with tlsAllowInvalidCertificates=true")
    
    # Test the connection
    db_names = client.list_database_names()
    print(f"Available databases: {db_names}")
    client.close()
except Exception as e:
    print(f"Error with tlsAllowInvalidCertificates=true: {e}")

# Try with specific SSL context
try:
    print("\nAttempt 3: Using custom SSL context")
    # Create a custom SSL context
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    client = pymongo.MongoClient(
        uri, 
        ssl_cert_reqs=ssl.CERT_NONE,
        ssl=True,
        serverSelectionTimeoutMS=5000
    )
    print("Connected with custom SSL context")
    
    # Test the connection
    db_names = client.list_database_names()
    print(f"Available databases: {db_names}")
    client.close()
except Exception as e:
    print(f"Error with custom SSL context: {e}")

# Try direct connection (non-SRV)
try:
    print("\nAttempt 4: Using direct connection")
    # Note: You need to change the ports and servers according to your MongoDB Atlas cluster
    direct_uri = "mongodb://tbartfalvi:4B5GsC2X5IhYY0Qx@ac-j7x6h9l-shard-00-00.mxhvpku.mongodb.net:27017,ac-j7x6h9l-shard-00-01.mxhvpku.mongodb.net:27017,ac-j7x6h9l-shard-00-02.mxhvpku.mongodb.net:27017/airon_db?replicaSet=atlas-8vv8dj-shard-0&ssl=true&authSource=admin"
    
    client = pymongo.MongoClient(
        direct_uri, 
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
        serverSelectionTimeoutMS=5000
    )
    print("Connected with direct connection")
    
    # Test the connection
    db_names = client.list_database_names()
    print(f"Available databases: {db_names}")
    client.close()
except Exception as e:
    print(f"Error with direct connection: {e}")
