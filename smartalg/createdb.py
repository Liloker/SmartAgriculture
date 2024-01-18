from flask_models import *

with app.app_context():
    db.create_all()
