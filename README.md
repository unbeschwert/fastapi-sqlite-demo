# Introduction
This was a coding exercise for an interview. 

# Installation
1. Execute the following code:
    ```
    git clone https://github.com/unbeschwert/backend-exercise-I.git backend
    cd backend
    python3 -m venv VirtualEnv
    source VirtualEnv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
2. Type the URL : ```http://127.0.0.1:8000/docs```

# Thought process
1. Sqlite3 is not thread-safe. Hence, requests should be seralized without performance penalty which is not done in this project. I used it mainly to refresh my SQL knowledge
2. I couldn't think of a better way to implement the ```modify_user()``` in ```Database``` class.
3. Rate limiting the user is not implemented. Could be interesting to implement it. 
4. I chose to implement using python virtual environment and not docker to make it easy for code analysis and review.
5. I have chosen to 3.9 as my base since I tested the program on both Debian 11 and Ubuntu 22.04.
6. I have chosen an in-memory database just for testing purposes. If persistence is desired then the name of db can be changed from ":memory:" to "users.db" for example.
