import os
from neo4j import GraphDatabase

# Load environment variables from .noe4j.env file
def load_env_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"')

# Load the .noe4j.env file
load_env_file(".noe4j.env")

# Get connection details from environment variables
CONNECTION_URI = os.getenv('CONNECTION_URI')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
NEO4J_DB = os.getenv('NEO4J_DB')
DB_USERNAME = os.getenv('USERNAME')

# Check if required environment variables are set
if not CONNECTION_URI or not ADMIN_PASSWORD:
    raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")

driver = GraphDatabase.driver(
    CONNECTION_URI,
    auth=(DB_USERNAME, ADMIN_PASSWORD)
)

session = driver.session(database = NEO4J_DB)

result = session.run("MATCH (n) RETURN n")
print(result.data())

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Hello, Neo4j!' AS msg")
        for record in result:
            print(record["msg"])

test_connection()
driver.close()