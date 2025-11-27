import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # permet d'importer server.py qui est à la racine du projet

import pytest
from server import app

@pytest.fixture
def client():
    # Création d'un client test Flask pour simuler les requêtes HTTP
    with app.test_client() as client:
        yield client


def test_index(client):
    # Test basique pour vérifier que la page d'accueil répond bien
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'Bienvenue' in response.data or b'<html>' in response.data

def test_purchase_places_deducts_club_points(client):
    """Teste que les points du club sont déduits après réservation"""
    
    # Étape 1: Connexion avec email valide (Simply Lift a 13 points)
    summary_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert summary_response.status_code == 200
    
    # Étape 2: Réservation de 2 places pour Spring Festival
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': '2'
    }
    response = client.post('/purchasePlaces', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
    
    # Étape 3: Vérifier que les points ont été déduits (13 - 2 = 11)
    assert b'Points available: 11' in response.data 

def test_cannot_book_past_competitions(client):
    """Teste qu'on ne peut pas réserver pour des compétitions passées"""
    
    # Connexion Simply Lift
    summary_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert summary_response.status_code == 200
    
    # Tentative de réservation pour Spring Festival (2020 - PASSÉ)
    data_past = {
        'competition': 'Spring Festival', 
        'club': 'Simply Lift', 
        'places': '2'
    }
    response_past = client.post('/purchasePlaces', data=data_past, follow_redirects=True)
    assert response_past.status_code == 200
    assert b"Cannot book places for past competitions" in response_past.data
    assert b'Great-booking complete!' not in response_past.data
    
    # Vérifier que les points n'ont PAS été déduits (toujours 13)
    assert b'Points available: 13' in response_past.data
