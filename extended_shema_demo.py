#!/usr/bin/env python3
"""
Extended Schema Demo for Neo4j Location Network
Shows how to add new node types and relationship types
"""

import os
from datetime import datetime, date
from starter_demo import (
    Neo4jLocationNetwork,
    load_env_file
)

class ExtendedNeo4jNetwork(Neo4jLocationNetwork):
    """Extended network with additional node types and relationships"""
    
    def setup_extended_constraints(self):
        """Set up constraints for extended schema"""
        with self.session.begin_transaction() as tx:
            try:
                # Company constraints
                tx.run("CREATE CONSTRAINT company_name_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.name IS UNIQUE")
                tx.run("CREATE INDEX company_industry_index IF NOT EXISTS FOR (c:Company) ON (c.industry)")
                
                # Event constraints
                tx.run("CREATE CONSTRAINT event_name_unique IF NOT EXISTS FOR (e:Event) REQUIRE e.name IS UNIQUE")
                tx.run("CREATE INDEX event_type_index IF NOT EXISTS FOR (e:Event) ON (e.type)")
                tx.run("CREATE INDEX event_date_index IF NOT EXISTS FOR (e:Event) ON (e.start_date)")
                
                # Interest constraints
                tx.run("CREATE CONSTRAINT interest_name_unique IF NOT EXISTS FOR (i:Interest) REQUIRE i.name IS UNIQUE")
                tx.run("CREATE INDEX interest_category_index IF NOT EXISTS FOR (i:Interest) ON (i.category)")
                
                # Project constraints
                tx.run("CREATE CONSTRAINT project_name_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE")
                tx.run("CREATE INDEX project_status_index IF NOT EXISTS FOR (p:Project) ON (p.status)")
                
                tx.commit()
                print("✅ Extended schema constraints created successfully")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Failed to setup extended constraints: {e}")
                raise
    
    def create_company(self, name: str, industry: str, founded_year: int, headquarters: str, size: str):
        """Create a Company node"""
        self.session.run("""
            MERGE (c:Company {name: $name})
            ON CREATE SET c.industry = $industry, c.founded_year = $founded_year, 
                         c.headquarters = $headquarters, c.size = $size
            ON MATCH SET c.industry = $industry, c.founded_year = $founded_year,
                         c.headquarters = $headquarters, c.size = $size
            """, name=name, industry=industry, founded_year=founded_year, 
                 headquarters=headquarters, size=size)
    
    def create_event(self, name: str, event_type: str, start_date: str, end_date: str, 
                    venue: str, description: str):
        """Create an Event node"""
        self.session.run("""
            MERGE (e:Event {name: $name})
            ON CREATE SET e.type = $type, e.start_date = date($start_date), 
                         e.end_date = date($end_date), e.venue = $venue, e.description = $description
            ON MATCH SET e.type = $type, e.start_date = date($start_date),
                         e.end_date = date($end_date), e.venue = $venue, e.description = $description
            """, name=name, type=event_type, start_date=start_date, 
                 end_date=end_date, venue=venue, description=description)
    
    def create_interest(self, name: str, category: str, level: str = "Intermediate"):
        """Create an Interest node"""
        self.session.run("""
            MERGE (i:Interest {name: $name})
            ON CREATE SET i.category = $category, i.level = $level
            ON MATCH SET i.category = $category, i.level = $level
            """, name=name, category=category, level=level)
    
    def create_project(self, name: str, description: str, start_date: str, 
                      end_date: str = None, status: str = "Active", budget: float = None):
        """Create a Project node"""
        self.session.run("""
            MERGE (p:Project {name: $name})
            ON CREATE SET p.description = $description, p.start_date = date($start_date),
                         p.end_date = $end_date, p.status = $status, p.budget = $budget
            ON MATCH SET p.description = $description, p.start_date = date($start_date),
                         p.end_date = $end_date, p.status = $status, p.budget = $budget
            """, name=name, description=description, start_date=start_date,
                 end_date=end_date, status=status, budget=budget)
    
    def create_works_for_relationship(self, person_name: str, company_name: str, 
                                    position: str, start_date: str, end_date: str = None, 
                                    department: str = None):
        """Create WORKS_FOR relationship"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (c:Company {name: $company_name})
            MERGE (p)-[:WORKS_FOR {
                position: $position,
                start_date: date($start_date),
                end_date: $end_date,
                department: $department
            }]->(c)
            """, person_name=person_name, company_name=company_name, position=position,
                 start_date=start_date, end_date=end_date, department=department)
    
    def create_attended_relationship(self, person_name: str, event_name: str, 
                                   role: str = "Attendee", feedback_rating: float = None):
        """Create ATTENDED relationship"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (e:Event {name: $event_name})
            MERGE (p)-[:ATTENDED {
                role: $role,
                feedback_rating: $feedback_rating
            }]->(e)
            """, person_name=person_name, event_name=event_name, role=role, 
                 feedback_rating=feedback_rating)
    
    def create_has_interest_relationship(self, person_name: str, interest_name: str, 
                                       proficiency: str = "Intermediate", years_experience: int = None):
        """Create HAS_INTEREST relationship"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (i:Interest {name: $interest_name})
            MERGE (p)-[:HAS_INTEREST {
                proficiency: $proficiency,
                years_experience: $years_experience
            }]->(i)
            """, person_name=person_name, interest_name=interest_name, 
                 proficiency=proficiency, years_experience=years_experience)
    
    def create_collaborates_relationship(self, person_name: str, project_name: str, 
                                       role: str, contribution: str):
        """Create COLLABORATES_ON relationship"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (proj:Project {name: $project_name})
            MERGE (p)-[:COLLABORATES_ON {
                role: $role,
                contribution: $contribution
            }]->(proj)
            """, person_name=person_name, project_name=project_name, 
                 role=role, contribution=contribution)
    
    def create_visited_relationship(self, person_name: str, city_name: str, 
                                  visit_date: str, purpose: str, duration_days: int = None):
        """Create VISITED relationship"""
        self.session.run("""
            MATCH (p:Person {name: $person_name})
            MATCH (c:City {name: $city_name})
            MERGE (p)-[:VISITED {
                visit_date: date($visit_date),
                purpose: $purpose,
                duration_days: $duration_days
            }]->(c)
            """, person_name=person_name, city_name=city_name, visit_date=visit_date,
                 purpose=purpose, duration_days=duration_days)
    
    def create_sample_extended_network(self):
        """Create a sample network with extended schema"""
        with self.session.begin_transaction() as tx:
            try:
                print("🏢 Creating companies...")
                companies = [
                    ("TechCorp", "Technology", 2010, "San Francisco", "Large"),
                    ("DataFlow", "Data Science", 2018, "New York", "Medium"),
                    ("GreenEnergy", "Renewable Energy", 2015, "Berlin", "Medium"),
                    ("HealthTech", "Healthcare", 2012, "London", "Large"),
                    ("StartupXYZ", "E-commerce", 2020, "Tokyo", "Small")
                ]
                
                for name, industry, founded, hq, size in companies:
                    self.create_company(name, industry, founded, hq, size)
                
                print("🎉 Creating events...")
                events = [
                    ("TechConf 2024", "Conference", "2024-06-15", "2024-06-17", "San Francisco", "Annual tech conference"),
                    ("Data Science Meetup", "Meetup", "2024-05-20", "2024-05-20", "New York", "Monthly data science meetup"),
                    ("Green Energy Summit", "Summit", "2024-07-10", "2024-07-12", "Berlin", "International energy conference"),
                    ("Health Innovation Workshop", "Workshop", "2024-04-25", "2024-04-26", "London", "Healthcare innovation workshop"),
                    ("Startup Pitch Night", "Pitch Event", "2024-06-30", "2024-06-30", "Tokyo", "Startup pitch competition")
                ]
                
                for name, event_type, start, end, venue, desc in events:
                    self.create_event(name, event_type, start, end, venue, desc)
                
                print("🎯 Creating interests...")
                interests = [
                    ("Python", "Technology", "Expert"),
                    ("Machine Learning", "Technology", "Intermediate"),
                    ("Data Visualization", "Data Science", "Advanced"),
                    ("Solar Energy", "Renewable Energy", "Intermediate"),
                    ("Healthcare Analytics", "Healthcare", "Expert"),
                    ("E-commerce Strategy", "Business", "Advanced"),
                    ("Blockchain", "Technology", "Beginner"),
                    ("AI Ethics", "Technology", "Intermediate")
                ]
                
                for name, category, level in interests:
                    self.create_interest(name, category, level)
                
                print("📋 Creating projects...")
                projects = [
                    ("AI Chatbot Platform", "Building an AI-powered chatbot for customer service", "2024-01-01", None, "Active", 50000.0),
                    ("Data Pipeline Optimization", "Optimizing data processing workflows", "2024-03-01", "2024-05-01", "Completed", 25000.0),
                    ("Green Energy Dashboard", "Creating a dashboard for renewable energy monitoring", "2024-02-01", None, "Active", 75000.0),
                    ("Healthcare Data Analysis", "Analyzing patient data for insights", "2024-01-15", None, "Active", 100000.0),
                    ("E-commerce Mobile App", "Developing a mobile app for online shopping", "2024-04-01", None, "Planning", 150000.0)
                ]
                
                for name, desc, start, end, status, budget in projects:
                    self.create_project(name, desc, start, end, status, budget)
                
                print("🔗 Creating professional relationships...")
                # People working for companies
                work_relationships = [
                    ("Roberts", "TechCorp", "Senior Developer", "2020-01-01", None, "Engineering"),
                    ("Wilson", "DataFlow", "Data Scientist", "2021-03-01", None, "Data Science"),
                    ("Brown", "GreenEnergy", "Project Manager", "2019-06-01", None, "Operations"),
                    ("Taylor", "HealthTech", "Research Analyst", "2022-01-01", None, "Research"),
                    ("Anderson", "StartupXYZ", "Founder", "2020-01-01", None, "Executive")
                ]
                
                for person, company, position, start, end, dept in work_relationships:
                    self.create_works_for_relationship(person, company, position, start, end, dept)
                
                print("🎭 Creating event attendance...")
                # People attending events
                attendance = [
                    ("Roberts", "TechConf 2024", "Speaker", 4.8),
                    ("Wilson", "Data Science Meetup", "Attendee", 4.5),
                    ("Brown", "Green Energy Summit", "Organizer", 4.9),
                    ("Taylor", "Health Innovation Workshop", "Attendee", 4.2),
                    ("Anderson", "Startup Pitch Night", "Judge", 4.7)
                ]
                
                for person, event, role, rating in attendance:
                    self.create_attended_relationship(person, event, role, rating)
                
                print("🎯 Creating interest relationships...")
                # People with interests
                interest_relationships = [
                    ("Roberts", "Python", "Expert", 8),
                    ("Wilson", "Machine Learning", "Advanced", 5),
                    ("Brown", "Solar Energy", "Intermediate", 3),
                    ("Taylor", "Healthcare Analytics", "Expert", 7),
                    ("Anderson", "E-commerce Strategy", "Advanced", 6)
                ]
                
                for person, interest, proficiency, years in interest_relationships:
                    self.create_has_interest_relationship(person, interest, proficiency, years)
                
                print("🤝 Creating project collaborations...")
                # People collaborating on projects
                collaborations = [
                    ("Roberts", "AI Chatbot Platform", "Lead Developer", "Architecture and core development"),
                    ("Wilson", "Data Pipeline Optimization", "Data Engineer", "Pipeline design and implementation"),
                    ("Brown", "Green Energy Dashboard", "Project Manager", "Project coordination and planning"),
                    ("Taylor", "Healthcare Data Analysis", "Data Analyst", "Data analysis and insights"),
                    ("Anderson", "E-commerce Mobile App", "Product Manager", "Product strategy and requirements")
                ]
                
                for person, project, role, contribution in collaborations:
                    self.create_collaborates_relationship(person, project, role, contribution)
                
                print("✈️ Creating travel relationships...")
                # People visiting cities
                visits = [
                    ("Roberts", "Berlin", "2024-02-15", "Business", 5),
                    ("Wilson", "Paris", "2024-01-20", "Leisure", 3),
                    ("Brown", "Tokyo", "2024-03-10", "Conference", 7),
                    ("Taylor", "Sydney", "2024-04-05", "Business", 4),
                    ("Anderson", "London", "2024-05-12", "Meeting", 2)
                ]
                
                for person, city, visit_date, purpose, duration in visits:
                    self.create_visited_relationship(person, city, visit_date, purpose, duration)
                
                tx.commit()
                print("✅ Extended network created successfully!")
                
            except Exception as e:
                tx.rollback()
                print(f"❌ Failed to create extended network: {e}")
                raise
    
    def get_extended_network_summary(self):
        """Get a complete summary of the extended network"""
        print("\n" + "="*60)
        print("🌐 EXTENDED NETWORK SUMMARY")
        print("="*60)
        
        # Count all node types
        node_counts = {}
        node_types = ["Person", "City", "Company", "Event", "Interest", "Project"]
        
        for node_type in node_types:
            count = self.session.run(f"MATCH (n:{node_type}) RETURN count(n) as total").single()['total']
            node_counts[node_type] = count
            print(f"📊 {node_type}s: {count}")
        
        # Count all relationship types
        rel_counts = {}
        rel_types = ["LIVES_IN", "MET_IN", "NEARBY", "WORKS_FOR", "ATTENDED", 
                    "HAS_INTEREST", "COLLABORATES_ON", "VISITED"]
        
        for rel_type in rel_types:
            count = self.session.run(f"MATCH ()-[r:{rel_type}]->() RETURN count(r) as total").single()['total']
            rel_counts[rel_type] = count
            print(f"🔗 {rel_type}: {count}")
        
        # Show some sample data
        print(f"\n🏢 SAMPLE COMPANIES:")
        companies = self.session.run("MATCH (c:Company) RETURN c.name as name, c.industry as industry LIMIT 5")
        for record in companies:
            print(f"  - {record['name']} ({record['industry']})")
        
        print(f"\n🎉 SAMPLE EVENTS:")
        events = self.session.run("MATCH (e:Event) RETURN e.name as name, e.type as type, e.venue as venue LIMIT 5")
        for record in events:
            print(f"  - {record['name']} ({record['type']}) in {record['venue']}")
        
        print(f"\n🎯 SAMPLE INTERESTS:")
        interests = self.session.run("MATCH (i:Interest) RETURN i.name as name, i.category as category LIMIT 5")
        for record in interests:
            print(f"  - {record['name']} ({record['category']})")
        
        print("="*60)

def main():
    """Main function to demonstrate extended schema"""
    # Load environment
    load_env_file('.noe4j.env')
    
    # Get connection details
    connection_uri = os.getenv('CONNECTION_URI')
    admin_password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('USERNAME', 'neo4j')
    neo4j_db = os.getenv('NEO4J_DB')
    
    if not connection_uri or not admin_password or not neo4j_db:
        raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")
    
    print("🚀 Neo4j Location Network - Extended Schema Demo")
    print("=" * 60)
    
    try:
        with ExtendedNeo4jNetwork(connection_uri, username, admin_password, neo4j_db) as network:
            print(f"🔗 Connected to database: {neo4j_db}")
            
            # Setup extended constraints
            network.setup_extended_constraints()
            
            # Create extended network
            network.create_sample_extended_network()
            
            # Show extended summary
            network.get_extended_network_summary()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
