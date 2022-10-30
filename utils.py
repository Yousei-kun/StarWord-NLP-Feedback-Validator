import tensorflow as tf
import pickle
import re
import csv
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

def load_model(model_path):
  loaded_model = tf.keras.models.load_model(model_path)
  return loaded_model

def load_tokenizer(tokenizer_path):
  with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)
    return tokenizer

def return_sentiment_label(prediction):
  result = np.argmax(prediction)
  if result == 0:
    result_class = "Negative"
  elif result == 1:
    result_class = "Positive"
  elif result == 2:
    result_class = "Advice"
  else:
    result_class = "Error"
  return result_class

def clean_data(input_text):
  processed_text = input_text.lower().strip()
  processed_text = re.sub(r"[^A-Za-z\d -]+", r" ", processed_text).strip()
  processed_text = re.sub(r"((?<=^)|(?<= )).((?=$)|(?= ))", r"", processed_text).strip()
  return processed_text

def remove_stopwords(input_text):
  with open('packages/stopword_bahasa/stopword_bahasa.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    stopwords = []
    for row in csv_reader:
      stopwords.append(row[0])

  processed_text = [word.lower() for word in input_text.split() if word.lower() not in stopwords]
  processed_text = ' '.join(processed_text)
  return processed_text

def check_positive_or_not(input_text):
  positive_review_indicator = ['sudah baik', 'belum ada', 'belom ada', 'tidak', 'tidak ada', 'sudah cukup', 'sdh ckp', 'sdh baik', 'tdk ada', 'blm ada', 'gada', 'gda', 'baik', 'cukup', 'ckp', 'bagus', 'sudah bagus', 'sdh bgs', 'sdh bagus', 'ckp bagus', 'cukup bagus', 'ckp bgs', 'ga ada', 'tak ada', 'tak ade', '-', ' ', '']

  if input_text in positive_review_indicator:
    return True
  return False

def tokenize_relevant(input_text):
  input_text = [input_text]
  tokenizer = load_tokenizer('packages/model/tokenizer_relevant/tokenizer_relevant.pickle')
  text_sequence = tokenizer.texts_to_sequences(input_text)
  padded_sequence = pad_sequences(text_sequence, maxlen=100, padding='post', truncating='post')
  return padded_sequence

def tokenize_sentiment(input_text):
  input_text = [input_text]
  tokenizer = load_tokenizer('packages/model/tokenizer_sentiment/tokenizer_sentiment.pickle')
  text_sequence = tokenizer.texts_to_sequences(input_text)
  padded_sequence = pad_sequences(text_sequence, maxlen=100, padding='post', truncating='post')
  return padded_sequence

def predict_relevant(input_text):
  checked = check_positive_or_not(input_text)
  if checked:
    return 1

  input_text = clean_data(input_text)
  processed_text = remove_stopwords(input_text)

  checked = check_positive_or_not(processed_text)
  if checked:
    return 1

  padded_sequence = tokenize_relevant(processed_text)

  model_relevant = load_model('packages/model/model_relevant/model_relevant.h5')
  result = model_relevant.predict(padded_sequence)
  result_class = 1 if result > 0.5 else 0
  return result_class

def predict_sentiment(input_text, relevant):
  if relevant == 0:
    return None

  checked = check_positive_or_not(input_text)
  if checked:
    return 1

  input_text = clean_data(input_text)
  processed_text = remove_stopwords(input_text)

  checked = check_positive_or_not(processed_text)
  if checked:
    return 1

  padded_sequence = tokenize_sentiment(processed_text)

  model_sentiment = load_model('packages/model/model_sentiment/model_sentiment.h5')
  result = model_sentiment.predict(padded_sequence)
  result_class = np.argmax(result)
  return result_class

def feedback_validity(star, relevant, sentiment):
  if relevant == 0:
    return 0

  if (star == 1 or star == 2 or star == 3) and (sentiment == 0 or sentiment == 2):
    return 1
  elif (star == 4 or star == 5) and (sentiment == 1 or sentiment == 2):
    return 1
  else:
    return 0

# Use this code commented below to test the script!
# if __name__ == "__main__":
#     print(predict_relevant("Your string here"))
#     print(predict_sentiment("Your string here", 1))
