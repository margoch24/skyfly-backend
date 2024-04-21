from api.controllers.reviews_controller import ReviewResource, ReviewsResource
from api.flask_app import FlaskApp

app = FlaskApp()

reviews_blueprint = app.create_blueprint("reviews")
reviews_api = app.create_api(reviews_blueprint)

app.add_resource(reviews_api, ReviewResource, "/review")
app.add_resource(reviews_api, ReviewsResource, "/reviews")
