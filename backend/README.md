# Trivia API Backend

## Getting Started

### Dependencies

#### Python 3.8

Follow instructions to install the latest version of python [on Unix OS](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) and [on Windows OS](https://docs.python.org/3/using/windows.html)
> The project's python code follow `PEP8 Styling Guide`

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, follow these steps to create a database and seed some sample data into the database:
1. Create a new database using the command
   ```bash
   $ createdb trivia
   ```
2. Later, run the python file `data_feeder.py` to seed some sample data

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ python app.py
```

## Endpoints

#### Overview

These are the following endpoints available to access the resources in Trivia API

1. Catagory related endpoints
   ```
   GET '/categories'                                - All categories
   GET '/categories/<int:category_id>/questions'    - All questions per category
   ```
2. Question related endpoints
   ```
   GET '/questions'                                 - All questions
   POST '/questions'                                - Create a new question
   POST '/questions/search'                         - Search for existing question
   DELETE '/questions/<int:question_id>'            - Delete a question (using Question ID)
   ```
3. And lastly, endpoint to generate random questions from selected category
   ```
   POST '/quizzes'
   ```

#### Detailed Information

```
GET '/categories'
- Gets a key-value pair json object, key being the ID and value being the type of the category
- Request Arguments: None
- Response: JSON object with key (Category ID): Value (Category Type), count and success
- Sample
    {
      "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
      },
      "count": 6,
      "success": true
    }

GET '/categories/<int:category_id>/questions'
- Gets an array of json objects of questions belonging to the requested category
- Request Arguments: Flask named parameter (1 in this sample)
- Response: JSON object with current_category, questions (an array), total_questions
  and success
- Sample
    {
      "current_category": 1,
      "questions": [
        {
          "answer": "Muhammad Ali",
          "category": 1,
          "difficulty": 4,
          "id": 2,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Uruguay",
          "category": 1,
          "difficulty": 6,
          "id": 7,
          "question": "Which country won the first ever soccer World Cup in 1930?"
        }
      ],
      "success": true,
      "total_questions": 2
    }

GET '/questions'
- Gets a JSON object of categories and an array of JSON objects holding questions
- Request Arguments: None
- Response: categories (A JSON object), questions (List of JSON objects holding questions),
  total_questions and success
- Sample
    {
      "categories": {
        "1": "Science",
        "2": "Art",
      },
      "questions": [
        {
          "answer": "Muhammad Ali",
          "category": 1,
          "difficulty": 4,
          "id": 2,
          "question": "What boxer's original name is Cassius Clay?"
        },
        {
          "answer": "Apollo 13",
          "category": 3,
          "difficulty": 5,
          "id": 3,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 5,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
      ],
      "success": true,
      "total_questions": 3
    }

POST '/questions'
- Creats a new questions based on JSON data received
- Request Arguments: None (but needs a JSON object of new question as data)
- Response: new_question (JSON object) and success
- Sample
    {
        'success': True,
        'new_question': {
              "answer": "Tom Cruise",
              "category": 5,
              "difficulty": 5,
              "id": 4,
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }
    }

POST '/questions/search'
- Get matching (case-insensitive) questions in the form of JSON objects
- Request Arguments: None (but needs a JSON object holding a key "searchTerm")
- Response: A JSON object with success, total_questions and questions (array)
- Sample
    {
        'success': True,
        'total_questions': 1,
        'questions': [
            {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 5,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }
        ]
    }

DELETE '/questions/<int:question_id>'
- Deletes an existing question from the database
- Request Arguments: Flask named parameter (1 in this sample)
- Response: A JSON object with success and question_id which was deleted
- Sample
    {
        'success': True,
        'question_id': 1
    }

POST '/quizzes'
- Gets a random (non repeating) question based on category given
- Request Arguments: None (but a json object with key 'quiz_category' and value
  holding a category JSON object)
- Response: A JSON object with success and question JSON object
- Sample
    {
        'success': True,
        'question': {
                "answer": "Tom Cruise",
                "category": 5,
                "difficulty": 5,
                "id": 4,
                "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            }
    }
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
python test_flaskr.py
```