# Back-End API Development using Flask and Flask Restful

To support the back-end of the program, a Restful API is made.

<br>

## Summary

Made for StarWord - Bangkit 2022 Company-based Capstone of C22-FV01, this API mainly focuses on predicting the input data from the user, by providing pipeline for the pre-made TensorFlow model saved in H5 format to predict the feedback's validity.

Improving further, some supporting features are added in this API. This supporting feature consists of ILT CRUD for admin page, ILT Feedback deletion, and download in CSV format.

<br>

## Main Dependencies

Below are the explanation of each of the main frameworks used in this Restful API, along with the explanation and the reason of choice.
<br>

### 1. [Flask & Flask Restful](https://flask-restful.readthedocs.io/en/latest/)

Heart of this restful API. This micro-framework excels in API development, especially since it is written in Python, it saves time and effort to build pipeline for the model. The “micro” in microframework means Flask aims to keep the core simple but extensible. Flask won’t make many decisions for their users.
<br>

### 2. [SQLAlchemy](https://www.sqlalchemy.org/)

SQLAlchemy plays role in database-related commands. It is ORM for Flask, and fits well with the Flask framework.
<br>

### 3. [TensorFlow](https://www.tensorflow.org/)

Primarily utilizated in the predicting section. TensorFlow is made use from the input sequencing and padding process, until the prediction result extraction.

## How to Download and Host

This section is the steps to run StarWord API on local and deploy it to Google Cloud Platform and Heroku which will be explained with a short code.

<br>

### Run StarWord API on local

#### 1. Clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 2. Go to the cc-development branch and install virtualenv

```
pip install virtualenv
```

#### 3. Create and name a virtual environment

```
python -m venv <name of environment>
```

#### 4. Activate the environment

```
<name of environment>\Scripts\activate
```

#### 5. Install all required packages for this API

```
pip install -r requirements.txt
```

#### 6. Create database, then run python from the terminal and create database table based from the app.py model

```
>>> from app import db
>>> db.create_all()
>>> exit()
```

#### 7. Add debug mode to keep reloading server (only for development)

```
if __name__ == "__main__":
  app.run(debug=True)
```

#### 8. Run the API server

```
python app.py
```

<br>

### Deploy on Google Cloud Platform

#### 1. Create a project in GCP and enable billing for this project

#### 2. Enable the Compute Engine API and Cloud Build API. Open the GCP Console then on the left in the sidebar menu select > APIs & Services > Library

#### 3. Create a Cloud SQL Instance and select MySQL for the database

#### 4. Activate Cloud Shell then clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 5. Go to the cc-development branch and create app.yaml

```
runtime: python38
entrypoint: gunicorn -b :$PORT app:app
instance_class: F2
```

#### 6. Specify the region for the App Engine in the Cloud Shell

```
gcloud app create --region=<region>
```

#### 7. Deploy the API

```
gcloud app deploy
```

<br>

### Deploy on Heroku

#### 1. Create an account on Heroku

#### 2. Install the Heroku CLI

#### 3. Clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 4. Go to the cc-development branch

#### 5. Login to the Heroku CLI

```
$ heroku login -i
```

#### 6. Create Heroku apps from the CLI

```
$ heroku create <name of apps>
```

#### 7. Create a Procfile file

```
web: gunicorn app:app
```

#### 8. Initialize a Git repository in a new or existing directory

```
$ git init
$ heroku git:remote -a <name of apps>
```

#### 9. Commit the code to the repository and deploy it to Heroku using Git

```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```

<br>

## Routes & Request Methods for API V1

For this V1, there are two main APIs, which are ILT API, and ILT Feedback API. In this documentation below will be shown the database structure and the expected return for each API, followed by the route addresses and the input and output for each of the route.

<br>

### ILT API (Admin)

Below is the database structure and the expected return JSON on this ILT session for each of the return data.

| Key           | Data Type | Optional | Explanation                                                                                                                                                                                                       | Example                        |
| :------------ | :-------: | :------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| id **(PK)**   |  Integer  |    No    | Incremental ID for easier identification process.                                                                                                                                                                 | 1                              |
| title         |  String   |    No    | The **title** of this ILT, usually for the **publication purpose**.                                                                                                                                               | "ILT CC 1 - Front-end Website" |
| learning_path |  String   |    No    | **Determine** which **learning path** is this ILT on.                                                                                                                                                             | "Cloud Computing"              |
| session_name  |  String   |    No    | The **unique** "ID" of the ILT session. The **second** phrase determines the **learning path**, the **third** phrase is the **serial number**, while the **last** is the **session** **alphabet** **identifier**. | "ILT-CC-01-A"                  |
| mentor        |  String   |    No    | The **main mentor** in this ILT session.                                                                                                                                                                          | "Ivan Budianto"                |
| date          |   Date    |    No    | The **date** of this ILT session. Follows conventional date format (**YYYY-MM-DD**)                                                                                                                               | 2022-05-20                     |
| start_time    |   Time    |    No    | The starting **time** of this ILT session. Uses **ONLY** the hour and the minute. (**HH:MM**)                                                                                                                     | 12.00                          |
| end_time      |   Time    |    No    | The ending **time** of this ILT session. Uses **ONLY** the hour and the minute. (**HH:MM**)                                                                                                                       | 14.15                          |

<br>

#### 1. Route: api/v1/iltsession

- **GET** - Return all of ILT session in database

  Input: NONE

  Output: 200 - JSON of ILT sessions with keys shown above.

<br>

- **POST** - Create new record of ILT session in database

  Input: JSON with keys shown above.

  Output: 201 - JSON of the the created instance with keys shown above.

<br>

#### 2. Route: api/v1/iltsession/{string:session_name}

- **GET** - Return the data of a specific ILT session in database using its session_name

  Input: NONE

  Output: 200 - JSON of ILT with the same session_name as the parameter.

<br>

- **PATCH** - Update the record of a specific ILT session in database using its session_name

  Input: JSON with keys shown above.

  Output: 201 - JSON of the the updated instance with keys shown above.

<br>

- **DELETE** - Delete the record of a specific ILT session in database using its session_name

  Input: NONE

  Output: 204

<br>

#### 3. Route: api/v1/iltsession/learningpath/{string:session_path}

- **GET** - Return the ILT sessions of only the specified learning path in database

  Input: NONE

  Output: 200 - JSON of ILT sessions of a specific learning path with keys shown above.

<br>

### ILT Feedback (Admin & User)

Below is the database structure and the expected return JSON on this ILT feedback for each of the return data.

| Key           | Data Type | Optional | Explanation                                                                                                            | Example           |
| :------------ | :-------: | :------: | ---------------------------------------------------------------------------------------------------------------------- | ----------------- |
| id (PK)       |  Integer  |    No    | Incremental ID for easier identification process.                                                                      | 1                 |
| name          |  String   |    No    | The **name** of the **creator** of this ILT feedback, usually for the **identification purpose**.                      | "Ivan Budianto"   |
| email         |  String   |    No    | The **email** of the **creator** of this ILT feedback.                                                                 | "ivan@test.com"   |
| learning_path |  String   |    No    | The **learning path** of the **creator** of this ILT feedback.                                                         | "Cloud Computing" |
| session_name  |  String   |    No    | The **ILT session name** of this ILT feedback.                                                                         | "ILT-CC-01-A"     |
| rating        |  Integer  |    No    | The **quantitative rating** of this ILT session feedback. **Range from 1 to 5**.                                       | 5                 |
| feedback      |  String   |    No    | The **reason** of the rating. **Must be in word/sentence/paragraph**.                                                  | "ILT ini keren."  |
| relevant      |  Integer  |    No    | The **relevancy** of the given **feedback** with the **ILT**. **1** for **irrelevant**, and **2** for **relevant**.    | 2                 |
| sentiment     |  Integer  |   Yes    | The **sentiment** of the given **feedback**. **1** for **negative**, **2** for **positive**, and **3** for **advice**. | 2                 |
| validity      |  Integer  |    No    | The **validity** of the given **feedback** with the **ILT**. **1** for **invalid**, and **2** for **valid**.           | 2                 |

<br>

#### 4. Route: api/v1/iltsession/feedback

- **GET** - Return all of ILT feedback in database

  Input: NONE

  Output: 200 - JSON of ILT feedback with keys shown above.

<br>

- **POST** - Create new record of ILT feedback in database

  Input: **JSON with ONLY key of: name, email, learning_path, session_name, rating, and feedback**.

  Output: 201 - JSON of the the created instance with keys shown above.

<br>

#### 5. Route: api/v1/iltsession/feedback/{string:id}

- **GET** - Return the data of a specific ILT feedback in database using its id

  Input: NONE

  Output: 200 - JSON of ILT with the same session_name as the parameter.

<br>

- **DELETE** - Delete the record of a specific ILT feedback in database using its id

  Input: NONE

  Output: 204

<br>

#### 6. Route: api/v1/iltsession/feedback/bestfeedback

- **GET** - Return the best 3 ILT feedback to be displayed in the homepage

  Input: NONE

  Output: 200 - JSON of 3 best ILT feedback with keys shown above.

<br>

#### 7. Route: api/v1/iltsession/feedback/csv

- **GET** - Return a **CSV file** consisting of **all** ILT feedback in database with semicolon ";" delimiter

  Input: NONE

  Output: 200 - CSV file consisting of **all** ILT feedback in database

<br>

#### 8. Route: api/v1/iltsession/feedback/csv/{int:start_id}-{int:end_id}

- **GET** - Return a **CSV file** consisting of **ranged** ILT feedback in database, bounded between the start_id and end_id.

  Input: NONE

  Output: 200 - CSV file consisting of **ranged** ILT feedback in database,

  bounded between the start_id and end_id.
