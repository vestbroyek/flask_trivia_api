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
        SQLALCHEMY_DATABASE_URI="postgresql://student:password@localhost:5432/trivia",
        FLASK_ENV="development",
        DEBUG=True,
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Set up CORS
    # TODO update resources regex
    CORS(app, resources={r"*": {"origins": "*"}})

    # Set up after-request logic
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )

        return response

    # GET available categories
    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()

        # Format
        formatted_categories = [category.format() for category in categories]

        return jsonify({"success": True, "categories": formatted_categories})

    @app.route("/questions", methods=["GET"])
    def get_questions():
        # Get page
        page = request.args.get("page", 1, type=int)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + 10

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]

        # categories = [question.category for question in questions]

        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        # "Current category" is required in spec but unclear why
        return jsonify(
            {
                "success": True,
                "questions": formatted_questions[start:end],
                "total_questions": len(formatted_questions),
                "categories": formatted_categories,
            }
        )

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()

            return jsonify({"success": True})

        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def post_question():
        # Grab JSON
        try:
            question, answer, difficulty, category = (
                request.json["question"],
                request.json["answer"],
                request.json["difficulty"],
                request.json["category"],
            )

        except KeyError:
            abort(400)

        try:
            # Create new question
            new_question = Question(question, answer, difficulty, category)
            new_question.insert()
        except:
            # Catch all exceptions if the keys are present but something else fails
            abort(500)

        return jsonify({"success": True})

    @app.route("/questions/search", methods=["POST"])
    def search_question():
        # Get search term
        try:
            query = request.json["search_term"]
        except KeyError:
            abort(400)

        # Search db
        result = Question.query.filter(Question.question.icontains(query))
        formatted_result = [question.format() for question in result]

        return jsonify(
            {
                "success": True,
                "questions": formatted_result,
                "total_questions": len(formatted_result),
            }
        )

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_by_category(category_id):
        # get all relevant questions
        result = Question.query.filter(Question.category == category_id)
        formatted_result = [question.format() for question in result]

        # get current category
        category = Category.query.filter(Category.id == category_id).one_or_none()

        if not formatted_result or not category:
            abort(404)

        formatted_category = category.format()

        return jsonify(
            {
                "success": True,
                "questions": formatted_result,
                "total_questions": len(formatted_result),
                "current_category": formatted_category["type"],
            }
        )

    @app.route("/quizzes", methods=["POST"])
    def start_quiz():
        # Get previous questions and the desired category
        try:
            previous_questions = request.json["previous_questions"]
            quiz_category = request.json["quiz_category"]["id"]
        except KeyError:
            abort(400)

        # Filter existing questions
        questions = Question.query.filter(
            Question.category == quiz_category, Question.id.notin_(previous_questions)
        )

        formatted_questions = [question.format() for question in questions]

        return jsonify(
            {"success": True, "question": random.choice(formatted_questions)}
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(422)
    def unprocesseable(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Request could not be processed",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Server error",
                }
            ),
            500,
        )

    return app
