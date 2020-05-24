import unittest
import json

from flaskr import create_app
from models import setup_db, Question, Category


def insert_dummy_data():
    """Utility function to insert dummy data"""
    dummy_question = {
        'question': 'A dummy question ?',
        'answer': 'Dummy answer',
        'category': 1,
        'difficulty': 1
    }

    sample_question = Question(**dummy_question)
    sample_question.insert()

    return sample_question.id


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)
        self.database_name = "trivia_test"
        self.database_host = "localhost:5432"
        self.username_pwd = "biswas:T@me0302"
        self.database_path = "postgresql://{}@{}/{}".format(self.username_pwd, self.database_host, self.database_name)
        setup_db(self.app, self.database_path)
        self.client = self.app.test_client

    def tearDown(self):
        """Executed after reach test"""
        pass

    # --- Tests for Category resource endpoints --- #

    def test_get_all_categories(self):
        """
        Test to verify GET /categories endpoint
        status codes: 200
        exceptions: None
        """
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])

    # --- Tests for Question resource endpoints --- #

    def test_get_all_questions(self):
        """
        Test to verify GET /questions endpoint
        status codes: 200, 404
        exceptions: ResourceNotFound
        """
        # 200 test
        res = self.client().get("/questions?page=1")
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])

        # 404 test
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual("resource not found", data['message'])

    def test_delete_question(self):
        """
        Test to verify DELETE /questions/<question_id> endpoint
        status codes: 200, 404, 500
        exceptions: ResourceNotFound, InternalServerError
        """
        # Inserting sample data into database
        question_id = insert_dummy_data()

        # 200 test
        res = self.client().delete('/questions/' + str(question_id))
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertEqual(question_id, data['question_id'])

        # 404 test
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual("resource not found", data['message'])

    def test_create_question(self):
        """
        Test to verify DELETE /questions/<question_id> endpoint
        status codes: 201, 400, 500
        exceptions: BadRequest, InternalServerError
        """
        # 201 test
        dummy_question = {
            'question': 'A second dummy question ?',
            'answer': 'Second dummy answer',
            'category': 1,
            'difficulty': 1
        }
        res = self.client().post("/questions", json=dummy_question)
        data = json.loads(res.data)

        self.assertEqual(201, res.status_code)
        self.assertTrue(data['success'])
        self.assertEqual(dummy_question['question'], data['new_question']['question'])

        # 400 test
        bad_dummy_question = {
            'question': 'A bad dummy question ?',
            'difficulty': 1
        }
        res = self.client().post("/questions", json=bad_dummy_question)
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertFalse(data['success'])
        self.assertEqual("bad request", data['message'])

    def test_search_question(self):
        """
        Test to verify POST /questions for search functionality
        status codes: 200, 400
        exceptions: BadRequest
        """
        # 200 test
        search_data = {
            "searchTerm": "dummy"
        }
        res = self.client().post("/questions/search", json=search_data)
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'])
        self.assertTrue(data['total_questions'] >= 0)
        self.assertIsNotNone(data['questions'])

        # 400 test
        bad_search_data = {
            "searchTTTTerm": "dummy"
        }
        res = self.client().post("/questions", json=bad_search_data)
        data = json.loads(res.data)

        self.assertEqual(400, res.status_code)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
