from flask import Flask, jsonify, request
app = Flask(__name__)
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the User API!"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({user_id: user})
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_id = max(users.keys()) + 1 if users else 1
    users[new_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({new_id: users[new_id]}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    users[user_id].update(data)  
    return jsonify({user_id: users[user_id]})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    deleted_user = users.pop(user_id)
    return jsonify({"message": "User deleted", "user": deleted_user})

if __name__ == "__main__":
    app.run(debug=True)