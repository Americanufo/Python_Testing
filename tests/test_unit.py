# Tests unitaires pour la fonction purchasePlaces()

import pytest
import sys
import os  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Permet d'importer server

from unittest.mock import patch, MagicMock
from datetime import datetime
from server import loadClubs, loadCompetitions, app, purchasePlaces  # Import app et purchasePlaces

@pytest.fixture
def mock_data():
    """Données de test de base"""
    clubs = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}]
    competitions = [{"name": "Winter Gala", "date": "2025-12-15 09:00:00", "numberOfPlaces": "30"}]
    return clubs, competitions

def test_purchase_places_reussite(mock_data):
    """Test réservation 5 places """
    clubs, competitions = mock_data
    
    with app.test_request_context(method='POST', data={
        'competition': 'Winter Gala',
        'club': 'Simply Lift',
        'places': '5'
    }):
        with patch('server.loadClubs', return_value=clubs), \
             patch('server.loadCompetitions', return_value=competitions):
            
            purchasePlaces()
            
            # Vérifications : déductions effectuées
            assert int(competitions[0]['numberOfPlaces']) == 25  # 30-5
            assert int(clubs[0]['points']) == 8                 # 13-5

def test_purchase_places_competition_passee(mock_data):
    """Test : bloque si compétition passée"""
    clubs, competitions = mock_data
    competitions[0]['date'] = "2020-01-01 10:00:00"  # Date passée (AVANT 2025)
    
    with app.test_request_context(method='POST', data={
        'competition': 'Winter Gala',
        'club': 'Simply Lift',
        'places': '5'
    }):
        with patch('server.loadClubs', return_value=clubs), \
             patch('server.loadCompetitions', return_value=competitions):
            
            purchasePlaces()
            
            # Pas de modification des données
            assert competitions[0]['numberOfPlaces'] == "30"

def test_purchase_places_points_insuffisants(mock_data):
    """Test : bloque si pas assez de points"""
    clubs, competitions = mock_data
    clubs[0]['points'] = "3"  # Seulement 3 points
    
    with app.test_request_context(method='POST', data={
        'competition': 'Winter Gala',
        'club': 'Simply Lift',
        'places': '5'
    }):
        with patch('server.loadClubs', return_value=clubs), \
             patch('server.loadCompetitions', return_value=competitions):
            
            purchasePlaces()
            
            # Points inchangés
            assert clubs[0]['points'] == "3"

def test_purchase_places_places_insuffisants(mock_data):
    """Test : bloque si pas assez de places en compétition"""
    clubs, competitions = mock_data
    competitions[0]['numberOfPlaces'] = "3"  # Seulement 3 places
    
    with app.test_request_context(method='POST', data={
        'competition': 'Winter Gala',
        'club': 'Simply Lift',
        'places': '5'
    }):
        with patch('server.loadClubs', return_value=clubs), \
             patch('server.loadCompetitions', return_value=competitions):
            
            purchasePlaces()
            
            # Places inchangées
            assert competitions[0]['numberOfPlaces'] == "3"

def test_purchase_places_limite_12(mock_data):
    """Test : bloque au-delà de 12 places par réservation"""
    clubs, competitions = mock_data
    
    with app.test_request_context(method='POST', data={
        'competition': 'Winter Gala',
        'club': 'Simply Lift',
        'places': '13'
    }):
        with patch('server.loadClubs', return_value=clubs), \
             patch('server.loadCompetitions', return_value=competitions):
            
            purchasePlaces()
            
            # Pas de déduction
            assert competitions[0]['numberOfPlaces'] == "30"
