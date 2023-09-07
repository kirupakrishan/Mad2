from routes import db
from flask import request, jsonify, Response
from Models.user_model import Users
import json
from helpers import token_required, token_generate
from flask import Blueprint

auth_routes = Blueprint('auth_routes', __name__)

# Route for Login
@auth_routes.route('/login', methods=["POST"])
def login():
    # getting login info from the form
    login = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    # using try catch for sys error and check pass
    try:
        user = Users.query.filter_by(email=login["email"]).first()
        if not user:
            return jsonify({'message': "Invalid Credentials"})

        if (user.password == login["password"]):
            token = token_generate(login["email"])
            return jsonify({"token": token,"admin":user.admin}), 200

        else:
            return jsonify({"message": "Invalid Credentials"}), 404

    except:
        return jsonify({"message": "Invalid Credentials"}), 404

#Route for Signup
@auth_routes.route('/signup', methods=["POST"])
def signup():
    # creating a user dict to store the values from the forms
    # Form Details : username , email , password , cPassword
    user = request.json
    print(user)
    if user["password"] == user["cPassword"]:
        # creating a connection to database and initializing the cursor
        new_user = Users(name=user["username"], email=user["email"],password=user["password"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"token": token_generate(new_user.email)}), 200
    else:
        return Response(
            response=json.dumps(
                {"message": "Password Incorrect. Try again!!"}),
            status=401,
            mimetype="application/json")

