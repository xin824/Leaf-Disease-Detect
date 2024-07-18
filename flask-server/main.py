from flask import request, jsonify, send_from_directory
from config import app, db
from models import Plant


@app.route("/plants", methods=["GET"])
def get_plants():
    plants = Plant.query.all()
    json_plants = list(map(lambda x: x.to_json(), plants))
    return jsonify({"plants": json_plants})


@app.route("/create_plant", methods=["POST"])
def create_plant():
    ip = request.json.get("ip")
    name = request.json.get("name")
    state = request.json.get("state")
    # ratio = request.json.get("ratio")
    image_path = request.json.get("image_path")
    update_time = request.json.get("update_time")

    new_plant = Plant(ip=ip, name=name, state=state, image_path=image_path, update_time=update_time)
    try:
        db.session.add(new_plant)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Plant created!"}), 201


@app.route("/update_plant/<int:user_id>", methods=["PATCH"])
def update_plant(user_id):
    plant = Plant.query.get(user_id)

    if not plant:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    plant.name = data.get("name", plant.name)
    plant.ip = data.get("ip", plant.ip)
    plant.state = data.get("state", plant.state)
    # plant.ratio = data.get("ratio", plant.ratio)
    plant.image_path = data.get("image_path", plant.image_path)
    plant.update_time = data.get("update_time", plant.update_time)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_plant/<int:user_id>", methods=["DELETE"])
def delete_plant(user_id):
    plant = Plant.query.get(user_id)

    if not plant:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(plant)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

@app.route("/delete_all_plants", methods=["DELETE"])
def delete_all_plants():
    try:
        num_rows_deleted = db.session.query(Plant).delete()
        db.session.commit()
        return jsonify({"message": f"Deleted {num_rows_deleted} plants"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
