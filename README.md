<p align='center'>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />        
  </a>&nbsp;&nbsp;
  <a href="https://flask.palletsprojects.com/en/2.0.x/">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />        
  </a>&nbsp;&nbsp;
  <a href="https://www.tensorflow.org/">
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
  </a>&nbsp;&nbsp;
</p>
<br>
<p align='center'>
    <img src="readme_thumbnail/thumbnail.jpg/" alt="Dices showing Faces">
</p>

<a name="demolink"></a>

# StarWord Demo Link

[Click here to view StarWord](https://starword.site)

<br>

<a name="table"></a>

# Table of Contents

0. [Table of Contents](#table)
1. [StarWord Demo Link](#demolink)
2. [About StarWord](#about)
   1. [Background](#background)
   2. [Goal & Aim](#goal)
   3. [How to Download and Host](#downloadandhost)
      1. [Run StarWord Web on local](#local)
      2. [Deploy on Google Cloud Platform](#gcp)
      3. [Deploy on Heroku](#heroku)
   4. [How Does the Inference Work? #1 - Relevant or Irrelevant](#inference1)
   5. [How Does the Inference Work? #1 - Positive, Negative, Advice](#inference2)
   6. [Plans & Realization](#plans)
   7. [Repository & Branch](#repo)
   8. [Google Cloud Tools and Monthly Pricing](#pricing)
   9. [Bibliography](#bibliography)
   10. [Contributing Developers](#dev)

<br>
<a name="about"></a>

# About StarWord

**StarWord** is an Indonesian-language-based website with machine-learning powered website, made using TensorFlow and Flask.

StarWord helps Dicoding Indonesia by validating feedback from ILT (Instructor-Led Training). Each of the feedback fed into the system will be rendered valid or not based on 3 factors: its relevancy to ILT, its sentiment, and its quantitative rating.

This project is developed by 5 developers for the company-capstone project of **Bangkit Academy 2022 by Google, GoTo, Traveloka** of **MBKM 2022** from **Machine Learning (ML) and Cloud Computing (CC)** specialization path with the team ID **C22-FV01**.

<br>

<a name="background"></a>

## 1. Background

All modern user-based services, including Dicoding, use feedback from users to improve further as metrics. It is not rare that this approach has flaws, especially in the process of data acquisition. 15% of the users give mismatched quantitative (star-based) and qualitative (essay field) feedback, making it harder to get an overview of the potential improvements and new strategies for the company to improve as the assessment is clouded by the mismatched data.

Tackling this problem, an API is developed to help service providers to validate all of their user's feedback results, thus leading to the fully-accurate data-driven improvement. Specifically, this API will take an input of a JSON dictionary pair(s) of quantitative and qualitative feedback to be classified. This dictionary will be broken down into each pair of their respective ratings. If both the quantitative and the sentiment of the qualitative feedback have a “Positive” label, then this feedback will be considered valid and vice-versa. The output of this process will be a JSON dictionary for each of the input pairs, which can be consumed through an API link to be utilized for end-users through a website, or a mobile application.

<br>

<a name="goal"></a>

## 2. Goal & Aim

- This website aims to help Dicoding to validate the feedback collected in ILT sessions. StarWord will help Dicoding by fetching the label of whether the feedback is relevant to ILT and predicting its sentiment. This result will be compared to the star given by the user.
- StarWord has a feature to help the admin validate the feedbacks per batch, and has 2 views, which are for admin to manipulate the ILT sessions and feedback, and for users to input the feedback for ILT sessions.

<br>

<a name="downloadandhost"></a>

## 3. How to Download and Host

This section contains the steps to run StarWord Web on local device and environment, then how to deploy it to Google Cloud Platform or Heroku. Those three steps will be explained with several short codes below.

<br>

<a name="local"></a>

### A. Run StarWord Web on Local

#### 	1. Clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 	2. Go to the main branch and install virtualenv

```
pip install virtualenv
```

#### 	3. Create and name a virtual environment

```
python -m venv <name of environment>
```

#### 	4. Activate the environment

```
<name of environment>\Scripts\activate
```

#### 	5. Install all required packages for this Web

```
pip install -r requirements.txt
```

#### 	6. Add debug mode to keep reloading server (only for development)

```
if __name__ == "__main__":
  app.run(debug=True)
```

#### 	7. Run the Web server

```
python run.py
```

Now, your own StarWord website is ready to serve!



<br>

<a name="gcp"></a>

### B. Deploy on Google Cloud Platform

#### 	1. Create a project in GCP and enable billing for this project

#### 	2. Enable the Cloud Run Admin API. Open the GCP Console then on the left in the sidebar menu select > APIs &

#### 		Services > Library

#### 	3. Activate Cloud Shell then clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 	4. Go to the main branch and create Dockerfile below

```
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app
```

#### 	5. Open the Editor Console then on the bottom click Cloud Code

#### 	6. Deploy to Cloud Run

<br>

<a name="heroku"></a>

### C. Deploy on Heroku

#### 	1. Create an account on Heroku

#### 	2. Install the Heroku CLI

#### 	3. Clone this repository

```
https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator.git
```

#### 	4. Go to the main branch

#### 	5. Login to the Heroku CLI

```
$ heroku login -i
```

#### 	6. Create Heroku apps from the CLI

```
$ heroku create <name of apps>
```

#### 	7. Create a Procfile file

```
web: gunicorn run:app
```

#### 	8. Initialize a Git repository in a new or existing directory

```
$ git init
$ heroku git:remote -a <name of apps>
```

#### 	9. Commit the code to the repository and deploy it to Heroku using Git

```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```

<br>

<a name="inference1"></a>

## 4. How Does The Inference Work? #1 - Relevant Irrelevant

1. From the web page, grab user's input such as **name**, **email**, **leaning path**, **session name**, **rating**, and **feedback**. Before going to the next step, it is crucial to make sure that the **session name** input is a valid name. if **session name** is invalid, the relust will be `Nama sesi ILT tersebut tidak tersedia`.

2. Check whether the **feedback** is relevant or not by calling `predict_relevant` function which contains a `check_positive_or_not` function. The mentioned function will return true if the feedback is in "positive_review_indicator" list, false otherwise. If it is true, return it as a **positive feedback**. Elseways, call the `clean_data` function to remove unwanted characters after lowering it.

3. Clean the stop words from the **feedback** string by using the `remove_stopwords` function. This function will load the "**stopword_Bahasa.csv**" file which contains stop words in Indonesian and delete every stop word in the **feedback** string respectively. Perform manual checking once more by utilizing the `check_positive_or_not` function.

4. Tokenize the **feedback** by using the `tokenize_relevant` function. The function will load the "**tokenizer_relevant.pickle**" which contains the tokenizer object and make the **feedback** string into sequences by using the `texts_to_sequences` method. Finally, call the `pad_sequences` function from the `TensorFlow` library to make the pads sequences of the **feedback** the same length, then return the padded sequence.

5. Load the model from the 'model_relevant.h5' file which is in the folder "packages/model/model_sentiment/model_relevant.h5" using the `load_model` function with`TensorFlow` library.

6. Use the model loaded previously to predict the relevance of the **feedback** by using the `predict` method and set the padded sequence as parameters. The result is a float with the range 0 to 1. However, to predict sentiment later, the result of relevance prediction has to be either 0 (irrelevant) or 1 (relevant). Therefore, the returned result will be rounded to 0 or 1.

<br>

<a name="inference2"></a>

## 5. How Does The Inference Work? #2 - Positive, Negative, Advice

1. From the web page, grab user's input such as **name**, **email**, **leaning path**, **session name**, **rating**, and **feedback**. Before validation make sure the **session name** input is a valid name. if **session name** is invalid, the relust will be `Nama sesi ILT tersebut tidak tersedia`.

2. Check the sentiment by using the `predict_sentiment` function, where the parameter "relevant" will be checked whether its value is 0 or not, and returned as `None` if it is. Otherwise, the **feedback** will be further checked if it is in "positive_review_indicator" list by using the `check_positive_or_not` function. It will return 1 (which indicates the **feedback** is positive) if returned True. Elseways, call the `clean_data` function to remove unwanted characters and punctuation after lowering it.

3. Clean the stop words from the **feedback** string by using the `remove_stopwords` function. This function will load the "**stopword_Bahasa.csv**" file which contains stop words in Indonesian and delete every stop word in the **feedback** string respectively. Perform manual checking once more by utilizing the `check_positive_or_not` function.

4. Tokenize the **feedback** by using the `tokenize_relevant` function. The function will load the "**tokenizer_relevant.pickle**" which contains the tokenizer object and make the **feedback** string into sequences by using the `texts_to_sequences` method. Finally, call the `pad_sequences` function from the `TensorFlow` library to make the pads sequences of the **feedback** the same length, then return the padded sequence.

5. Load the model from the 'model_relevant.h5' file which is in the folder "packages/model/model_sentiment/model_sentiment.h5" using the `load_model` function with`TensorFlow` library.

6. Use the model loaded previously to predict the relevance of the **feedback** by using the `predict` method and set the padded sequence as parameters. The result returned is an array of the model's confidence of each label (array of 3 values of classes available for *positive*, *negative*, and *advice*). From the array, the index of maximum value is fetched using `argmax` method from `NumPy` library.

<br>

<a name="plans"></a>

## 6. Plans & Realization

The development plan of this project can be seen in the Gantt Chart in the picture provided or [for more information can click here to view](https://bit.ly/C22FV01-ProjectSchedule)
<img src="https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator/blob/ml-development/image/gann_chart.png" width="950" />

As the development has finished, these are the points conducted from the plan & realization:

- First week

  This week is for the project planning, as well as for the additional datasets since the real given datasets are insufficient and include processes in dataset cleaning, view templating, dataset labeling, and finalization. Meanwhile, the front-end is developed is constructed parallelly.

- Second week

  This week is focusing on model development including the model tuning for relevant labels and continuing to sentiment labels. Therefore, the second week is spent on the model development and its completion to get the best fit model.

- Third week

  This week is for deployment including API integration, hosting process and pipeline production for StarWord to be able to be used for the users. The deployment used Flask as the main framework and the hosting process involved Heroku as the host.

- Fourth week

  This week is for project testing and finalization. There was a mentoring session conducted within this week which resulted in wide range of improvements, including front-end, additional dataset, and re-training to develop better model.

- The rest of the weeks

  These weeks are used to make the project brief, documentation. Moreover, preparation for the presentation of the project is produced within these periods.

<br>

<a name="repo"></a>

## 7. Repository & Branch

The **StarWord Repository** is divided into **3 branches** (including master). Below is the explanation:

- **API Development Branch** (cc-development)

  The cc-development branch is the branch for back-end (dedicated for ONLY API) development. It is written in Python by using the flask and flask restful framework.

  See the full documentation and the routings configuration, as well as their input and output [here](https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator/tree/cc-development). 

- **Machine Learning Development Branch** (ml-development)

  The ML branch is the branch for machine learning development. It is written in Python, and it uses most basic libraries such as Pandas, NumPy, Sci-Kit Learn, and TensorFlow. Full documentation of the Machine Learning project with steps to make the model is clearly explained in the readme.md file of the Machine Learning development branch, along with the pipeline testing of each model.

  See the full documentation and the model development process from scratch [here](https://github.com/Yousei-kun/StarWord-NLP-FeedbackValidator/tree/ml-development).

- **Main Branch** (main)

  The Main branch is used as the integration branch of CC-development and ML-development. The plan is to use the Flask framework to build and integrate the website and machine learning model as a whole website. In the main branch lies the front-end website which only uses monolithic Flask to consume the API made from the cc-development branch. 

<br>

<a name="pricing"></a>

## 8. Google Cloud Tools and Monthly Pricing

Below are the tools used for deployment, and its detail of monthly pricing.

| Name              | Detail                                                       | Type                              | Monthly Pricing Est. |
| ----------------- | ------------------------------------------------------------ | --------------------------------- | -------------------- |
| Google Cloud SQL  | Database-related functions to create, read, update, delete data | db-standard-1. 10 GiB SSD storage | $42                  |
| Google App Engine | Hosting the website                                          | F2                                | $133                 |
| Google Cloud Run  | Handle the request-related  from users                       | 0.25 GiB Memory, per 10k requests | $5                   |



<br>

<a name="bibliography"></a>

## 9. Bibliography

### A. Framework, Library, and external repository/API used:

- [Flask](https://flask.palletsprojects.com/en/2.1.x/) & [Flask Restful](https://flask-restful.readthedocs.io/en/latest/)
- [TensorFlow](https://tensorflow.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Requests](https://requests.readthedocs.io/en/latest/)
- [Pandas](https://pandas.pydata.org/docs/)
- [NumPy](https://numpy.org/doc/stable/)
- [Scikit-Learn](https://scikit-learn.org/stable/)
- [Datetime](https://docs.python.org/3/library/datetime.html)
- [Bootstrap](https://getbootstrap.com/)

<br>

<a name="dev"></a>

## 10. Contributing developers

**Bangkit 2022 | Company-Capstone Product | C22-FV01 Team Members**:

- (ML) M7227F2096 - Ivan Budianto
- (ML) M2150F1654 - Jestine Siewij
- (ML) M7312H2694 - Agus Wahyudi
- (ML) M2299F2566 - Khamidah Ahmad Syauqi
- (CC) C2193F1826 - Mochamad Nahrul Hayawan
