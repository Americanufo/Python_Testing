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
        'competition': 'Winter Gala',
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

def test_cannot_book_more_than_12_places(client):
    """Teste qu'on ne peut pas réserver plus de 12 places par réservation"""
    
    # Connexion Simply Lift (13 points)
    summary_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert summary_response.status_code == 200
    
    # Tentative de réservation de 13 places (AU-DESSUS DE 12)
    data_excess = {
        'competition': 'Winter Gala',  # Compétition future
        'club': 'Simply Lift', 
        'places': '13'
    }
    response_excess = client.post('/purchasePlaces', data=data_excess, follow_redirects=True)
    assert response_excess.status_code == 200
    assert b"Cannot book more than 12 places per competition per club" in response_excess.data  # ← ÉCHEC
    assert b'Great-booking complete!' not in response_excess.data
    
    # Vérifier que les points n'ont PAS été déduits (toujours 13)
    assert b'Points available: 13' in response_excess.data

def test_cannot_spend_more_points_than_available(client):
    """Teste qu'un club ne peut pas réserver plus de places que ses points disponibles"""
    
    # Connexion club Simply Lift (13 points)
    summary_response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert summary_response.status_code == 200
    
    # Tentative de réservation de 20 places (plus que 13 points)
    data_too_many = {
        'competition': 'Winter Gala',  # compétition future
        'club': 'Simply Lift',
        'places': '20'
    }
    
    response_too_many = client.post('/purchasePlaces', data=data_too_many, follow_redirects=True)
    assert response_too_many.status_code == 200
    assert b"Not enough points" in response_too_many.data 
    assert b'Great-booking complete!' not in response_too_many.data
    
    # Vérifier que les points restent inchangés (13)
    assert b'Points available: 13' in response_too_many.data

def test_cannot_book_more_places_than_available(client):
    """Teste qu'on ne peut pas réserver plus de places que disponibles dans la compétition"""
    
    # Connexion She Lifts (22 points)
    summary_response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert summary_response.status_code == 200
    
    # Tentative réservation 21 places sur New Year's Championship (20 places dispo)
    data_excess = {
        'competition': "New Year's Championship",  #  20 places disponibles
        'club': 'She Lifts',                      #  22 points disponibles  
        'places': '21'                            #  21 > 20 → doit échouer
    }
    
    response_excess = client.post('/purchasePlaces', data=data_excess, follow_redirects=True)
    assert response_excess.status_code == 200
    
    # Doit afficher une erreur places insuffisantes
    assert b"Not enough places available in this competition" in response_excess.data
    assert b'Great-booking complete!' not in response_excess.data
    
    # Points n'ont pas été déduits
    assert b'Points available: 22' in response_excess.data



def test_points_page_displays_all_clubs(client):
    """Teste que la page points affiche tous les clubs et leurs points"""
    response = client.get('/points')
    assert response.status_code == 200
    assert b'Simply Lift' in response.data
    assert b'Iron Temple' in response.data
    assert b'She Lifts' in response.data
    assert b'13' in response.data  # Simply Lift points
