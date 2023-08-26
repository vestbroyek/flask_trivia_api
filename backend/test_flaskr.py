import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": "postgresql://student:password@localhost/test_trivia"
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        resp = self.client.get("/categories")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["success"])

    def test_get_questions_success(self):
        resp = self.client.get("/questions?page=1")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["success"])

    def test_get_questions_non_int_page(self):
        # Should return page 1 rather than error
        resp = self.client.get("/questions?page=hello")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["success"])

    def test_get_questions_non_existent_page(self):
        # Should not return any questions but still succeed
        resp = self.client.get("/questions?page=999")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["success"])
        # Empty lists are falsy
        self.assertFalse(resp.json["questions"])

    # def test_delete_question_success(self):
    #     resp = self.client.delete("/questions/4")

    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue(resp.json["success"])

    def test_delete_question_error(self):
        resp = self.client.delete("/questions/999")
        resp2 = self.client.delete("/questions/hello")

        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp2.status_code, 404)

    def test_post_question_success(self):
        resp = self.client.post(
            "/questions",
            data=json.dumps(
                {
                    "question": "What's up?",
                    "answer": "The sky",
                    "difficulty": 5,
                    "category": 1,  # science
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["success"])

    def test_post_question_key_error(self):
        resp = self.client.post(
            "/questions",
            # Test KeyError (400)
            data=json.dumps(
                {"question": "What's up?", "answer": "The sky", "difficulty": 5}
            ),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.json["success"])

    def test_post_question_server_error(self):
        resp = self.client.post(
            "/questions",
            # Test server error
            data=json.dumps(
                {
                    "question": "What's up?",
                    "answer": "The sky",
                    "difficulty": "banana",
                    "category": 2,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 500)
        self.assertFalse(resp.json["success"])

    def test_post_search_question_success(self):
        resp = self.client.post(
            "/questions/search",
            data=json.dumps({"search_term": "title"}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["questions"])
        self.assertIsNotNone(resp.json["total_questions"])
        self.assertIsNotNone(resp.json["current_category"])

    def test_post_search_question_key_error(self):
        resp = self.client.post(
            "/questions/search",
            # Test KeyError
            data=json.dumps({"search": "title"}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)

    def test_post_search_question_not_found_error(self):
        resp = self.client.post(
            "/questions/search",
            # Test KeyError
            data=json.dumps({"search_term": "456543454dfgfds"}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 404)

    def test_get_questions_by_category_success(self):
        resp = self.client.get("/categories/1/questions")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json["questions"])
        self.assertTrue(resp.json["success"])

    def test_get_questions_by_category_not_found_error(self):
        resp = self.client.get("/categories/99/questions")

        self.assertEqual(resp.status_code, 404)
        self.assertFalse(resp.json["success"])

    # TODO test /quizzes


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
