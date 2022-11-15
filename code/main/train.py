import pickle
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from util import convert_comma_csv_to_tab_format, clean_dataset, tokenize, split_train_test, encode_sequences, define_model
# Preproces Dataset Test Code
raw_dataset_file = convert_comma_csv_to_tab_format("../resource/raw_dataset/en-fr_sample/file_test.csv", "../resource/raw_dataset/en-fr_sample/file_test_raw.csv")
dataset_file = clean_dataset(raw_dataset_file, "../resource/clean_dataset/en-fr_sample/file_test.pkl")
# load full dataset
dataset = pickle.load(open("../resource/clean_dataset/en-fr_sample/file_test.pkl", 'rb'))
# prepare tokenizer
eng_tokenizer = tokenize(dataset[:,0])
fr_tokenizer = tokenize(dataset[:,1])
# prepare vocab size and max length of the sentence
# English
eng_vocab_size = len(eng_tokenizer.word_index) + 1
eng_max_length = max([len(sentence) for sentence in dataset[:,0]])
print("==> " + "English Vocabulary Size: " + str(eng_vocab_size))
print("==> " + "English Maximum Length: " + str(eng_max_length))
#French
fr_vocab_size = len(fr_tokenizer.word_index) + 1
fr_max_length = max([len(sentence) for sentence in dataset[:,1]])
print("==> " + "French Vocabulary Size: " + str(fr_vocab_size))
print("==> " + "French Maximum Length: " + str(fr_max_length))
# Split dataset to train and test
train_file, test_file = split_train_test(dataset_file, "../resource/clean_dataset/train/en-fr_sample/file_test_train.pkl", "../resource/clean_dataset/test/en-fr_sample/file_test_test.pkl")
# load train and test file
train = pickle.load(open(train_file, 'rb'))
test = pickle.load(open(test_file, 'rb'))
# encode sequence for trainX, trainY and testX, testY
trainX = encode_sequences(fr_tokenizer, fr_max_length, train[:,1])
trainY = encode_sequences(eng_tokenizer, eng_max_length, train[:,0])
testX = encode_sequences(fr_tokenizer, fr_max_length, test[:,1])
testY = encode_sequences(eng_tokenizer, eng_max_length, test[:,0])
# compile model
learning_rate = 0.003
n_units = 256
metrics = "accuracy"
loss = "sparse_categorical_crossentropy"
model = define_model(fr_vocab_size, eng_vocab_size, fr_max_length, eng_max_length, n_units)
model.compile(loss=loss, optimizer=Adam(learning_rate), metrics=[metrics])
# summarize define model
print(model.summary())

# fit model
model_file = '../resource/model/model_v1.h5'
epoch = 15
batch_size = 64
checkpoint = ModelCheckpoint(model_file, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
model.fit(trainX, trainY, epochs=epoch, batch_size=batch_size, validation_data=(testX, testY), callbacks=[checkpoint])