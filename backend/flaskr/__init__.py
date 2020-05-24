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

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        # Check if we have any questions
        #   if yes
        #       then
        #       404 - if out of bound page number (like 1000th page for 2 questions)
        #       200 - else wise
        #   else (no questions)
        #       404 - if its not the first page
        #       200 - else wise
        if len(formatted_questions) != 0:
            if start >= len(formatted_questions):
                abort(404)
            else:
                paginated_questions = formatted_questions[start:end]

                return jsonify({
                    "success": True,
                    "questions": paginated_questions,
                    "total_questions": len(formatted_questions),
                    "categories": formatted_categories,
                    "current_category": None
                })
        else:
            if page_number > 1:
                abort(404)
            else:
                return jsonify({
                    "success": True,
                    "questions": [],
                    "total_questions": 0,
                    "categories": formatted_categories,
                    "current_category": None
                })

    # Delete a Question (cruD - Using DELETE)
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get_or_404(question_id)

        try:
            question.delete()
            return jsonify({
                "success": True,
                "question_id": question.id
            })
        except Exception:
            abort(500)

    # Create a new Question (Crud - Using POST)
    @app.route("/questions", methods=['POST'])
    def create_question():
        data = request.get_json()
        expected_data_keys = sorted(['question', 'answer', 'category', 'difficulty'])

        # Checking if all the columns(keys) exist in the incoming data
        if sorted([key for key in data]) == expected_data_keys:
            new_question = Question(**data)
            try:
                new_question.insert()
                return jsonify({
                    'success': True,
                    'new_question': new_question.format()
                }), 201
            except Exception:
                abort(500)
        else:
            abort(400)

    # Get a Question based on Search term (cRud - Using POST)
    @app.route("/questions/search", methods=['POST'])
    def search_question():
        data = request.get_json()

        if "searchTerm" in data:
            questions = Question.query.filter(Question.question.ilike(f"%{data['searchTerm']}%"))
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'total_questions': len(formatted_questions),
                'questions': formatted_questions
            })
        else:
            abort(400)

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

    # --- Error Handlers --- #
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
