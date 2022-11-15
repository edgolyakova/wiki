import pickle
from util import encode_sequences, tokenize, evaluate_model
from keras.models import load_model
model_file = "../resource/model/model_v1.h5"
dataset_file = "../resource/clean_dataset/en-fr_sample/file_test.pkl"
test_file = "../resource/clean_dataset/train/en-fr_sample/file_test_train.pkl"
dataset = pickle.load(open(dataset_file, 'rb'))
test = pickle.load(open(test_file, 'rb'))
# prepare tokenizer
fr_tokenizer = tokenize(dataset[:,0])
fr_vocab_size = len(fr_tokenizer.word_index) + 1
fr_max_length = max([len(sentence) for sentence in dataset[:,1]])
# encode sequence
testX = encode_sequences(fr_tokenizer, fr_max_length, test[:, 0])
# load model
model = load_model(model_file)
# testing
print("*"*5 + "Evaluate Model" + "*"*5)
evaluate_model(model, fr_tokenizer, testX, dataset)