#!/usr/bin/env python3
"""
Extended Schema Database Loader for Neo4j Location Network
Loads companies, events, interests, projects, and professional relationships
"""

import json
import os
from starter_demo import (
    Neo4jLocationNetwork,
    load_env_file
)

def load_extended_schema_data(json_file_path: str):
    """Load extended schema data from JSON file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if it's the new extended format
        if 'metadata' in data and data['metadata']['schema_version'] == 'extended_v1':
            print("✅ Loading extended schema data (v1)")
            return data['people'], data['companies'], data['events'], data['interests'], data['projects']
        else:
            # Fallback to old format (people only)
            print("⚠️ Loading legacy people-only data")
            return data, [], [], [], []
            
    except Exception as e:
        print(f"❌ Error loading data from {json_file_path}: {e}")
        raise

def validate_extended_data(people_data, companies, events, interests, projects):
    """Validate the extended schema data"""
    print("🔍 Validating extended schema data...")
    
    # Validate people data
    if not people_data:
        raise ValueError("No people data found")
    
    # Validate companies
    if companies:
        for company in companies:
            required_fields = ['name', 'industry', 'founded_year', 'headquarters', 'size']
            for field in required_fields:
                if field not in company:
                    raise ValueError(f"Company missing required field: {field}")
    
    # Validate events
    if events:
        for event in events:
            required_fields = ['name', 'type', 'start_date', 'end_date', 'venue', 'description']
            for field in required_fields:
                if field not in event:
                    raise ValueError(f"Event missing required field: {field}")
    
    # Validate interests
    if interests:
        for interest in interests:
            required_fields = ['name', 'category', 'level']
            for field in required_fields:
                if field not in interest:
                    raise ValueError(f"Interest missing required field: {field}")
    
    # Validate projects
    if projects:
        for project in projects:
            required_fields = ['name', 'description', 'start_date', 'status']
            for field in required_fields:
                if field not in project:
                    raise ValueError(f"Project missing required field: {field}")
    
    print(f"✅ Validation passed: {len(people_data)} people, {len(companies)} companies, {len(events)} events, {len(interests)} interests, {len(projects)} projects")

def load_companies_to_db(network, companies):
    """Load companies into the database"""
    if not companies:
        print("⚠️ No companies to load")
        return
    
    print(f"🏢 Loading {len(companies)} companies...")
    
    for i, company in enumerate(companies):
        try:
            network.create_company(
                name=company['name'],
                industry=company['industry'],
                founded_year=company['founded_year'],
                headquarters=company['headquarters'],
                size=company['size']
            )
            
            if (i + 1) % 10 == 0:
                print(f"  ✅ Loaded {i + 1}/{len(companies)} companies")
                
        except Exception as e:
            print(f"❌ Error loading company {company['name']}: {e}")
    
    print(f"✅ Successfully loaded {len(companies)} companies")

def load_events_to_db(network, events):
    """Load events into the database"""
    if not events:
        print("⚠️ No events to load")
        return
    
    print(f"🎉 Loading {len(events)} events...")
    
    for i, event in enumerate(events):
        try:
            network.create_event(
                name=event['name'],
                event_type=event['type'],
                start_date=event['start_date'],
                end_date=event['end_date'],
                venue=event['venue'],
                description=event['description']
            )
            
            if (i + 1) % 20 == 0:
                print(f"  ✅ Loaded {i + 1}/{len(events)} events")
                
        except Exception as e:
            print(f"❌ Error loading event {event['name']}: {e}")
    
    print(f"✅ Successfully loaded {len(events)} events")

def load_interests_to_db(network, interests):
    """Load interests into the database"""
    if not interests:
        print("⚠️ No interests to load")
        return
    
    print(f"🎯 Loading {len(interests)} interests...")
    
    for i, interest in enumerate(interests):
        try:
            network.create_interest(
                name=interest['name'],
                category=interest['category'],
                level=interest['level']
            )
            
            if (i + 1) % 20 == 0:
                print(f"  ✅ Loaded {i + 1}/{len(interests)} interests")
                
        except Exception as e:
            print(f"❌ Error loading interest {interest['name']}: {e}")
    
    print(f"✅ Successfully loaded {len(interests)} interests")

def load_projects_to_db(network, projects):
    """Load projects into the database"""
    if not projects:
        print("⚠️ No projects to load")
        return
    
    print(f"📋 Loading {len(projects)} projects...")
    
    for i, project in enumerate(projects):
        try:
            network.create_project(
                name=project['name'],
                description=project['description'],
                start_date=project['start_date'],
                end_date=project.get('end_date'),
                status=project['status'],
                budget=project.get('budget')
            )
            
            if (i + 1) % 20 == 0:
                print(f"  ✅ Loaded {i + 1}/{len(projects)} projects")
                
        except Exception as e:
            print(f"❌ Error loading project {project['name']}: {e}")
    
    print(f"✅ Successfully loaded {len(projects)} projects")

def load_professional_relationships(network, people_data, companies, events, interests, projects):
    """Load professional relationships into the database"""
    print("💼 Loading professional relationships...")
    
    total_relationships = 0
    
    for i, person in enumerate(people_data):
        if 'professional' not in person:
            continue
            
        prof = person['professional']
        
        try:
            # Load WORKS_FOR relationships
            if 'works_for' in prof:
                work = prof['works_for']
                network.create_works_for_relationship(
                    person_name=person['name'],
                    company_name=work['company'],
                    position=work['position'],
                    start_date=work['start_date'],
                    end_date=work.get('end_date'),
                    department=work.get('department')
                )
                total_relationships += 1
            
            # Load HAS_INTEREST relationships
            if 'interests' in prof:
                for interest in prof['interests']:
                    network.create_has_interest_relationship(
                        person_name=person['name'],
                        interest_name=interest['name'],
                        proficiency=interest['proficiency'],
                        years_experience=interest.get('years_experience')
                    )
                    total_relationships += 1
            
            # Load COLLABORATES_ON relationships
            if 'projects' in prof:
                for project in prof['projects']:
                    network.create_collaborates_relationship(
                        person_name=person['name'],
                        project_name=project['name'],
                        role=project['role'],
                        contribution=project['contribution']
                    )
                    total_relationships += 1
            
            # Load ATTENDED relationships (simplified - using event type)
            if 'events' in prof:
                for event_data in prof['events']:
                    # Find a matching event in our events list
                    matching_events = [e for e in events if e['type'] == event_data['type']]
                    if matching_events:
                        event = matching_events[0]
                        network.create_attended_relationship(
                            person_name=person['name'],
                            event_name=event['name'],
                            role=event_data['role'],
                            feedback_rating=event_data.get('rating')
                        )
                        total_relationships += 1
            
            if (i + 1) % 100 == 0:
                print(f"  ✅ Processed {i + 1}/{len(people_data)} people")
                
        except Exception as e:
            print(f"❌ Error loading professional relationships for {person['name']}: {e}")
    
    print(f"✅ Successfully loaded {total_relationships} professional relationships")

def main():
    """Main function to load extended schema data"""
    # Load environment
    load_env_file('.noe4j.env')
    
    # Get connection details
    connection_uri = os.getenv('CONNECTION_URI')
    admin_password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('USERNAME', 'neo4j')
    neo4j_db = os.getenv('NEO4J_DB')
    
    if not connection_uri or not admin_password or not neo4j_db:
        raise ValueError("Missing required environment variables. Please check your .noe4j.env file.")
    
    # File path for extended schema data
    json_file_path = "extended_schema_data.json"
    
    if not os.path.exists(json_file_path):
        print(f"❌ File not found: {json_file_path}")
        print("💡 Please run generate_dummy_data.py first to create the extended schema data")
        return
    
    print("🚀 Neo4j Location Network - Extended Schema Data Loader")
    print("=" * 60)
    
    try:
        # Load and validate data
        people_data, companies, events, interests, projects = load_extended_schema_data(json_file_path)
        validate_extended_data(people_data, companies, events, interests, projects)
        
        # Connect to database
        with Neo4jLocationNetwork(connection_uri, username, admin_password, neo4j_db) as network:
            print(f"🔗 Connected to database: {neo4j_db}")
            
            # Setup extended constraints
            print("🔧 Setting up extended schema constraints...")
            network.setup_extended_constraints()
            
            # Load extended schema data
            load_companies_to_db(network, companies)
            load_events_to_db(network, events)
            load_interests_to_db(network, interests)
            load_projects_to_db(network, projects)
            
            # Load professional relationships
            load_professional_relationships(network, people_data, companies, events, interests, projects)
            
            # Show final summary
            print("\n" + "="*60)
            print("🎉 EXTENDED SCHEMA LOADING COMPLETE!")
            print("="*60)
            network.get_extended_network_summary()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
