from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

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
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            "count": len(formatted_categories),
            "categories": formatted_categories
        })

    # Get Questions based on Category (cRud - Using GET)
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        category = Category.query.get_or_404(category_id)
        questions = category.questions
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(formatted_questions),
            "current_category": category.id,
        })

    # --- Question Resource Endpoints --- #

    # Get All Questions (cRud - Using GET)
    @app.route("/questions")
    def get_all_questions():
        page_number = request.args.get("page", 1, type=int)
        start = QUESTIONS_PER_PAGE * (page_number - 1)
        end = start + QUESTIONS_PER_PAGE

        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
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
            category = data.pop('category')
            new_question = Question(**data)

            try:
                new_question.category = Category.query.get(category)
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

    # Get a questions based on category and previous questions asked
    # Using POST
    @app.route("/quizzes", methods=['POST'])
    def get_quiz_question():
        data = request.get_json()

        if data['quiz_category']['id'] == 0:
            category_questions = Question.query.all()
        else:
            category = Category.query.get_or_404(data['quiz_category']['id'])
            category_questions = category.questions

        question_ids = [question.id for question in category_questions]
        unused_question_ids = [qid for qid in question_ids if qid not in data['previous_questions']]

        if len(unused_question_ids) > 0:
            question = Question.query.get(random.choice(unused_question_ids))
            return jsonify({
                'success': True,
                'question': question.format()
            }), 200
        else:
            return jsonify({
                'success': True,
                'question': None
            }), 200

    # --- Error Handlers --- #
    @app.errorhandler(404)
    def not_found(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        print(error)
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
