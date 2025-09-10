import os
import json
from starter_demo import (
    Neo4jLocationNetwork,
    load_env_file
)

def load_people_from_json(json_file_path: str):
    """Load people data from a JSON file"""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} people from {json_file_path}")
        return data
        
    except FileNotFoundError:
        print(f"❌ JSON file not found: {json_file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON format: {e}")
        return []
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return []

def validate_people_data(people_data):
    """Validate the structure of people data"""
    required_fields = ['name', 'city', 'country']
    
    for i, person in enumerate(people_data):
        missing_fields = [field for field in required_fields if field not in person]
        if missing_fields:
            print(f"❌ Person {i+1} missing required fields: {missing_fields}")
            return False
        
        # Validate optional fields
        if 'latitude' in person and person['latitude'] is not None:
            try:
                float(person['latitude'])
            except (ValueError, TypeError):
                print(f"❌ Person {person['name']} has invalid latitude: {person['latitude']}")
                return False
        
        if 'longitude' in person and person['longitude'] is not None:
            try:
                float(person['longitude'])
            except (ValueError, TypeError):
                print(f"❌ Person {person['name']} has invalid longitude format.")
                return False
    
    print("✅ All people data validated successfully")
    return True

def bulk_load_people(network, people_data):
    """Bulk load people into the database"""
    print(f"\n🚀 Starting bulk load of {len(people_data)} people...")
    
    success_count = 0
    error_count = 0
    
    for person in people_data:
        try:
            print(f"📝 Processing: {person['name']} from {person['city']}, {person['country']}")
            
            # Extract data with defaults
            name = person['name']
            city = person['city']
            country = person['country']
            latitude = person.get('latitude')
            longitude = person.get('longitude')
            friends_data = person.get('friends', [])
            
            # Add person with relationships
            network.add_person_with_relationships(
                name=name,
                home_city=city,
                country=country,
                friends_data=friends_data,
                latitude=latitude,
                longitude=longitude
            )
            
            success_count += 1
            print(f"✅ Successfully added {name}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Failed to add {person.get('name', 'Unknown')}: {e}")
            continue
    
    print(f"\n📊 Bulk load completed:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📝 Total: {len(people_data)}")

def main():
    """Main function to load and process people data"""
    # Load environment
    load_env_file('.noe4j.env')
    
    # Get connection details
    connection_uri = os.getenv('CONNECTION_URI')
    admin_password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('USERNAME', 'neo4j')
    neo4j_db = os.getenv('NEO4J_DB')
    
    if not connection_uri or not admin_password or not neo4j_db:
        raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")
    
    # JSON file path - you can change this or pass as argument
    json_file_path = "700_people_data.json"
    
    print("🚀 Neo4j Location Network - Bulk Data Loader")
    print("="*60)
    
    # Load people data from JSON
    people_data = load_people_from_json(json_file_path)
    
    if not people_data:
        print("❌ No data to process. Exiting.")
        return
    
    # Validate data structure
    if not validate_people_data(people_data):
        print("❌ Data validation failed. Exiting.")
        return
    
    # Process data with database
    try:
        with Neo4jLocationNetwork(connection_uri, username, admin_password, neo4j_db) as network:
            print(f"\n🔗 Connecting to database: {neo4j_db}")
            
            # Setup constraints if needed
            network.setup_constraints()
            
            # Bulk load people
            bulk_load_people(network, people_data)
            
            # Show final summary
            print("\n" + "="*50)
            network.get_network_summary()
            
    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        raise

if __name__ == "__main__":
    main()