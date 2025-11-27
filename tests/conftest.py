import json
import pytest
import sys 
import os

# Ajoute le répertoire parent pour server
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(autouse=True, scope='function')
def reset_json_files():
    """Reset clubs.json et competitions.json avant chaque test"""
    
    original_clubs = {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "11"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "22"}
        ]
    }
    
    original_competitions = {
        "competitions": [
            {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
            {"name": "Winter Gala", "date": "2025-12-15 09:00:00", "numberOfPlaces": "30"},
            {"name": "New Year's Championship", "date": "2026-01-02 11:00:00", "numberOfPlaces": "10"}
        ]
    }
    
    # Supprime les fichiers existants d'abord
    import os
    if os.path.exists('clubs.json'):
        os.remove('clubs.json')
    if os.path.exists('competitions.json'):
        os.remove('competitions.json')
    
    # Écriture des originaux
    with open('clubs.json', 'w') as f:
        json.dump(original_clubs, f, indent=2)
    with open('competitions.json', 'w') as f:
        json.dump(original_competitions, f, indent=2)

@pytest.fixture
def client():
    from server import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
