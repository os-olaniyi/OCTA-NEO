#!/usr/bin/env python3
"""
Relationship Builder for Neo4j Location Network
Creates connections between people who are already in the database
"""

import os
from starter_demo import Neo4jLocationNetwork, load_env_file

# def load_env_file(file_path: str):
#     with open(file_path, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if line and not line.startswith('#') and '=' in line:
#                 key, value = line.split('=', 1)
#                 os.environ[key.strip()] = value.strip().strip('"')

def get_existing_people(network):
    """Get list of all existing people in the database"""
    result = network.session.run("MATCH (p:Person) RETURN p.name as name ORDER BY p.name")
    return [record['name'] for record in result]

def build_relationships_between_existing_people(network, relationship_data):
    """Build relationships between people who already exist in the database"""
    print(f"🔗 Building {len(relationship_data)} relationships...")
    
    success_count = 0
    error_count = 0
    
    for relationship in relationship_data:
        try:
            person1 = relationship['person1']
            person2 = relationship['person2']
            meeting_city = relationship['meeting_city']
            
            print(f"📝 Creating: {person1} ←→ {person2} in {meeting_city}")
            
            # Create the relationship
            network.create_met_in_relationship(person1, person2, meeting_city)
            
            success_count += 1
            print(f"✅ Successfully connected {person1} and {person2}")
            
        except Exception as e:
            error_count += 1
            print(f"❌ Failed to connect {person1} and {person2}: {e}")
            continue
    
    print(f"\n📊 Relationship building completed:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📝 Total: {len(relationship_data)}")

def main():
    """Main function to build relationships between existing people"""
    # Load environment
    load_env_file('.noe4j.env')
    
    # Get connection details
    connection_uri = os.getenv('CONNECTION_URI')
    admin_password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('USERNAME', 'neo4j')
    neo4j_db = os.getenv('NEO4J_DB')
    
    if not connection_uri or not admin_password or not neo4j_db:
        raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")
    
    print("🔗 Neo4j Location Network - Relationship Builder")
    print("=" * 60)
    
    # Define relationships to create
    # Format: person1, person2, meeting_city
    relationships_to_create = [
        # Connect existing sample people with new people
        {"person1": "Roberts", "person2": "Wilson", "meeting_city": "Berlin"},
        {"person1": "Callahan", "person2": "Brown", "meeting_city": "Paris"},
        {"person1": "Johnson", "person2": "Taylor", "meeting_city": "Tokyo"},
        {"person1": "Smith", "person2": "Anderson", "meeting_city": "London"},
        {"person1": "Davis", "person2": "Garcia", "meeting_city": "Madrid"},
        
        # Connect new people with each other
        {"person1": "Wilson", "person2": "Brown", "meeting_city": "Paris"},
        {"person1": "Taylor", "person2": "Anderson", "meeting_city": "Sydney"},
        {"person1": "Garcia", "person2": "Chen", "meeting_city": "Shanghai"},
        {"person1": "Patel", "person2": "Silva", "meeting_city": "São Paulo"},
        
        # Cross-continental connections
        {"person1": "Roberts", "person2": "Chen", "meeting_city": "Tokyo"},
        {"person1": "Callahan", "person2": "Patel", "meeting_city": "Mumbai"},
        {"person1": "Johnson", "person2": "Silva", "meeting_city": "Rio de Janeiro"},
        
        # European connections
        {"person1": "Wilson", "person2": "Garcia", "meeting_city": "Madrid"},
        {"person1": "Brown", "person2": "Callahan", "meeting_city": "Stockholm"},
        {"person1": "Smith", "person2": "Wilson", "meeting_city": "Berlin"},
        
        # Asian-Pacific connections
        {"person1": "Taylor", "person2": "Chen", "meeting_city": "Tokyo"},
        {"person1": "Anderson", "person2": "Patel", "meeting_city": "Mumbai"},
        {"person1": "Chen", "person2": "Taylor", "meeting_city": "Shanghai"},
        
        # Americas connections
        {"person1": "Roberts", "person2": "Silva", "meeting_city": "São Paulo"},
        {"person1": "Johnson", "person2": "Garcia", "meeting_city": "Mexico City"},
        {"person1": "Davis", "person2": "Patel", "meeting_city": "Toronto"}
    ]
    
    try:
        with Neo4jLocationNetwork(connection_uri, username, admin_password, neo4j_db) as network:
            print(f"🔗 Connected to database: {neo4j_db}")
            
            # Show existing people
            existing_people = get_existing_people(network)
            print(f"\n👥 Found {len(existing_people)} people in database")
            
            # Show first 10 people as examples
            print("📋 Sample people in database:")
            for i, person in enumerate(existing_people[:10], 1):
                print(f"  {i}. {person}")
            if len(existing_people) > 10:
                print(f"  ... and {len(existing_people) - 10} more")
            
            # Build the relationships
            build_relationships_between_existing_people(network, relationships_to_create)
            
            # Show final summary
            print("\n" + "=" * 50)
            network.get_network_summary()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
