from config import app, db
from models import Plant

def delete_plant_by_ip(ip):
    plant_to_delete = Plant.query.filter_by(ip=ip).first()
    if plant_to_delete:
        db.session.delete(plant_to_delete)
        db.session.commit()
        return plant_to_delete
    return None

def add_plant(ip):
    new_plant = Plant(ip=ip, name=None, state='Unknown', image_path='connect', update_time='0')
    db.session.add(new_plant)
    db.session.commit()
    return new_plant

def update_plant_ip(ip, state, progress):
    plant_to_update = Plant.query.filter_by(ip=ip).first()
    if plant_to_update:
        plant_to_update.state = state
        plant_to_update.update_time = progress
        db.session.commit()
        return plant_to_update
    return None

def set_plant_connect(ip):
    plant_to_update = Plant.query.filter_by(ip=ip).first()
    if plant_to_update:
        plant_to_update.image_path = 'connect'
        db.session.commit()
        return plant_to_update
    return None

def set_plant_disconnect(ip):
    plant_to_update = Plant.query.filter_by(ip=ip).first()
    if plant_to_update:
        plant_to_update.image_path = 'disconnect'
        db.session.commit()
        return plant_to_update
    return None

# with app.app_context():

    # delete plant: 
    # deleted_plant = delete_plant_by_ip('192.168.1.1')

    # add plant: (new ESP32CAM connect)
    # new_plant = add_plant('192.168.1.3')

    # update plant (new disease detect result available from model)
    # updated_plant = update_plant_ip('192.168.1.3', 'healthy', '0')

    # set plant connection state to 'connect' (default)
    # set_plant_connect('192.168.1.1')

    # set plant connection state to 'disconnect'
    # set_plant_disconnect('192.168.1.1')
    


    


