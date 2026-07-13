# WFH Burnout Data Prediction

## Project Description
This project implements a Flask web application to predict WFH (Work From Home) burnout scores. It uses a pre-trained machine learning model and stores user data and predictions in a MongoDB database.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd WFH_Burnout_Data
```

### 2. Set up a Python Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```
*(Note: A `requirements.txt` file is assumed to exist or will need to be created with `pip freeze > requirements.txt` after installing necessary libraries like Flask, PyMongo, scikit-learn, Keras, etc.)*

### 4. MongoDB Setup
This project uses MongoDB. Ensure you have MongoDB installed and running on `localhost:27017`.
The application will connect to a database named `wfh_burnout` and use collections `burnout_data` and `wfh_users`.

### 5. Machine Learning Model Artifacts
The project relies on pre-trained model artifacts located in the `artifacts/` directory. Ensure these files are present:
- `MLP_Trained_Model.keras`
- `MLP_col_data.json`
- `std_scalar.pkl`
These files are typically generated during model training and should be placed in the `artifacts/` folder in the project root.

## Running the Application

### 1. Activate Virtual Environment (if not already active)
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Run the Flask Application
```bash
python main.py
```

The application will typically run on `http://0.0.0.0:5000` (or `http://127.0.0.1:5000`).

## API Endpoints

- `/`: Redirects to `/login_page`
- `/login_page`: Renders the login page.
- `/register_page`: Renders the registration page.
- `/forgot_password_page`: Renders the forgot password page.
- `/register` (POST): Registers a new user.
- `/login` (POST): Logs in a user and returns a JWT access token.
- `/forget_password` (POST): Allows a user to reset their password.
- `/predict_burnout_score` (POST, JWT Protected): Predicts burnout score based on user input.
- `/show_day_type_options` (GET): Returns available day type options for prediction form.
- `/logout` (GET/POST): Logs out the user.
- `/dashboard`: Renders the dashboard page.
- `/prediction_form_page`: Redirects to the dashboard page.

---