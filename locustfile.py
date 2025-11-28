from locust import HttpUser, task, between

class ClubSecretary(HttpUser):
    wait_time = between(1, 3)  # Pause 1-3s entre actions
    
    @task
    def visit_welcome(self):
        self.client.get("/")  # Page d'accueil
    
    @task
    def book_page(self):
        self.client.get("/book/Winter Gala/Simply Lift")  # Page réservation
    
    @task
    def points_page(self):
        self.client.get("/points")  # Tableau points
    
    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", {
            "competition": "Winter Gala",
            "club": "Simply Lift",
            "places": "1"
        })