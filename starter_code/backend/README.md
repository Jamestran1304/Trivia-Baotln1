Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, ` http://localhost:3000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /cateogry
- General:
    - Returns a list of cateogries to register new question, to get categorical questions. Return a list of categories, success value.
- Sample: `curl http://localhost:3000/categories`

```{
	"categories" : {"1": "Math"},
	"success": True
}
```

#### GET /questions
- General:
    - Return a list of question, number of returned questions, a list of categories, id of a particular category, success value. api parameter page is used for pagination.
- `curl http://localhost:3000/questions?page=1`
```
{
      "questions": [{"question": "1 + 1 = ?", "answer": "2", "category": "test_data", "difficulty": 1, id: 1}],
      "total_questions": 1,
      "categories": {"1": "Math"},
      "current_category": "1",
      "success": True
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Return the success value.
- `curl -X DELETE http://localhost:3000/questions/4`
```{
	"success": True
}
```

#### POST /questions
- General:
    - If provided, create question in the database. Returns the success value. 
- `curl http://localhost:3000/questions -X PATCH -H "Content-Type: application/json" -d '{"question":"","answer":"","difficulty":1,"category":1}'`
```
{
"question":"what is 'use strict' in JavaScript?",
"answer":"apply stricter encoding and error handling of the JavaScript code at runtime on a limited basis.",
"difficulty":1,"category":1
}
```



#### POST /questions/search-action
- General:
    - If provided, search question that matches the searchTerm property. Returns the success value. 
- `curl http://localhost:3000/questions/search-action -X PATCH -H "Content-Type: application/json" -d '{"searchTerm":""}'`
```
{
 "questions": [{"question": "1 + 1 = ?", "answer": "2", "category": "test_data", "difficulty": 1, id: 1}],
 "total_questions": 1,
 "current_category": "1",
  "success": True
}
```

#### POST /categories/{category_id}/questions
- General:
    -  Return a random questions within the given category, if provided, and that is not one of the previous questions.
- `curl http://localhost:3000/quizzes -X PATCH -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"JavaScript","id":"1"}}`
```
{
  "question": {
    "answer": "D", 
    "category": "1", 
    "difficulty": 4, 
    "id": 4, 
    "question": "what is async and await in the JavaScript?"
  }, 
  "success": true
}


```
