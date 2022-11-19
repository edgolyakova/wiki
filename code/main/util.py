# import libraries
from pickletools import optimize
import string
import csv
import re
import pickle
import math
from unicodedata import normalize
from numpy import array, argmax
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import LSTM, Dense, Input, TimeDistributed, Activation, RepeatVector, Embedding, Dropout
from nltk.translate.bleu_score import corpus_bleu

# Preprocess dataset
def convert_comma_csv_to_tab_format(InputFile, OutputFile):
  InputFile = InputFile
  OutputFile = OutputFile

  print("* "*5 + "Converting CSV to tab-delimited file" + " *"*5)

  with open(InputFile) as inputfile:
    with open(OutputFile, 'w', newline='') as outputfile:
      reader = csv.DictReader(inputfile, delimiter=',')
      writer = csv.DictWriter(outputfile, reader.fieldnames, delimiter='\t')
      writer.writeheader()
      writer.writerows(reader)
  print("* "*5 + "Conversion Complete" + " *"*5)
  return OutputFile

def clean_dataset(InputFile, OutputFile):
  OutputFile = OutputFile
  # Read File
  file = open(InputFile, mode='rt', encoding='utf-8')
  text = file.read()
  file.close()
  # Split text to sentences
  lines = text.strip().split('\n')
  pairs = [line.split('\t') for line in lines]
  # Clean pairs
  cleaned = list()
  # prepare regex for char filtering
  re_print = re.compile('[^%s]' % re.escape(string.printable))
  # prepare translation table for removing punctuation
  table = str.maketrans('', '', string.punctuation)
  for pair in pairs:
    clean_pair = list()
    for line in pair:
      # normalize unicode characters
      line = normalize('NFD', line).encode('ascii', 'ignore')
      line = line.decode('UTF-8')
      # tokenize on white space
      line = line.split()
      # convert to lowercase
      line = [ word.lower() for word in line]
      # remove punctuation from each token
      line = [word.translate(table) for word in line]
      # remove non-printable chars from each token
      line = [re_print.sub('', w) for w in line]
      # remove tokens with numbers in them
      line = [word for word in line if word.isalpha()]
      # store as string
      clean_pair.append(' '.join(line))
    cleaned.append(clean_pair)
  pickle.dump(array(cleaned), open(OutputFile, 'wb'))
  print("* "*5 + "Saved Clean Dataset" + " *"*5)
  return OutputFile

# Split dataset to train and test
def split_train_test(InputFile, TrainFile, TestFile):
  # load dataset
  dataset = pickle.load(open(InputFile, 'rb'))
  # Calculate length of dataset
  n = len(dataset)
  # Calculate the partition index for 20% for test and 80% for training
  ind = math.floor(n * 0.8)
  train, test = dataset[:ind], dataset[ind:]
  # save to file
  pickle.dump(train, open(TrainFile, 'wb'))
  pickle.dump(test, open(TestFile, 'wb'))
  return TrainFile, TestFile

def tokenize(lines):
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(lines)
  return tokenizer

def encode_sequences(tokenizer, length, lines):
  sequence = tokenizer.texts_to_sequences(lines)
  sequence = pad_sequences(sequence, maxlen=length, padding='post')
  return sequence

def define_model(fr_vocab, eng_vocab, fr_timesteps, eng_timesteps, n_units):
  model = Sequential()
  model.add(Embedding(fr_vocab, n_units, input_length=fr_timesteps))
  model.add(LSTM(n_units))
  model.add(RepeatVector(eng_timesteps))
  model.add(LSTM(n_units, return_sequences=True))
  model.add(TimeDistributed(Dense(eng_vocab, activation='softmax')))
  return model

def evaluate_model(model, tokenizer, sources, raw_dataset):
    actual, predicted = list(), list()
    for i, source in enumerate(sources):
        # translate encoded source text
        source = source.reshape((1, source.shape[0]))
        translation = predict_sequence(model, tokenizer, source)
        raw_target, raw_src = raw_dataset[i]
        print("raw_target:", raw_target)
        print("translation:",translation)
        if i < 10:
            print('src=[%s], target=[%s], predicted=[%s]' % (raw_src, raw_target, translation))
        actual.append([raw_target.split()])
        predicted.append(translation.split())
    # calculate BLEU score
    print('BLEU-1-gram: %f' % corpus_bleu(actual, predicted, weights=(1.0, 0, 0,0)))
    print('BLEU-2-gram: %f' % corpus_bleu(actual, predicted, weights=(0.5,0.5,0,0)))
    print('BLEU-3-gram: %f' % corpus_bleu(actual, predicted, weights=(0.3,0.3,0.3,0)))

# map an integer to a word
def map_int_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

# Predict Sentence
def predict_sequence(model, tokenizer, source):
    prediction = model.predict(source, verbose=0)[0]
    integers = [argmax(vector) for vector in prediction]
    target = list()
    for i in integers:
        word = map_int_to_word(i, tokenizer)
        if word is None:
            break
        target.append(word)
    return ' '.join(target)