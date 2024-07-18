from config import db

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(80), unique=False)
    state = db.Column(db.String(80), unique=False)
    # ratio = db.Column(db.String(80), unique=False)
    image_path = db.Column(db.String(255), unique=False) #connection status
    update_time = db.Column(db.String(80), unique=False) #ratio

    def to_json(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "name": self.name,
            "state": self.state,
            # "ratio": self.ratio,
            "image_path": self.image_path,
            "update_time": self.update_time,
        }

# from config import db


# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(80), unique=False, nullable=False)
#     last_name = db.Column(db.String(80), unique=False, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def to_json(self):
#         return {
#             "id": self.id,
#             "firstName": self.first_name,
#             "lastName": self.last_name,
#             "email": self.email,
#         }