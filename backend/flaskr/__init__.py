import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='postgresql://student:password@localhost:5432/trivia',
        FLASK_ENV="development",
        DEBUG=True
    )
    
    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Set up CORS
    #TODO update resources regex
    CORS(app, resources={r"*" : {'origins': '*'}})

    # Set up after-request logic
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    # GET available categories
    @app.route('/categories', methods=['GET'])
    def get_categories():

        categories = Category.query.all()

        # Format
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Get page
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE 
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        # categories = [question.category for question in questions]

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            "success": True,
            "questions": formatted_questions[start:end],
            "total_questions": len(formatted_questions),
            "categories": formatted_categories,
            "current_category": formatted_categories[0]
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({
                "success": True
            })
        
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_question():
        # Grab JSON 
        try:
            question, answer, difficulty, category = request.json['question'], request.json['answer'], request.json['difficulty'], request.json['category'] 
            
        except KeyError:
            abort(400)

        # Create new question
        new_question = Question(question, answer, difficulty, category)
        new_question.insert()

        return jsonify({
            "success": True
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        # Get search term
        query = request.json['search_term']

        # Search db
        result = Question.query.filter(Question.question.icontains(query))
        formatted_result = [question.format() for question in result]

        if not result:
            abort(404)
        
        else:
            return jsonify({
                "success": True,
                "questions": formatted_result,
                "total_questions": len(formatted_result),
                "current_category": "science"
            })


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        # get all relevant questions
        result = Question.query.filter(Question.category == category_id)
        formatted_result = [question.format() for question in result]

        if not result:
            abort(404)

        return jsonify({
            "success": True,
            "questions": formatted_result,
            "total_questions": len(formatted_result),
            "current_category": "science"
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def start_quiz():
        # Get previous questions and the desired category
        previous_questions = request.json['previous_questions']
        excluded_ids = [question.id for question in previous_questions]
        quiz_category = request.json['quiz_category']

        # Filter existing questions
        questions = Question.query.filter(
            Question.category == quiz_category,
            Question.id.notin_(excluded_ids)
        )

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            "success": True,
            "questions": formatted_questions
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
            }), 400

    return app

