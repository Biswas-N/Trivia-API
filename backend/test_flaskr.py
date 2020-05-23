import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


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
        #
        # # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
        Test cases for Category resource endpoints
    """

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

    """
        Test cases for Question resource endpoints
    """

    def test_get_all_questions(self):
        """
        Test to verify GET /questions endpoint
        status codes: 200, 404
        exceptions: PageNotFound
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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()