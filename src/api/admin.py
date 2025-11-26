  
import os
from flask_admin import Admin
from .models import db, User, Oferta
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.getenv('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='MercadoEspanol Admin')


    # Add your models here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Oferta, db.session))