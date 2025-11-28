# GUDLFT - Réservation de Compétitions

## 📖 Description

Application Flask pour les secrétaires de clubs permettant de réserver des places de compétitions en utilisant des points. 

**Fonctionnalités principales :**
- Connexion sécurisée par email
- Réservation de places (max 12 par club)
- Déduction automatique des points
- Tableau public des points clubs

## Fonctionnalités Implémentées

###  Phase 1 - Authentification & Réservations
- [x] Connexion secrétaires via email/mot de passe
- [x] Liste compétitions à venir
- [x] Formulaire réservation `/book/mpétition>/<club>`
- [x] Achat places `/purchasePlaces`
- [x] Déconnexion `/logout`

###  Phase 2 - Transparence & Performance
- [x] Tableau points public `/points` (lecture seule)
- [x] Tests Locust : 6 utilisateurs simultanés
  - GET pages : 5-6ms (< 5s ✅)
  - POST achat : 14ms (< 2s ✅)
- [x] 100% Couverture pour le code server.py

###  Contraintes Métier
- [x] Max 12 places par club/compétition
- [x] Nombre de points requis pour la réservation
- [x] Pas de réservation pour les compétitions passées

## 🛠️ Installation et démarrage

### Prérequis
- Python 3.8 ou plus récent
- `pip` installé

### Installation des dépendances

Dans votre terminal, positionnez-vous dans le dossier du projet puis exécutez :

pip install -r requirements.txt

Cette commande installe les bibliothèques nécessaires.

### Lancement de l’application

Pour démarrer l’application Flask localement, tapez :

flask --app server.py run -p 5000


L’application sera accessible ensuite à l’adresse :  
`http://127.0.0.1:5000`

---

## 🧪 Tests automatisés

### Lancement des tests unitaires et d’intégration

Les tests sont organisés dans le dossier `tests/`. Pour exécuter tous les tests, utilisez :

coverage run -m pytest


Cela lance tous les tests tout en mesurant la couverture du code.

### Visualiser le rapport de couverture

Pour obtenir un rapport détaillé de la couverture de code :

coverage report -m


L’objectif est d’avoir un taux minimum de 60 % de couverture, mais ici la couverture est à 100 % sur `server.py`.

---

## 🚀 Tests de performance avec Locust

### Description

Locust simule des utilisateurs réels pour tester la performance sous charge. Ici, 6 utilisateurs effectuent les actions de consultation et réservation.

### Lancement des tests Locust

Dans un nouveau terminal, lancez Locust avec :

locust -f locustfile.py --host=http://localhost:5000 --users 6 --spawn-rate 1 --run-time 30s


Ensuite, ouvrez un navigateur à l’adresse :  
`http://localhost:8089`

Cliquez sur start avec 6 utilisateurs pour commencer les tests.

### Résultat attendu

Les temps de réponse doivent être :
- Inférieurs à 5 secondes pour le chargement des pages
- Inférieurs à 2 secondes pour les achats de places

Notre rapport `Locust_Test_Report.html` contient les résultats détaillés.

---

## Structure du projet

python_testing/
├── server.py # Application Flask principale
├── tests/
│ ├── test_unit.py # Tests unitaires
│ ├── test_integration.py # Tests d’intégration
│ └── conftest.py # Configuration pytest
├── locustfile.py # Scénarios de tests de performance Locust
├── Locust_Test_Report.html # Rapport de test de performance généré par Locust
└── README.md # Ce fichier
