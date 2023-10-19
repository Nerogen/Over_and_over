# Import necessary modules
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
import requests

# Create a Flask app
app: Flask = Flask(__name__)

# Configure the app to use the database URL from the environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DB_URL")

# Disable tracking modifications for SQLAlchemy to suppress a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the SQLAlchemy database
db: SQLAlchemy = SQLAlchemy(app)


# Define a SQLAlchemy model for the 'questions' table
class Question(db.Model):
    __tablename__: str = 'questions'
    id: db.Integer = db.Column(db.Integer, primary_key=True)
    question_text: db.String = db.Column(db.String, nullable=False)
    answer_text: db.String = db.Column(db.String, nullable=False)
    created_date: db.DateTime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, question_text: str, answer_text: str):
        self.question_text: str = question_text
        self.answer_text: str = answer_text


# Create the database tables
with app.app_context():
    db.create_all()


# Define a route for the home page
@app.route('/')
def index():
    return render_template('main.html')


# Define a route to fetch and store questions
@app.route('/get_questions/', methods=['POST'])
def get_questions():
    data: dict = request.get_json()
    questions_num: int = data.get('questions_num', 1)
    unique_questions: list[dict] = []

    while len(unique_questions) < questions_num:
        # Fetch random questions from an API
        response: requests.Response = requests.get(f"https://jservice.io/api/random?count={questions_num}")
        questions_data: requests.Response.json = response.json()

        for question_data in questions_data:
            # Check if the question already exists in the database
            existing_question: Question = Question.query.filter_by(question_text=question_data['question']).first()

            if existing_question:
                continue

            # Create a new Question instance and add it to the database
            question: Question = Question(
                question_text=question_data['question'],
                answer_text=question_data['answer']
            )
            db.session.add(question)
            db.session.commit()

            # Add the unique question to the response list
            unique_questions.append({
                'id': question.id,
                'question_text': question.question_text,
                'answer_text': question.answer_text,
                'created_date': question.created_date
            })

    # Return the unique questions as JSON
    return jsonify(unique_questions)


# Run the app if this script is the main module
if __name__ == '__main__':
    app.run(debug=True)
