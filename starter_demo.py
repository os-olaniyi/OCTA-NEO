import os
from neo4j import GraphDatabase
from neo4j.exceptions import AuthError, ServiceUnavailable, ConstraintError
from typing import List, Dict, Optional, Tuple

class Neo4jLocationNetwork:
    """ACID-compliant location-based social network manager"""
    
    def __init__(self, connection_uri: str, username: str, password: str, database: str):
        self.driver = GraphDatabase.driver(connection_uri, auth=(username, password))
        self.database = database
        self.session = None
    
    def __enter__(self):
        self.session = self.driver.session(database=self.database)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()
        if self.driver:
            self.driver.close()
    
    def setup_constraints(self):
        """Set up database constraints for data integrity"""
        with self.session.begin_transaction() as tx:
            try:
                # Create unique constraints
                tx.run("CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE")
                tx.run("CREATE CONSTRAINT city_name_unique IF NOT EXISTS FOR (c:City) REQUIRE c.name IS UNIQUE")
                
                # Create indexes for performance
                tx.run("CREATE INDEX person_name_index IF NOT EXISTS FOR (p:Person) ON (p.name)")
                tx.run("CREATE INDEX city_name_index IF NOT EXISTS FOR (c:City) ON (c.name)")
                
                tx.commit()
                print("✅ Database constraints and indexes created successfully")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Failed to setup constraints: {e}")
                raise
    
    def create_city_safe(self, city_name: str, country: str, latitude: Optional[float] = None, longitude: Optional[float] = None):
        """Create a City node with duplicate prevention using MERGE"""
        self.session.run("""
            MERGE (c:City {name: $city_name})
            ON CREATE SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
            ON MATCH SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
            """, city_name=city_name, country=country, latitude=latitude, longitude=longitude)
    
    def create_person_safe(self, name: str, home_city: str, home_country: str):
        """Create a Person node with duplicate prevention using MERGE"""
        self.session.run("""
            MERGE (p:Person {name: $name})
            ON CREATE SET p.home_city = $home_city, p.home_country = $home_country
            ON MATCH SET p.home_city = $home_city, p.home_country = $home_country
            """, name=name, home_city=home_city, home_country=home_country)
    
    def create_lives_in_relationship(self, person_name: str, city_name: str):
        """Create LIVES_IN relationship between Person and City"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (c:City {name: $city_name})
            MERGE (p)-[:LIVES_IN]->(c)
            """, person_name=person_name, city_name=city_name)
    
    def create_met_in_relationship(self, person1_name: str, person2_name: str, meeting_city: str):
        """Create MET_IN relationship between two people in a specific city"""
        # Ensure meeting city exists
        self.create_city_safe(meeting_city, "Unknown")
        
        self.session.run("""
            MATCH (p1:Person {name: $person1_name})
            MATCH (p2:Person {name: $person2_name})
            MATCH (c:City {name: $meeting_city})
            MERGE (p1)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p2)
            MERGE (p2)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p1)
            """, person1_name=person1_name, person2_name=person2_name, meeting_city=meeting_city)
    
    def create_nearby_relationship(self, person1_name: str, person2_name: str):
        """Create NEARBY relationship if people live in same city"""
        self.session.run("""
            MATCH (p1:Person {name: $person1_name})
            MATCH (p2:Person {name: $person2_name})
            WHERE p1.home_city = p2.home_city AND p1.name < p2.name
            MERGE (p1)-[:NEARBY]->(p2)
            """, person1_name=person1_name, person2_name=person2_name)
    
    def add_person_with_relationships(self, name: str, home_city: str, country: str, 
                                    friends_data: List[Dict] = None, latitude: float = None, longitude: float = None):
        """Add person and relationships in a single ACID transaction"""
        with self.session.begin_transaction() as tx:
            try:
                # Create city first
                tx.run("""
                    MERGE (c:City {name: $city_name})
                    ON CREATE SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
                    ON MATCH SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
                    """, city_name=home_city, country=country, latitude=latitude, longitude=longitude)
                
                # Create person
                tx.run("""
                    MERGE (p:Person {name: $name})
                    ON CREATE SET p.home_city = $home_city, p.home_country = $home_country
                    ON MATCH SET p.home_city = $home_city, p.home_country = $home_country
                    """, name=name, home_city=home_city, home_country=country)
                
                # Create LIVES_IN relationship
                tx.run("""
                    MATCH (p:Person {name: $person_name})
                    MATCH (c:City {name: $city_name})
                    MERGE (p)-[:LIVES_IN]->(c)
                    """, person_name=name, city_name=home_city)
                
                # Add friend relationships if provided
                if friends_data:
                    for friend in friends_data:
                        # Ensure meeting city exists
                        tx.run("""
                            MERGE (c:City {name: $city_name})
                            """, city_name=friend['meeting_city'])
                        
                        # Create MET_IN relationship
                        tx.run("""
                            MATCH (p1:Person {name: $person1_name})
                            MATCH (p2:Person {name: $person2_name})
                            MATCH (c:City {name: $meeting_city})
                            MERGE (p1)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p2)
                            MERGE (p2)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p1)
                            """, person1_name=name, person2_name=friend['name'], meeting_city=friend['meeting_city'])
                
                tx.commit()
                print(f"✅ Successfully added {name} from {home_city}, {country}")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Error adding {name}: {e}")
                raise
    
    def add_multiple_people(self, people_data: List[Dict]):
        """Add multiple people from a list of dictionaries"""
        for person in people_data:
            self.add_person_with_relationships(
                person['name'],
                person['city'],
                person['country'],
                person.get('friends', []),
                person.get('latitude'),
                person.get('longitude')
            )
    
    def create_sample_network(self):
        """Create the complete sample location-based social network"""
        with self.session.begin_transaction() as tx:
            try:
                # Create cities
                cities = [
                    ("Kansas City", "USA", 39.0997, -94.5786),
                    ("Stockholm", "Sweden", 59.3293, 18.0686),
                    ("Toronto", "Canada", 43.6532, -79.3832),
                    ("New York", "USA", 40.7128, -74.0060),
                    ("London", "UK", 51.5074, -0.1278)
                ]
                
                for city_name, country, lat, lon in cities:
                    # Use tx.run instead of self.session.run inside transaction
                    tx.run("""
                        MERGE (c:City {name: $city_name})
                        ON CREATE SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
                        ON MATCH SET c.country = $country, c.latitude = $latitude, c.longitude = $longitude
                        """, city_name=city_name, country=country, latitude=lat, longitude=lon)
                
                # Create people with relationships
                people_data = [
                    {
                        "name": "Roberts",
                        "city": "Kansas City",
                        "country": "USA",
                        "friends": [
                            {"name": "Callahan", "meeting_city": "Toronto"},
                            {"name": "Johnson", "meeting_city": "New York"}
                        ]
                    },
                    {
                        "name": "Callahan",
                        "city": "Stockholm",
                        "country": "Sweden",
                        "friends": [
                            {"name": "Smith", "meeting_city": "London"}
                        ]
                    },
                    {
                        "name": "Johnson",
                        "city": "New York",
                        "country": "USA"
                    },
                    {
                        "name": "Smith",
                        "city": "London",
                        "country": "UK"
                    },
                    {
                        "name": "Davis",
                        "city": "Kansas City",
                        "country": "USA"
                    }
                ]
                
                for person in people_data:
                    # Create person
                    tx.run("""
                        MERGE (p:Person {name: $name})
                        ON CREATE SET p.home_city = $home_city, p.home_country = $home_country
                        ON MATCH SET p.home_city = $home_city, p.home_country = $home_country
                        """, name=person['name'], home_city=person['city'], home_country=person['country'])
                    
                    # Create LIVES_IN relationship
                    tx.run("""
                        MATCH (p:Person {name: $person_name})
                        MATCH (c:City {name: $city_name})
                        MERGE (p)-[:LIVES_IN]->(c)
                        """, person_name=person['name'], city_name=person['city'])
                    
                    # Create friend relationships if provided
                    if 'friends' in person:
                        for friend in person['friends']:
                            # Ensure meeting city exists
                            tx.run("""
                                MERGE (c:City {name: $city_name})
                                """, city_name=friend['meeting_city'])
                            
                            # Create MET_IN relationship
                            tx.run("""
                                MATCH (p1:Person {name: $person1_name})
                                MATCH (p2:Person {name: $person2_name})
                                MATCH (c:City {name: $meeting_city})
                                MERGE (p1)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p2)
                                MERGE (p2)-[:MET_IN {city: $meeting_city, timestamp: datetime()}]->(p1)
                                """, person1_name=person['name'], person2_name=friend['name'], meeting_city=friend['meeting_city'])
                
                # Create nearby relationships (people in same city)
                tx.run("""
                    MATCH (p1:Person {name: $person1_name})
                    MATCH (p2:Person {name: $person2_name})
                    WHERE p1.home_city = p2.home_city AND p1.name < p2.name
                    MERGE (p1)-[:NEARBY]->(p2)
                    """, person1_name="Roberts", person2_name="Davis")
                
                tx.commit()
                print("✅ Sample network created successfully!")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Failed to create sample network: {e}")
                raise
    
    def query_people_by_city(self, city_name: str):
        """Find all people who live in a specific city"""
        result = self.session.run("""
            MATCH (p:Person)-[:LIVES_IN]->(c:City {name: $city_name})
            RETURN p.name as name, p.home_city as city
            """, city_name=city_name)
        
        print(f"\n📍 People living in {city_name}:")
        people = []
        for record in result:
            people.append(record['name'])
            print(f"  - {record['name']}")
        
        if not people:
            print(f"  No people found in {city_name}")
        
        return people
    
    def query_meeting_locations(self, person_name: str):
        """Find where a person met other people"""
        result = self.session.run("""
            MATCH (p:Person {name: $person_name})-[r:MET_IN]->(other:Person)
            RETURN other.name as other_person, r.city as meeting_city
            """, person_name=person_name)
        
        print(f"\n🤝 Where {person_name} met people:")
        meetings = []
        for record in result:
            meetings.append({"person": record['other_person'], "city": record['meeting_city']})
            print(f"  - Met {record['other_person']} in {record['meeting_city']}")
        
        if not meetings:
            print(f"  No meetings found for {person_name}")
        
        return meetings
    
    def query_nearby_people(self, person_name: str):
        """Find people who live near a specific person"""
        result = self.session.run("""
            MATCH (p:Person {name: $person_name})-[:NEARBY]-(nearby:Person)
            RETURN nearby.name as nearby_person, nearby.home_city as city
            """, person_name=person_name)
        
        print(f"\n🏘️ People living near {person_name}:")
        nearby = []
        for record in result:
            nearby.append({"name": record['nearby_person'], "city": record['city']})
            print(f"  - {record['nearby_person']} in {record['city']}")
        
        if not nearby:
            print(f"  No nearby people found for {person_name}")
        
        return nearby
    
    def get_network_summary(self):
        """Get a complete summary of the network"""
        print("\n" + "="*50)
        print("🌐 NETWORK SUMMARY")
        print("="*50)
        
        # Count nodes
        node_count = self.session.run("MATCH (n) RETURN count(n) as total").single()['total']
        person_count = self.session.run("MATCH (p:Person) RETURN count(p) as total").single()['total']
        city_count = self.session.run("MATCH (c:City) RETURN count(c) as total").single()['total']
        
        print(f"📊 Total nodes: {node_count}")
        print(f"👥 People: {person_count}")
        print(f"🏙️ Cities: {city_count}")
        
        # Count relationships
        rel_count = self.session.run("MATCH ()-[r]->() RETURN count(r) as total").single()['total']
        print(f"🔗 Relationships: {rel_count}")
        
        # Show all people
        print(f"\n👥 PEOPLE IN NETWORK:")
        people = self.session.run("MATCH (p:Person) RETURN p.name as name, p.home_city as city, p.home_country as country")
        for record in people:
            print(f"  - {record['name']} (lives in {record['city']}, {record['country']})")
        
        # Show all cities
        print(f"\n🏙️ CITIES IN NETWORK:")
        cities = self.session.run("MATCH (c:City) RETURN c.name as name, c.country as country")
        for record in cities:
            print(f"  - {record['name']}, {record['country']}")
        
        print("="*50)
    
    def cleanup_database(self):
        """Clean up all data from the database"""
        with self.session.begin_transaction() as tx:
            try:
                # Delete all relationships first
                tx.run("MATCH ()-[r]-() DELETE r")
                # Delete all nodes
                tx.run("MATCH (n) DELETE n")
                tx.commit()
                print("🧹 Database cleaned successfully!")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Failed to cleanup database: {e}")
                raise

# Load environment variables
def load_env_file(file_path: str):
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"')

# Main execution
if __name__ == "__main__":
    # Load environment
    load_env_file('.noe4j.env')
    
    # Get connection details
    connection_uri = os.getenv('CONNECTION_URI')
    admin_password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('USERNAME')
    neo4j_db = os.getenv('NEO4J_DB')
    
    if not connection_uri or not admin_password or not neo4j_db:
        raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")
    
    print("🚀 Starting Neo4j Location Network Manager...")
    
    # Use context manager for automatic cleanup
    with Neo4jLocationNetwork(connection_uri, username, admin_password, neo4j_db) as network:
        try:
            # Setup database integrity
            network.setup_constraints()
            
            # Create sample network
            network.create_sample_network()
            
            # Query examples
            network.query_people_by_city("Kansas City")
            network.query_meeting_locations("Roberts")
            network.query_nearby_people("Roberts")
            
            # Show complete summary
            network.get_network_summary()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
