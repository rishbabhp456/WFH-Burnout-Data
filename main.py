from flask import Flask, jsonify, request,render_template, redirect, url_for, session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from src import utils
import config
import pymongo,datetime

obj_wfh_burnout = utils.WFH_Burnout()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = 'secret'
app.config["SECRET_KEY"] = "flask-session-secret"
jwt = JWTManager(app)

mongo_client = pymongo.MongoClient(config.MONGO_URL)
db = mongo_client[config.db_name]
data_collection = db[config.collection_user]

@app.route('/')
def index():
    return redirect(url_for('login_page'))


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/register_page')
def register_page():
    return render_template('register.html')


@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('forgot_password.html')



@app.route('/register', methods=['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    dob = data.get('dob')
    response = data_collection.find_one({"username": username},{"email": email})
    if not response:
        data_collection.insert_one({"username": username, "password": password, "email": email, "dob": dob})
        return jsonify({"message": "User registered successfully!"})
    else:
        return jsonify({"message": "User already exists!"})



@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('username') 
    password = data.get('password')
    response = data_collection.find_one({"username": username, "password": password})

    if response:
        access_token = create_access_token(identity=username,
                                            expires_delta= datetime.timedelta(minutes=5))
        return jsonify({"status": "success","message": "Login Successful", 
                        "access_token":access_token})
    else:
        return jsonify({"status": "failure", "message": "Invalid Credentials"})
    


@app.route("/forget_password", methods=["POST"])
def forget_password():
    data = request.form
    username = data.get('username')
    email = data.get('email')
    new_password = data.get('new_password')

    response = data_collection.find_one({"username": username, "email": email})
    if response:
        data_collection.update_one({"username": username, "email": email}, {"$set": {"password": new_password}})
        return jsonify({"status": "success", "message": "Password updated successfully"})
    else:
        return jsonify({"status": "failure", "message": "Invalid username or email"})



@app.route('/predict_burnout_score', methods=['POST'])
@jwt_required()
def predict_burnout_score():
    current_user = get_jwt_identity()
    user_input_data = request.form

    prediction = obj_wfh_burnout.predict_burnout(user_input_data)
    obj_wfh_burnout.save_data_in_db(user_input_data)
    return jsonify({"status": "success", "message": "Burnout score predicted successfully", "prediction": prediction, "user": current_user})



@app.route("/show_day_type_options", methods=["GET"])
def show_day_type_options():
    col_data = obj_wfh_burnout.load_column_data()
    day_type_values = list(col_data['day_type'].keys())
    return jsonify({"status": "success", "day_type_options": day_type_values})


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    if request.method == 'POST':
        return jsonify({"status": "success", "message": "Logged out successfully"})
    return redirect(url_for('login_page'))



@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')


@app.route('/prediction_form_page')
def prediction_form_page():
    return redirect(url_for('dashboard_page'))


if __name__ == '__main__':
    app.run(host= config.FLASK_HOST, port=config.FLASK_PORT,debug=True)