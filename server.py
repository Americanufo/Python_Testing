import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions

def saveClubs(clubs_list):
    """Sauvegarde la liste des clubs mise à jour dans clubs.json"""
    with open('clubs.json', 'w') as f:
        json.dump({'clubs': clubs_list}, f, indent=2)

def saveCompetitions(competitions_list):
    """Sauvegarde la liste des compétitions mise à jour dans competitions.json"""
    with open('competitions.json', 'w') as f:
        json.dump({'competitions': competitions_list}, f, indent=2)


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    # Chargement des données
    competitions = loadCompetitions()
    clubs = loadClubs()

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Vérifier la date de la compétition
    competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if competition_date < now:
        flash("Cannot book places for past competitions")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Vérifier la limite de 12 places max
    if placesRequired > 12:
        flash("Cannot book more than 12 places per competition per club")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Vérification du nombre de points restants avant réservation
    if placesRequired > int(club['points']):
        flash("Not enough points")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Vérifier que la compétition a assez de places disponibles
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Not enough places available in this competition")
        return render_template('welcome.html', club=club, competitions=competitions)
    
    # Déduire les places disponibles
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    # Déduire les points du club
    club['points'] = int(club['points']) - placesRequired

    # Sauvegarder les changements dans les fichiers JSON
    saveCompetitions(competitions)
    saveClubs(clubs)
    
    flash('Great-booking complete!')
    # Toujours recharger clubs et competitions avant d'envoyer au template
    return render_template('welcome.html', club=club, competitions=loadCompetitions())


@app.route('/points')
def show_points():
    """Affiche le tableau des points de tous les clubs (lecture seule)"""
    clubs = loadClubs()  # Recharge pour état actuel
    return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))