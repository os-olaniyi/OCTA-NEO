#!/usr/bin/env python3
"""
Dummy Data Generator for Neo4j Location Network
Generates 700 realistic records with varied names, cities, countries, and relationships
"""

import json
import random
from typing import List, Dict, Tuple
import os

# Realistic data pools
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
    "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen",
    "Charles", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra",
    "Donald", "Donna", "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon", "Joshua", "Michelle",
    "Kenneth", "Laura", "Kevin", "Emily", "Brian", "Kimberly", "George", "Deborah", "Edward", "Dorothy",
    "Ronald", "Lisa", "Timothy", "Nancy", "Jason", "Karen", "Jeffrey", "Betty", "Ryan", "Helen",
    "Jacob", "Sandra", "Gary", "Donna", "Nicholas", "Carol", "Eric", "Ruth", "Jonathan", "Sharon",
    "Stephen", "Michelle", "Larry", "Laura", "Justin", "Emily", "Scott", "Kimberly", "Brandon", "Deborah",
    "Benjamin", "Dorothy", "Samuel", "Lisa", "Frank", "Nancy", "Gregory", "Karen", "Raymond", "Betty",
    "Alexander", "Helen", "Patrick", "Sandra", "Jack", "Donna", "Dennis", "Carol", "Jerry", "Ruth",
    "Tyler", "Sharon", "Aaron", "Michelle", "Jose", "Laura", "Adam", "Emily", "Nathan", "Kimberly",
    "Henry", "Deborah", "Douglas", "Dorothy", "Zachary", "Lisa", "Peter", "Nancy", "Kyle", "Karen",
    "Walter", "Betty", "Ethan", "Helen", "Jeremy", "Sandra", "Harold", "Donna", "Harold", "Carol",
    "Sean", "Ruth", "Austin", "Sharon", "Gerald", "Michelle", "Carlos", "Laura", "Ralph", "Emily",
    "Roy", "Kimberly", "Benjamin", "Deborah", "Russell", "Dorothy", "Bobby", "Lisa", "Victor", "Nancy",
    "Ernest", "Karen", "Phillip", "Betty", "Todd", "Helen", "Jesse", "Sandra", "Craig", "Donna",
    "Alan", "Carol", "Shawn", "Ruth", "Clarence", "Sharon", "Wayne", "Michelle", "Samuel", "Laura",
    "Willie", "Emily", "Ralph", "Kimberly", "Lawrence", "Deborah", "Nicholas", "Dorothy", "Roy", "Lisa",
    "Benjamin", "Nancy", "Bruce", "Karen", "Brandon", "Betty", "Adam", "Helen", "Harry", "Sandra",
    "Jeremy", "Donna", "Harold", "Carol", "Ethan", "Ruth", "Jesse", "Sharon", "Fred", "Michelle",
    "Glenn", "Laura", "Jeff", "Emily", "Travis", "Kimberly", "Jeffery", "Deborah", "Chad", "Dorothy",
    "Jacob", "Lisa", "Lee", "Nancy", "Melvin", "Karen", "Alfred", "Betty", "Kyle", "Helen",
    "Francis", "Sandra", "Bradley", "Donna", "Jesus", "Carol", "Herbert", "Ruth", "Frederick", "Sharon",
    "Ray", "Michelle", "Joel", "Laura", "Edwin", "Emily", "Don", "Kimberly", "Eddie", "Deborah",
    "Ricky", "Dorothy", "Troy", "Lisa", "Randall", "Nancy", "Barry", "Karen", "Alexander", "Betty",
    "Bernard", "Helen", "Mario", "Sandra", "Leroy", "Donna", "Francisco", "Carol", "Marcus", "Ruth",
    "Micheal", "Sharon", "Theodore", "Michelle", "Miguel", "Laura", "Julio", "Emily", "Darius", "Kimberly",
    "Oscar", "Deborah", "Bryant", "Dorothy", "Pierre", "Lisa", "Mike", "Nancy", "Theo", "Karen",
    "Elijah", "Betty", "Jermaine", "Helen", "Trent", "Sandra", "Enrique", "Donna", "Freddy", "Carol",
    "Dante", "Ruth", "Abel", "Sharon", "Bennie", "Michelle", "Jordan", "Laura", "Jarvis", "Emily",
    "Fabian", "Kimberly", "Milan", "Deborah", "Rolf", "Dorothy", "Chip", "Lisa", "Kris", "Nancy",
    "Burt", "Karen", "Sal", "Betty", "Alec", "Helen", "Tanner", "Sandra", "Jarred", "Donna",
    "Donn", "Carol", "Leigh", "Ruth", "Tito", "Sharon", "Archie", "Michelle", "Jess", "Laura",
    "Flint", "Emily", "Ariel", "Kimberly", "Erwin", "Deborah", "Avery", "Dorothy", "Dorsey", "Lisa",
    "Reid", "Nancy", "Rupert", "Karen", "Marlon", "Betty", "Lamont", "Helen", "Collin", "Sandra",
    "Dereck", "Donna", "Kenton", "Carol", "Abner", "Ruth", "Rashad", "Sharon", "Doug", "Michelle",
    "Kendrick", "Laura", "Jan", "Emily", "Emory", "Kimberly", "Maxie", "Deborah", "Vic", "Dorothy"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos",
    "Kim", "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett",
    "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell",
    "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero",
    "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin", "Wallace", "Moreno",
    "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar",
    "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods",
    "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker", "Guzman",
    "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter", "Gordon", "Mendez", "Silva", "Shaw",
    "Snyder", "Mason", "Dixon", "Muñoz", "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black",
    "Robertson", "Boyd", "Rose", "Stone", "Cooper", "Morris", "Clarke", "Coleman", "Jenkins", "Perry",
    "Morgan", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward",
    "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz",
    "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster",
    "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson",
    "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton",
    "Graham", "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera",
    "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall",
    "Owens", "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry",
    "Chen", "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter",
    "Hunter", "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Muñoz", "Hunt",
    "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Cooper"
]

# Extended schema data pools
COMPANY_NAMES = [
    "TechCorp", "DataFlow", "GreenEnergy", "HealthTech", "StartupXYZ", "InnovateLab", "CloudNine", "FutureSystems",
    "DigitalDynamics", "SmartSolutions", "GlobalTech", "NextGen", "EliteCorp", "VisionWorks", "PeakPerformance",
    "SummitSolutions", "EliteTech", "PrimeSystems", "CoreLogic", "AdvancedTech", "InnovationHub", "TechVentures",
    "DigitalEdge", "SmartCorp", "FutureTech", "EliteSolutions", "PeakTech", "SummitCorp", "EliteWorks", "PrimeTech",
    "CoreSystems", "AdvancedCorp", "InnovationTech", "TechHub", "DigitalVentures", "SmartEdge", "FutureCorp",
    "EliteEdge", "PeakSolutions", "SummitTech", "EliteCorp", "PrimeWorks", "CoreTech", "AdvancedSystems"
]

INDUSTRIES = [
    "Technology", "Data Science", "Renewable Energy", "Healthcare", "E-commerce", "Finance", "Education", "Manufacturing",
    "Consulting", "Media", "Transportation", "Real Estate", "Food & Beverage", "Retail", "Entertainment", "Sports",
    "Fashion", "Automotive", "Aerospace", "Biotechnology", "Pharmaceuticals", "Telecommunications", "Utilities", "Insurance"
]

COMPANY_SIZES = ["Startup", "Small", "Medium", "Large", "Enterprise"]

EVENT_TYPES = [
    "Conference", "Meetup", "Workshop", "Summit", "Hackathon", "Webinar", "Panel Discussion", "Networking Event",
    "Training Session", "Product Launch", "Award Ceremony", "Trade Show", "Exhibition", "Seminar", "Bootcamp"
]

INTERESTS = [
    "Python", "Machine Learning", "Data Science", "Web Development", "Mobile Development", "Cloud Computing",
    "Artificial Intelligence", "Blockchain", "Cybersecurity", "DevOps", "UI/UX Design", "Product Management",
    "Business Strategy", "Marketing", "Sales", "Finance", "Human Resources", "Operations", "Legal", "Research",
    "Writing", "Public Speaking", "Leadership", "Project Management", "Agile", "Scrum", "Data Analysis",
    "Statistics", "Mathematics", "Physics", "Chemistry", "Biology", "Medicine", "Psychology", "Sociology",
    "History", "Philosophy", "Literature", "Art", "Music", "Sports", "Fitness", "Cooking", "Travel", "Photography"
]

INTEREST_CATEGORIES = [
    "Technology", "Data Science", "Business", "Science", "Arts", "Sports", "Lifestyle", "Education", "Health"
]

PROFICIENCY_LEVELS = ["Beginner", "Intermediate", "Advanced", "Expert"]

PROJECT_TYPES = [
    "Web Application", "Mobile App", "Data Pipeline", "Machine Learning Model", "Research Study", "Business Plan",
    "Marketing Campaign", "Product Design", "Infrastructure Setup", "Security Audit", "Performance Optimization",
    "User Experience Design", "Content Creation", "Process Improvement", "Quality Assurance", "Documentation"
]

PROJECT_STATUSES = ["Planning", "Active", "On Hold", "Completed", "Cancelled"]

JOB_TITLES = [
    "Software Engineer", "Data Scientist", "Product Manager", "Business Analyst", "Marketing Manager", "Sales Representative",
    "Human Resources Manager", "Financial Analyst", "Operations Manager", "Project Manager", "Designer", "Researcher",
    "Consultant", "Executive", "Founder", "CEO", "CTO", "CFO", "COO", "VP Engineering", "VP Marketing", "VP Sales"
]

DEPARTMENTS = [
    "Engineering", "Data Science", "Product", "Marketing", "Sales", "Human Resources", "Finance", "Operations",
    "Legal", "Research & Development", "Customer Success", "Support", "Quality Assurance", "DevOps", "Security"
]

CITIES_COUNTRIES = [
    ("New York", "USA", 40.7128, -74.0060),
    ("Los Angeles", "USA", 34.0522, -118.2437),
    ("Chicago", "USA", 41.8781, -87.6298),
    ("Houston", "USA", 29.7604, -95.3698),
    ("Phoenix", "USA", 33.4484, -112.0740),
    ("Philadelphia", "USA", 39.9526, -75.1652),
    ("San Antonio", "USA", 29.4241, -98.4936),
    ("San Diego", "USA", 32.7157, -117.1611),
    ("Dallas", "USA", 32.7767, -96.7970),
    ("San Jose", "USA", 37.3382, -121.8863),
    ("London", "UK", 51.5074, -0.1278),
    ("Manchester", "UK", 53.4808, -2.2426),
    ("Birmingham", "UK", 52.4862, -1.8904),
    ("Leeds", "UK", 53.8008, -1.5491),
    ("Liverpool", "UK", 53.4084, -2.9916),
    ("Toronto", "Canada", 43.6532, -79.3832),
    ("Montreal", "Canada", 45.5017, -73.5673),
    ("Vancouver", "Canada", 49.2827, -123.1207),
    ("Calgary", "Canada", 51.0447, -114.0719),
    ("Edmonton", "Canada", 53.5461, -113.4938),
    ("Berlin", "Germany", 52.5200, 13.4050),
    ("Munich", "Germany", 48.1351, 11.5820),
    ("Hamburg", "Germany", 53.5511, 9.9937),
    ("Cologne", "Germany", 50.9375, 6.9603),
    ("Frankfurt", "Germany", 50.1109, 8.6821),
    ("Paris", "France", 48.8566, 2.3522),
    ("Marseille", "France", 43.2965, 5.3698),
    ("Lyon", "France", 45.7640, 4.8357),
    ("Toulouse", "France", 43.6047, 1.4442),
    ("Nice", "France", 43.7102, 7.2620),
    ("Madrid", "Spain", 40.4168, -3.7038),
    ("Barcelona", "Spain", 41.3851, 2.1734),
    ("Valencia", "Spain", 39.4699, -0.3763),
    ("Seville", "Spain", 37.3891, -5.9845),
    ("Zaragoza", "Spain", 41.6488, -0.8891),
    ("Rome", "Italy", 41.9028, 12.4964),
    ("Milan", "Italy", 45.4642, 9.1900),
    ("Naples", "Italy", 40.8518, 14.2681),
    ("Turin", "Italy", 45.0703, 7.6869),
    ("Palermo", "Italy", 38.1157, 13.3615),
    ("Tokyo", "Japan", 35.6762, 139.6503),
    ("Osaka", "Japan", 34.6937, 135.5023),
    ("Nagoya", "Japan", 35.1815, 136.9066),
    ("Sapporo", "Japan", 43.0618, 141.3545),
    ("Fukuoka", "Japan", 33.5902, 130.4017),
    ("Seoul", "South Korea", 37.5665, 126.9780),
    ("Busan", "South Korea", 35.1796, 129.0756),
    ("Incheon", "South Korea", 37.4563, 126.7052),
    ("Daegu", "South Korea", 35.8714, 128.6014),
    ("Daejeon", "South Korea", 36.3504, 127.3845),
    ("Beijing", "China", 39.9042, 116.4074),
    ("Shanghai", "China", 31.2304, 121.4737),
    ("Guangzhou", "China", 23.1291, 113.2644),
    ("Shenzhen", "China", 22.3193, 114.1694),
    ("Chengdu", "China", 30.5728, 104.0668),
    ("Mumbai", "India", 19.0760, 72.8777),
    ("Delhi", "India", 28.7041, 77.1025),
    ("Bangalore", "India", 12.9716, 77.5946),
    ("Hyderabad", "India", 17.3850, 78.4867),
    ("Chennai", "India", 13.0827, 80.2707),
    ("Sydney", "Australia", -33.8688, 151.2093),
    ("Melbourne", "Australia", -37.8136, 144.9631),
    ("Brisbane", "Australia", -27.4698, 153.0251),
    ("Perth", "Australia", -31.9505, 115.8605),
    ("Adelaide", "Australia", -34.9285, 138.6007),
    ("São Paulo", "Brazil", -23.5505, -46.6333),
    ("Rio de Janeiro", "Brazil", -22.9068, -43.1729),
    ("Brasília", "Brazil", -15.7942, -47.8822),
    ("Salvador", "Brazil", -12.9714, -38.5011),
    ("Fortaleza", "Brazil", -3.7319, -38.5267),
    ("Mexico City", "Mexico", 19.4326, -99.1332),
    ("Guadalajara", "Mexico", 20.6597, -103.3496),
    ("Monterrey", "Mexico", 25.6866, -100.3161),
    ("Puebla", "Mexico", 19.0413, -98.2062),
    ("Tijuana", "Mexico", 32.5149, -117.0382),
    ("Stockholm", "Sweden", 59.3293, 18.0686),
    ("Gothenburg", "Sweden", 57.7089, 11.9746),
    ("Malmö", "Sweden", 55.6050, 13.0038),
    ("Uppsala", "Sweden", 59.8586, 17.6389),
    ("Västerås", "Sweden", 59.6163, 16.5526),
    ("Amsterdam", "Netherlands", 52.3676, 4.9041),
    ("Rotterdam", "Netherlands", 51.9225, 4.4792),
    ("The Hague", "Netherlands", 52.0705, 4.3007),
    ("Utrecht", "Netherlands", 52.0907, 5.1214),
    ("Eindhoven", "Netherlands", 51.4416, 5.4697),
    ("Vienna", "Austria", 48.2082, 16.3738),
    ("Graz", "Austria", 47.0707, 15.4395),
    ("Linz", "Austria", 48.3069, 14.2858),
    ("Salzburg", "Austria", 47.8095, 13.0550),
    ("Innsbruck", "Austria", 47.2692, 11.4041),
    ("Zurich", "Switzerland", 47.3769, 8.5417),
    ("Geneva", "Switzerland", 46.2044, 6.1432),
    ("Basel", "Switzerland", 47.5596, 7.5886),
    ("Bern", "Switzerland", 46.9479, 7.4474),
    ("Lausanne", "Switzerland", 46.5197, 6.6323),
    ("Copenhagen", "Denmark", 55.6761, 12.5683),
    ("Aarhus", "Denmark", 56.1629, 10.2039),
    ("Odense", "Denmark", 55.4038, 10.4024),
    ("Aalborg", "Denmark", 57.0488, 9.9217),
    ("Esbjerg", "Denmark", 55.4668, 8.4517),
    ("Oslo", "Norway", 59.9139, 10.7522),
    ("Bergen", "Norway", 60.3913, 5.3221),
    ("Trondheim", "Norway", 63.4305, 10.3951),
    ("Stavanger", "Norway", 58.9700, 5.7331),
    ("Drammen", "Norway", 59.7440, 10.2045),
    ("Helsinki", "Finland", 60.1699, 24.9384),
    ("Espoo", "Finland", 60.2055, 24.6559),
    ("Tampere", "Finland", 61.4978, 23.7610),
    ("Vantaa", "Finland", 60.2934, 25.0378),
    ("Oulu", "Finland", 65.0121, 25.4651),
    ("Warsaw", "Poland", 52.2297, 21.0122),
    ("Kraków", "Poland", 50.0647, 19.9450),
    ("Łódź", "Poland", 51.7592, 19.4559),
    ("Wrocław", "Poland", 51.1079, 17.0385),
    ("Poznań", "Poland", 52.4064, 16.9252),
    ("Prague", "Czech Republic", 50.0755, 14.4378),
    ("Brno", "Czech Republic", 49.1951, 16.6068),
    ("Ostrava", "Czech Republic", 49.8209, 18.2625),
    ("Plzen", "Czech Republic", 49.7475, 13.3776),
    ("Liberec", "Czech Republic", 50.7663, 15.0543),
    ("Budapest", "Hungary", 47.4979, 19.0402),
    ("Debrecen", "Hungary", 47.5316, 21.6273),
    ("Szeged", "Hungary", 46.2530, 20.1414),
    ("Miskolc", "Hungary", 48.1034, 20.7784),
    ("Pécs", "Hungary", 46.0727, 18.2323),
    ("Bucharest", "Romania", 44.4268, 26.1025),
    ("Cluj-Napoca", "Romania", 46.7712, 23.6236),
    ("Timișoara", "Romania", 45.7489, 21.2087),
    ("Iași", "Romania", 47.1585, 27.6014),
    ("Constanța", "Romania", 44.1733, 28.6383),
    ("Sofia", "Bulgaria", 42.6977, 23.3219),
    ("Plovdiv", "Bulgaria", 42.1354, 24.7453),
    ("Varna", "Bulgaria", 43.2141, 27.9147),
    ("Burgas", "Bulgaria", 42.5048, 27.4626),
    ("Ruse", "Bulgaria", 43.8256, 25.9546),
    ("Athens", "Greece", 37.9838, 23.7275),
    ("Thessaloniki", "Greece", 40.6401, 22.9444),
    ("Patras", "Greece", 38.2466, 21.7346),
    ("Piraeus", "Greece", 37.9485, 23.6424),
    ("Larissa", "Greece", 39.6390, 22.4191),
    ("Lisbon", "Portugal", 38.7223, -9.1393),
    ("Porto", "Portugal", 41.1579, -8.6291),
    ("Vila Nova de Gaia", "Portugal", 41.1333, -8.6167),
    ("Amadora", "Portugal", 38.7548, -9.2308),
    ("Braga", "Portugal", 41.5454, -8.4265),
    ("Dublin", "Ireland", 53.3498, -6.2603),
    ("Cork", "Ireland", 51.8969, -8.4863),
    ("Limerick", "Ireland", 52.6638, -8.6267),
    ("Galway", "Ireland", 53.2707, -9.0568),
    ("Waterford", "Ireland", 52.2593, -7.1101),
    ("Belfast", "Northern Ireland", 54.5973, -5.9301),
    ("Derry", "Northern Ireland", 54.9966, -7.3086),
    ("Lisburn", "Northern Ireland", 54.5162, -6.0581),
    ("Newry", "Northern Ireland", 54.1759, -6.3374),
    ("Bangor", "Northern Ireland", 54.6598, -5.6696),
    ("Reykjavik", "Iceland", 64.1466, -21.9426),
    ("Kópavogur", "Iceland", 64.1122, -21.9131),
    ("Hafnarfjörður", "Iceland", 64.0291, -21.9685),
    ("Akureyri", "Iceland", 65.6839, -18.1105),
    ("Reykjanesbær", "Iceland", 63.9981, -22.5618),
    ("Luxembourg City", "Luxembourg", 49.6116, 6.1319),
    ("Esch-sur-Alzette", "Luxembourg", 49.4958, 5.9803),
    ("Differdange", "Luxembourg", 49.5242, 5.8914),
    ("Dudelange", "Luxembourg", 49.4808, 6.0875),
    ("Pétange", "Luxembourg", 49.5586, 5.8806),
    ("Bratislava", "Slovakia", 48.1486, 17.1077),
    ("Košice", "Slovakia", 48.7139, 21.2581),
    ("Prešov", "Slovakia", 48.9984, 21.2339),
    ("Žilina", "Slovakia", 49.2231, 18.7394),
    ("Banská Bystrica", "Slovakia", 48.7363, 19.1531),
    ("Ljubljana", "Slovenia", 46.0569, 14.5058),
    ("Maribor", "Slovenia", 46.5547, 15.6467),
    ("Celje", "Slovenia", 46.2309, 15.2604),
    ("Kranj", "Slovenia", 46.2389, 14.3556),
    ("Koper", "Slovenia", 45.5481, 13.7302),
    ("Tallinn", "Estonia", 59.4370, 24.7536),
    ("Tartu", "Estonia", 58.3776, 26.7290),
    ("Narva", "Estonia", 59.3772, 28.1903),
    ("Pärnu", "Estonia", 58.3858, 24.4966),
    ("Kohtla-Järve", "Estonia", 59.3984, 27.2731),
    ("Riga", "Latvia", 56.9496, 24.1052),
    ("Daugavpils", "Latvia", 55.8754, 26.5362),
    ("Liepāja", "Latvia", 56.5047, 21.0108),
    ("Jelgava", "Latvia", 56.6511, 23.7214),
    ("Jūrmala", "Latvia", 56.9682, 23.7703),
    ("Vilnius", "Lithuania", 54.6872, 25.2797),
    ("Kaunas", "Lithuania", 54.8985, 23.9036),
    ("Klaipėda", "Lithuania", 55.7033, 21.1443),
    ("Šiauliai", "Lithuania", 55.9333, 23.3167),
    ("Panevėžys", "Lithuania", 55.7375, 24.3697),
    ("Warsaw", "Poland", 52.2297, 21.0122),
    ("Kraków", "Poland", 50.0647, 19.9450),
    ("Łódź", "Poland", 51.7592, 19.4559),
    ("Wrocław", "Poland", 51.1079, 17.0385),
    ("Poznań", "Poland", 52.4064, 16.9252)
]

def generate_realistic_name():
    """Generate a realistic full name"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"

def generate_city_country():
    """Generate a random city and country with coordinates"""
    return random.choice(CITIES_COUNTRIES)

def generate_company():
    """Generate a realistic company"""
    name = random.choice(COMPANY_NAMES)
    industry = random.choice(INDUSTRIES)
    founded_year = random.randint(1990, 2024)
    size = random.choice(COMPANY_SIZES)
    
    # Generate headquarters from existing cities
    city, country, _, _ = random.choice(CITIES_COUNTRIES)
    
    return {
        "name": name,
        "industry": industry,
        "founded_year": founded_year,
        "headquarters": city,
        "size": size
    }

def generate_event():
    """Generate a realistic event"""
    event_type = random.choice(EVENT_TYPES)
    
    # Generate event name based on type
    if event_type == "Conference":
        name = f"{random.choice(['Tech', 'Data', 'AI', 'Business', 'Innovation'])}Conf {random.randint(2024, 2025)}"
    elif event_type == "Meetup":
        name = f"{random.choice(['Data Science', 'Tech', 'Startup', 'AI'])} Meetup"
    elif event_type == "Workshop":
        name = f"{random.choice(['Machine Learning', 'Web Development', 'Product Design'])} Workshop"
    else:
        name = f"{event_type} {random.randint(1, 100)}"
    
    # Generate dates (events in the future)
    start_date = f"2024-{random.randint(6, 12):02d}-{random.randint(1, 28):02d}"
    end_date = f"2024-{random.randint(6, 12):02d}-{random.randint(1, 28):02d}"
    
    # Ensure end_date is after start_date
    if end_date < start_date:
        end_date = start_date
    
    # Pick venue from existing cities
    venue, _, _, _ = random.choice(CITIES_COUNTRIES)
    
    description = f"A {event_type.lower()} focused on {random.choice(['innovation', 'learning', 'networking', 'collaboration'])}"
    
    return {
        "name": name,
        "type": event_type,
        "start_date": start_date,
        "end_date": end_date,
        "venue": venue,
        "description": description
    }

def generate_interest():
    """Generate a realistic interest"""
    name = random.choice(INTERESTS)
    category = random.choice(INTEREST_CATEGORIES)
    level = random.choice(PROFICIENCY_LEVELS)
    
    return {
        "name": name,
        "category": category,
        "level": level
    }

def generate_project():
    """Generate a realistic project"""
    project_type = random.choice(PROJECT_TYPES)
    name = f"{project_type} Project"
    
    descriptions = {
        "Web Application": "Building a modern web application with responsive design",
        "Mobile App": "Developing a cross-platform mobile application",
        "Data Pipeline": "Creating an automated data processing pipeline",
        "Machine Learning Model": "Training and deploying a machine learning model",
        "Research Study": "Conducting comprehensive research and analysis",
        "Business Plan": "Developing a strategic business plan and roadmap",
        "Marketing Campaign": "Designing and executing a marketing campaign",
        "Product Design": "Creating user-centered product design solutions"
    }
    
    description = descriptions.get(project_type, f"Working on {project_type.lower()}")
    
    # Generate dates
    start_date = f"2024-{random.randint(1, 6):02d}-{random.randint(1, 28):02d}"
    end_date = None if random.random() < 0.7 else f"2024-{random.randint(7, 12):02d}-{random.randint(1, 28):02d}"
    
    status = random.choice(PROJECT_STATUSES)
    budget = random.randint(10000, 500000) if random.random() < 0.8 else None
    
    return {
        "name": name,
        "description": description,
        "start_date": start_date,
        "end_date": end_date,
        "status": status,
        "budget": budget
    }

def generate_professional_profile(person_name: str, existing_companies: list, existing_interests: list, existing_projects: list):
    """Generate professional profile for a person"""
    profile = {}
    
    # 70% chance of having a job
    if random.random() < 0.7 and existing_companies:
        company = random.choice(existing_companies)
        job_title = random.choice(JOB_TITLES)
        department = random.choice(DEPARTMENTS)
        start_date = f"20{random.randint(15, 24)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        end_date = None if random.random() < 0.8 else f"20{random.randint(20, 24)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        
        profile["works_for"] = {
            "company": company["name"],
            "position": job_title,
            "department": department,
            "start_date": start_date,
            "end_date": end_date
        }
    
    # 60% chance of having interests
    if random.random() < 0.6 and existing_interests:
        num_interests = random.randint(1, 4)
        selected_interests = random.sample(existing_interests, min(num_interests, len(existing_interests)))
        
        profile["interests"] = []
        for interest in selected_interests:
            profile["interests"].append({
                "name": interest["name"],
                "proficiency": random.choice(PROFICIENCY_LEVELS),
                "years_experience": random.randint(1, 10)
            })
    
    # 40% chance of working on projects
    if random.random() < 0.4 and existing_projects:
        num_projects = random.randint(1, 2)
        selected_projects = random.sample(existing_projects, min(num_projects, len(existing_projects)))
        
        profile["projects"] = []
        for project in selected_projects:
            profile["projects"].append({
                "name": project["name"],
                "role": random.choice(JOB_TITLES),
                "contribution": f"Contributed to {project['name'].lower()}"
            })
    
    # 50% chance of attending events
    if random.random() < 0.5:
        profile["events"] = []
        num_events = random.randint(1, 3)
        
        for _ in range(num_events):
            event_type = random.choice(EVENT_TYPES)
            role = random.choice(["Attendee", "Speaker", "Organizer", "Panelist"])
            rating = round(random.uniform(3.5, 5.0), 1) if role == "Attendee" else None
            
            profile["events"].append({
                "type": event_type,
                "role": role,
                "rating": rating
            })
    
    return profile

def generate_friends_data(existing_people: List[str], current_person: str, num_friends: int = None):
    """Generate realistic friend relationships"""
    if not existing_people:
        return []
    
    if num_friends is None:
        # Random number of friends (0-5, weighted towards fewer friends)
        num_friends = random.choices([0, 1, 2, 3, 4, 5], weights=[0.3, 0.3, 0.2, 0.1, 0.08, 0.02])[0]
    
    if num_friends == 0:
        return []
    
    # Select random friends (excluding self)
    available_friends = [p for p in existing_people if p != current_person]
    if len(available_friends) < num_friends:
        num_friends = len(available_friends)
    
    selected_friends = random.sample(available_friends, num_friends)
    
    friends_data = []
    for friend in selected_friends:
        # Generate a realistic meeting city (could be either person's city or a third city)
        meeting_options = [
            (current_person, "current"),  # Current person's city
            (friend, "friend"),           # Friend's city
            (None, "third")               # Third city
        ]
        
        meeting_type = random.choices(meeting_options, weights=[0.4, 0.4, 0.2])[0]
        
        if meeting_type[1] == "third":
            # Pick a random city from the list
            meeting_city, _, _, _ = random.choice(CITIES_COUNTRIES)
        else:
            # Use one of the people's cities
            meeting_city = meeting_type[0]
        
        friends_data.append({
            "name": friend,
            "meeting_city": meeting_city
        })
    
    return friends_data

def generate_extended_schema_data():
    """Generate extended schema data (companies, events, interests, projects)"""
    print("🏢 Generating extended schema data...")
    
    # Generate companies
    companies = []
    for i in range(50):  # Generate 50 companies
        company = generate_company()
        companies.append(company)
    
    # Generate events
    events = []
    for i in range(100):  # Generate 100 events
        event = generate_event()
        events.append(event)
    
    # Generate interests
    interests = []
    for i in range(80):  # Generate 80 interests
        interest = generate_interest()
        interests.append(interest)
    
    # Generate projects
    projects = []
    for i in range(120):  # Generate 120 projects
        project = generate_project()
        projects.append(project)
    
    print(f"✅ Generated {len(companies)} companies, {len(events)} events, {len(interests)} interests, {len(projects)} projects")
    return companies, events, interests, projects

def generate_700_people():
    """Generate 700 realistic people records with extended schema data"""
    print("🚀 Generating 700 realistic people records with extended schema...")
    
    # First generate extended schema data
    companies, events, interests, projects = generate_extended_schema_data()
    
    people_data = []
    existing_people = []
    
    for i in range(700):
        # Generate person
        name = generate_realistic_name()
        city, country, lat, lon = generate_city_country()
        
        # Add to existing people list for relationship generation
        existing_people.append(name)
        
        # Generate friends data (relationships)
        friends_data = generate_friends_data(existing_people, name)
        
        # Generate professional profile
        professional_profile = generate_professional_profile(name, companies, interests, projects)
        
        # Create person record
        person_record = {
            "name": name,
            "city": city,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "friends": friends_data,
            "professional": professional_profile
        }
        
        people_data.append(person_record)
        
        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"✅ Generated {i + 1}/700 people")
    
    print(f"🎉 Successfully generated {len(people_data)} people records with extended schema!")
    return people_data, companies, events, interests, projects

def save_to_json(data: List[Dict], companies: List[Dict], events: List[Dict], 
                interests: List[Dict], projects: List[Dict], filename: str = "700_people_data.json"):
    """Save the generated data to a JSON file with extended schema"""
    try:
        # Create comprehensive dataset
        complete_dataset = {
            "people": data,
            "companies": companies,
            "events": events,
            "interests": interests,
            "projects": projects,
            "metadata": {
                "generated_at": "2024-01-01",
                "total_people": len(data),
                "total_companies": len(companies),
                "total_events": len(events),
                "total_interests": len(interests),
                "total_projects": len(projects),
                "schema_version": "extended_v1"
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(complete_dataset, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Extended schema data saved to {filename}")
        print(f"📊 File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"❌ Error saving to {filename}: {e}")

def save_people_only(data: List[Dict], filename: str = "700_people_data.json"):
    """Save only people data (backward compatibility)"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 People data saved to {filename}")
        print(f"📊 File size: {os.path.getsize(filename) / 1024 / 1024:.2f} MB")
        
    except Exception as e:
        print(f"❌ Error saving to {filename}: {e}")

def main():
    """Main function to generate and save dummy data"""
    print("🎯 Neo4j Location Network - Extended Schema Dummy Data Generator")
    print("=" * 60)
    
    # Generate 700 people with extended schema
    people_data, companies, events, interests, projects = generate_700_people()
    
    # Save complete extended schema data
    save_to_json(people_data, companies, events, interests, projects, "extended_schema_data.json")
    
    # Also save people-only data for backward compatibility
    save_people_only(people_data, "700_people_data.json")
    
    # Show comprehensive statistics
    print("\n📊 EXTENDED SCHEMA GENERATION STATISTICS:")
    print("=" * 50)
    
    # Count by country
    countries = {}
    cities = {}
    total_relationships = 0
    total_professional_relationships = 0
    
    for person in people_data:
        country = person['country']
        city = person['city']
        relationships = len(person['friends'])
        
        countries[country] = countries.get(country, 0) + 1
        cities[city] = cities.get(city, 0) + 1
        total_relationships += relationships
        
        # Count professional relationships
        if 'professional' in person:
            prof = person['professional']
            if 'works_for' in prof:
                total_professional_relationships += 1
            if 'interests' in prof:
                total_professional_relationships += len(prof['interests'])
            if 'projects' in prof:
                total_professional_relationships += len(prof['projects'])
            if 'events' in prof:
                total_professional_relationships += len(prof['events'])
    
    print(f"👥 Total people: {len(people_data)}")
    print(f"🏢 Total companies: {len(companies)}")
    print(f"🎉 Total events: {len(events)}")
    print(f"🎯 Total interests: {len(interests)}")
    print(f"📋 Total projects: {len(projects)}")
    print(f"🏙️ Unique cities: {len(cities)}")
    print(f"🌍 Unique countries: {len(countries)}")
    print(f"🔗 Total social relationships: {total_relationships}")
    print(f"💼 Total professional relationships: {total_professional_relationships}")
    print(f"📈 Average social relationships per person: {total_relationships / len(people_data):.2f}")
    print(f"📈 Average professional relationships per person: {total_professional_relationships / len(people_data):.2f}")
    
    # Top countries
    print(f"\n🏆 TOP 5 COUNTRIES:")
    sorted_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)
    for i, (country, count) in enumerate(sorted_countries[:5], 1):
        print(f"  {i}. {country}: {count} people")
    
    # Top cities
    print(f"\n🏆 TOP 5 CITIES:")
    sorted_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)
    for i, (city, count) in enumerate(sorted_cities[:5], 1):
        print(f"  {i}. {city}: {count} people")
    
    # Industry distribution
    print(f"\n🏭 TOP 5 INDUSTRIES:")
    industry_counts = {}
    for company in companies:
        industry = company['industry']
        industry_counts[industry] = industry_counts.get(industry, 0) + 1
    
    sorted_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (industry, count) in enumerate(sorted_industries[:5], 1):
        print(f"  {i}. {industry}: {count} companies")
    
    # Event type distribution
    print(f"\n🎭 TOP 5 EVENT TYPES:")
    event_type_counts = {}
    for event in events:
        event_type = event['type']
        event_type_counts[event_type] = event_type_counts.get(event_type, 0) + 1
    
    sorted_event_types = sorted(event_type_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (event_type, count) in enumerate(sorted_event_types[:5], 1):
        print(f"  {i}. {event_type}: {count} events")
    
    print("\n🎯 Ready to use with extended_schema_demo.py!")
    print("📁 Files created:")
    print("  - extended_schema_data.json (complete extended schema)")
    print("  - 700_people_data.json (people only, backward compatible)")

if __name__ == "__main__":
    main()
