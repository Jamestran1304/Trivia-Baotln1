import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.mock_question = {"question": "1 + 1 = ?", "answer": "2", "category": "test_data", "difficulty": 1}
        self.mock_quizz = {"previous_questions":[], "quiz_category":{"type":"click", "id": 1}}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    #test get question success when application starts
    def test_get_question_handler_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 10)
        self.assertGreaterEqual(len(data["categories"]), 0)
        self.assertGreaterEqual(data["total_questions"], 0)
    
    #test get question fail when application starts
    def test_404_failed_get_question_handler(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    #test question_delete_handler success
    def test_question_delete_handler_success(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    #test question_delete_handler error
    def test_422_failed_question_delete_handler(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def test_404_failed_question_delete_handler(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    #test create question success
    def test_question_create_handler_success(self):
        res = self.client().post('/questions', json = self.mock_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        
    #test create question error
    def test_404_failed_question_create_handler(self):
        res = self.client().post('/questions', json = {"question": "", "answer": "", "category": "Math", "difficulty": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_422_failed_question_create_handler(self):
        res = self.client().post('/questions', json = {"question": "", "answer": "", "category": "Math", "difficulty": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    # test search question success
    def test_search_question_handler_success(self):
        res = self.client().post('/questions/search-action', json = {"searchTerm": "test_data"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 0)
        self.assertGreaterEqual(data["total_questions"], 0)
        self.assertGreaterEqual(data["current_category"], str(0))
        
    # test search question error
    def test_404_failed_search_question_handler(self):
        res = self.client().post('/questions/search-action', json = {"searchTerm": ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_422_failed_search_question_handler(self):
        res = self.client().post('/questions/search-action', json = {"searchTerm": ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    #test get_categorical_questions success
    def test_get_categorical_questions_success(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertGreaterEqual(len(data["questions"]), 0)
        self.assertGreaterEqual(data["total_questions"], 0)
        self.assertGreaterEqual(data["current_category"], str(0))
    
    #test get_categorical_questions error
    def test_404_get_categorical_questions_success(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_422_get_categorical_questions_success(self):
        res = self.client().get('/categories/9/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    # test get quiz questions success
    def test_get_quiz_questions_success(self):
        res = self.client().post('/quizzes', json = self.mock_quizz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(data)
        
    #test get quiz questions error
    def test_400_failed_get_quiz_questions(self):
        res = self.client().post('/quizzes', json = {"previous_questions":[], "quiz_category":{"type":"click", "id": None}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_422_failed_get_quiz_questions(self):
        res = self.client().post('/quizzes', json = {"previous_questions":[], "quiz_category":{"type":"click", "id": None}})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()