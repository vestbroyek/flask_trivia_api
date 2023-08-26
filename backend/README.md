# Trivia API 
This API can be used to retrieve and post trivia questions in a variety o categories. It also powers a React web app. 

The API has endpoints for retrieving available categories, all questions for a specific category, for retrieving, posting, and deleting questions, and for initiating a trivia quiz (see API Reference below).

## Table of contents
1. [Getting started](#getting-started)
    1. [The backend](#the-backend)
        1. [The database](#the-database)
        2. [Flask](#flask)
    2. [The frontend](#the-frontend)
    3. [Tests](#tests)
2. [API reference](#api-reference)
    1. [/categories - GET](#categories--get)
    2. [/categories/category_id/questions - GET](#categoriescategory_idquestions--get)
    3. [/questions - GET](#questions--get)
    4. [/questions - POST](#questions--post)
    5. [/questions/question_id - DELETE](#questionsquestion_id---delete)
    6. [/questions/search - POST](#questionssearch--post)
    7. [/quizzes - POST](#quizzes--post)


## Getting started 
To get started with the API, you'll need to set up both the backend and the frontend.

### The backend
#### The database
To set up your database, run a Postgres container (or set up a local server) with 

`docker run -p 5432:5432 -e POSTGRES_USER=student -e POSTGRES_PASSWORD=password -e POSTGRES_DB=trivia postgres`

This will map your machine's port 5432 to the container's 5432, so you will be able to access the database, called `trivia`, at `localhost:5432`, with username `student` and password `password`. 

Then, in the database, run `backend/trivia_init.sql` to create the tables and set up permissions.

#### Flask
To get the API running, make a virtual environment, navigate to the `backend` folder, and install dependencies with `pip3 install -r requirements.txt`. Note that these dependencies have been tested with Python 3.10.9. If you are using a different version (especially <3.10), you may need to tweak the versions on Flask, flask-sqlalchemy, SQLAlchemy, and Jinja2.

Next, from the `backend` folder, ensure you run `export FLASK_APP=flaskr` and then run `flask run`. The app is defined in `__init__.py`. 

### The frontend
From the `frontend` folder, run `npm install`. (If you don't have npm installed, run `brew install node` or similar for your OS first). Then run `npm start`. You should now be able to access `localhost:3000` and see the app. 

### Tests
Tests are defined in `backend/test_flaskr.py`. They rely on having a test database set up. This is expected to be called `test_trivia`. To run tests, first create the database by running `create database test_trivia`, editing your connection to connect to this database (instead of to `trivia`, the "production" database), and re-run `trivia_init.sql`. 

Now you can run `test_flaskr.py`. 

## API reference
### Getting started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Endpoints

#### /categories - GET
- Functionality
    - Returns:
        - `categories: list`: a list of categories, each with an `id: int` and `type: str`
        - `success: bool`: successful status
- Sample
    - Request: `curl localhost:5000/categories`
    - Response:
    <details>
    <summary>Click to expand</summary>

        ```json
        {
        "categories": [
            {
            "id": 1,
            "type": "Science"
            },
            {
            "id": 2,
            "type": "Art"
            },
            {
            "id": 3,
            "type": "Geography"
            },
            {
            "id": 4,
            "type": "History"
            },
            {
            "id": 5,
            "type": "Entertainment"
            },
            {
            "id": 6,
            "type": "Sports"
            }
        ],
        "success": true
        }
        ```
        </details>

#### /categories/category_id/questions - GET
- Functionality
    - Requires:
        - `category_id: int`: a category ID whose questions you'd like to return
    - Returns:
        - `current_category: str`: the category you requested the questions for
        - `questions: list`: a list of questions
        - `success: bool`: successful status
        - `total_questions: int`: the number of questions returned
    - Raises:
        - 404 Not found: if the category ID does not exist
- Sample
    - Request: `curl localhost:5000/categories/4/questions`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {
    "current_category": "History",
    "questions": [
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
        },
        {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
        "answer": "The sky",
        "category": 4,
        "difficulty": 1,
        "id": 28,
        "question": "What's up?"
        },
        {
        "answer": "The sky",
        "category": 4,
        "difficulty": 1,
        "id": 29,
        "question": "What's up?"
        },
        {
        "answer": "The sky",
        "category": 4,
        "difficulty": 1,
        "id": 30,
        "question": "What's up?"
        }
    ],
    "success": true,
    "total_questions": 7
    }
    ```
    </details>

#### `/questions - GET`
- Functionality
    - Requires:
        - `page: int`: a page number (optional)
    - Returns:
        - `success: bool`: Successful status
        - `questions: list`: A list of questions
        - `total_questions: int`: Total questions available
        - `categories: list`: The categories

- Sample
    - Request: `curl localhost:5000/questions?page=1`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {
    "categories": [
        {
        "id": 1,
        "type": "Science"
        },
        {
        "id": 2,
        "type": "Art"
        },
        {
        "id": 3,
        "type": "Geography"
        },
        {
        "id": 4,
        "type": "History"
        },
        {
        "id": 5,
        "type": "Entertainment"
        },
        {
        "id": 6,
        "type": "Sports"
        }
    ],
    "questions": [
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "id": 12,
        "question": "Who invented Peanut Butter?"
        },
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
        },
        {
        "answer": "Escher",
        "category": 2,
        "difficulty": 1,
        "id": 16,
        "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 21
    }
    ```
    </details>

#### `/questions - POST` 
- Functionality
    - Requires: 
        - `question: str`: A question
        - `answer: str`: The answer
        - `difficulty: int`: The difficulty, 1-5
        - `category: str`: The category, 1-6 
    - Returns:
        - `success: bool`: Successful status
    - Raises:
        - 400 Bad request: if one or more of the above keys is not provided
        - 500 Server error: any other errors while processing the request
- Sample
    - Request: `curl -X POST -H "Content-Type: application/json" -d '{"question": "What is up?", "answer": "The sky", "difficulty": 4, "category": 1}' localhost:5000/questions`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {"success":true}
    ```
    </details>

#### `/questions/question_id - DELETE`
- Functionality
    - Requires:
        - `question_id: int`
    - Returns: 
        - `success: bool`: Successful status
    - Raises:
        - 404 Not found: If no question matches the provided ID
        - 422 Unprocesseable: Any other issues while processing the request

- Sample
    - Request: `curl -X DELETE -H "Content-Type: application/json" localhost:5000/questions/11`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {"success":true}
    ```
    </details>

#### `/questions/search - POST`
- Functionality
    - Requires:
        - `search_term: str`: A search term. 
            - Search for substrings 
    - Returns:
        - `success: bool`: Successful status
        - `questions: list`: A list of matching questions
        - `total_questions: int`: The number of matching questions
- Sample
    - Request: ` curl -X POST -H "Content-Type: application/json" -d '{"search_term": "title"}' localhost:5000/questions/search`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {
    "questions": [
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 2
    }
    ```
    </details>

#### `/quizzes - POST`
- Functionality
    - Requires:
        - `previous_questions: list`: Previously played question IDs
        - `quiz_category: dict`: The desired category 
    - Returns:
        - `success: bool`: Successful status
        - `question: dict`: A randomly chosen question
    - Raises:
        - 400 Bad request: If either of the required parameters is not supplied
- Sample
    - Request: `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"id": 1, "type": "Science"}}' localhost:5000/quizzes`
    - Response: 
    <details>
    <summary>Click to expand</summary>

    ```json
    {
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "success": true
    }
    ```
    </details>

### Error handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "Bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 500: Server error