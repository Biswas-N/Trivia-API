from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=False):
    # create and configure the app
    app = Flask(__name__)
    if not test_config:
        setup_db(app)

    # Enabling Cross Origin Resource Sharing to Flask app
    CORS(app=app)

    # Setting response header to allow all Origins
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    # --- Category Resource Endpoints --- #

    # Get All Categories (cRud - Using GET)
    @app.route("/categories")
    def get_all_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            "success": True,
            "count": len(formatted_categories),
            "categories": formatted_categories
        })

    # --- Question Resource Endpoints --- #

    # Get All Questions (cRud - Using GET)
    @app.route("/questions")
    def get_all_questions():
        page_number = request.args.get("page", 1, type=int)
        start = QUESTIONS_PER_PAGE * (page_number - 1)
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        paginated_questions = formatted_questions[start:end]

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            "success": True,
            "questions": paginated_questions,
            "total_questions": len(formatted_questions),
            "categories": formatted_categories,
            "current_category": None
        })
    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    return app
