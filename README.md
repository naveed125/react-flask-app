# React Flask App
A simple application build using JavaScript/React frontend and Python/Flask backend. 

# Start
```
% docker-compose up -d
Creating network "react-flask-app_default" with the default driver
Creating react-flask-app_db_1     ... done
Creating react-flask-app_client_1 ... done
Creating react-flask-app_server_1 ... done
```

# Initialize the sample database
```
% docker exec -it react-flask-app_db_1 mongo /scripts/InitDB.js
MongoDB shell version v4.2.6
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session ...
MongoDB server version: 4.2.6
Inserting: 1 Imagination is more important than knowledge. Knowledge is limited. Imagination encircles the world
Inserting: 2 Try not to become a man of success, but rather try to become a man of value
Inserting: 3 Life is like riding a bicycle. To keep your balance you must keep moving
Inserting: 4 Look deep into nature, and then you will understand everything better
Inserting: 5 Logic will get you from A to B. Imagination will take you everywhere
Inserting: 6 Insanity is doing the same thing over and over again and expecting different results
Inserting: 7 The hardest thing to understand in the world is the income tax
```

# Further reading
Complete description is in [this medium post](https://medium.com/@naveed125/up-and-running-with-react-flask-and-mongodb-in-5-minutes-or-less-e9bd038d2bee).
