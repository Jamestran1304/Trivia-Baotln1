import json
import os
import sys
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
category_data_type = {
    "id": None,
    "type": None
}
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the DONEs
    '''
    CORS(app)
    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        # response.headers.add('Access-Control-Allow-Credentials','true')
        response.headers.add('Access-Control-Allow-Origin',"*")
        return response 

    '''
    @DONE: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories', methods = ['GET'])
    def get_question_category():
        try:
            categories = {}
            category_queried_list = Category.query.all()
            for item in category_queried_list:
                categories[item.id] = item.type
        except:
            print(sys.exc_info())
            return jsonify({"categories" : categories, "success": True})

    '''
    @DONE: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions', methods = ['GET'])
    def get_question_handler():
        question_list_formatted = []
        category_list_formatted = {}
        try:
            question_list = Question.query.order_by(db.asc(Question.id)).all()
            category_list = Category.query.order_by(db.asc(Category.id)).all()
            page_number = request.args.get('page', 1, type=int)
            start = (page_number - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE
            for item in question_list:
                temp = Question(question=item.question, answer=item.answer, 
                                category=item.category, difficulty=item.difficulty).format()
                temp["id"] = item.id
                question_list_formatted.append(temp)
            if len(question_list_formatted[start:end]) == 0:
                abort(404)
            for item in category_list:
                category_list_formatted[item.id] = item.type
        except:
            print(sys.exc_info())
            return jsonify({
            "questions": question_list_formatted[start:end],
            "total_questions": len(question_list_formatted),
            "categories": category_list_formatted,
            "current_category": str(1),
            "success": True
            })
        
    '''
    @DONE: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods = ['DELETE'])
    def question_delete_handler(question_id):
        try:
            question = Question.query.filter_by(id = question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({'success': True})
        except:
            print(sys.exc_info())
            abort(422)
    '''
    @DONE: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    @app.route('/questions', methods=['POST'])
    def question_create_handler():
        question_info = json.loads(request.data)
        if question_info is None or question_info["answer"] == "" or question_info["question"] == "":
            abort(404)
        try:
            Question(question = question_info["question"], answer = question_info["answer"], 
                                category = question_info["category"], difficulty = question_info["difficulty"]).insert()
        except:
            print(sys.exc_info())
            abort(422)
            return jsonify({"success": True})
  
    '''
    @DONE: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions/search-action', methods=['POST'])
    def search_question_handler():
        search_term = {}
        searched_question_formatted = []
        searched_category = 0
        search_term = json.loads(request.data)
        if search_term["searchTerm"] == '':
            abort(404)
        try:
            searched_question = Question.query.filter_by(question = search_term["searchTerm"]).all()
            for item in searched_question:
                temp = Question(question=item.question, answer=item.answer, 
                                category=item.category, difficulty=item.difficulty).format()
                temp["id"] = item.id
                searched_question_formatted.append(temp)
                
            if len(searched_question_formatted) != 0:
                searched_category = searched_question_formatted[0]["category"]
        except:
            print(sys.exc_info())
            abort(422)
            return jsonify({
            "questions": searched_question_formatted,
            "total_questions": len(searched_question_formatted),
            "current_category": str(searched_category),
            "success": True
            })
    '''
    @DONE: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    @app.route('/categories/<int:category_id>/questions', methods = ['GET'])
    def get_categorical_questions(category_id):
        question_list_formatted = []
        try:
            category_id = str(category_id)
            question_list = db.session.query(Question).filter_by(category = category_id).order_by(db.asc(Question.id)).all()
            if len(question_list) == 0:
                abort(404)
            for item in question_list:
                temp = Question(question=item.question, answer=item.answer, 
                                category=item.category, difficulty=item.difficulty).format()
                temp["id"] = item.id
                question_list_formatted.append(temp)
        except:
            print(sys.exc_info())
            abort(422)
            return jsonify({
            "questions": question_list_formatted, 
            "total_questions": len(question_list_formatted),
            "current_category": str(category_id),
            "success": True
            })

    '''
    @DONE: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods = ['POST'])
    def get_quiz_questions():
        quizz_info = json.loads(request.data)
        question = {}
        quizz_list = []
        unanswer_question_list = []
        random_question_id = 1
        if quizz_info is None or quizz_info["quiz_category"]["id"] is None:
            abort(404)
        try:
            if quizz_info["quiz_category"]["id"] == 0:
                quizz_list = Question.query.order_by(db.asc(Question.id)).all()
                if len(quizz_list) == 0:
                    print("App must have at least one question")
            else:
                question_category_id = quizz_info["quiz_category"]["id"]
                quizz_list = Question.query.filter_by(category = question_category_id).order_by(db.asc(Question.id)).all()
                if len(quizz_list) == 0:
                    print("Category must have at least one question")
                for item in quizz_list:
                    if item.id not in quizz_info["previous_questions"]:
                        unanswer_question_list.append(item)
                if len(unanswer_question_list) != 0:
                    question =  Question(question = unanswer_question_list[0].question, answer = unanswer_question_list[0].answer,
                                        category = unanswer_question_list[0].category, difficulty = unanswer_question_list[0].difficulty).format()
                    question["id"] = unanswer_question_list[0].id
                else: 
                    question = None
        except:
            print(sys.exc_info())
            abort(422)
            return jsonify({"question": question, "success": True})
    '''
    @DONE: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({"success": False, "error": 404, "message": "resource not found"}),404,)
    
    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)
    
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({"success": False, "error": 422, "message": "unprocessable"}),422)
    
    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405)
    
    return app
