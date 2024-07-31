import control
from config import app

with app.app_context():
    new_plant = control.add_plant('192.168.1.2')
