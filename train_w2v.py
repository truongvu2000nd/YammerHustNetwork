import pandas as pd
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from keras.models import Model, load_model
from gensim.models import Word2Vec
from keras import preprocessing
from keras.layers import Embedding
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import argparse


parser = argparse.ArgumentParser(description='Train model')
parser.add_argument('--model', default="nn", choices=["logistic-regression", "naive-bayes", "svm", "decision-tree", "nn"])

args = parser.parse_args()

data_train = pd.read_csv('data/train.csv')
data_val = pd.read_csv('data/valid.csv')

sentences = data_train['NoiDung'].values
sentences = [[word for word in line.split()] for line in sentences]

model = Word2Vec(min_count=1, vector_size=100, sg=1)
model.build_vocab(sentences)
print("-" * 60)
print("Train w2v....")
model.train(sentences, total_examples = model.corpus_count, epochs=5)

tokenizer = preprocessing.text.Tokenizer(split=' ', oov_token="NaN", filters='!"#$%&()*+,-./:;<=>?@[]^`{|}~ ')
lst_corpus = data_train['NoiDung'].values
tokenizer.fit_on_texts(lst_corpus)
dic_vocabulary = tokenizer.word_index

X_train = tokenizer.texts_to_sequences(lst_corpus)

## start the matrix (length of vocabulary x vector size) with all 0s
embeddings = np.zeros((len(dic_vocabulary)+1, 100))
for word, idx in dic_vocabulary.items():
    ## update the row with vector
    try:
        embeddings[idx] =  model.wv[word]
    ## if word not in model then skip and the row stays all 0s
    except:
        pass

X_train_ = []
for x_train in X_train:
    x_train = np.array(x_train)
    x_train = Embedding(input_dim=embeddings.shape[0], output_dim=embeddings.shape[1], weights=[embeddings],
                      input_length=len(x_train))(x_train)
    x_train = x_train.numpy()
    x_train = np.mean(x_train, axis=0)
    X_train_.append(x_train)

X_train = np.array(X_train_)

X_val = data_val['NoiDung'].values
X_val = tokenizer.texts_to_sequences(X_val)
X_val_ = []
for x_val in X_val:
    x_val = np.array(x_val)
    x_val = Embedding(input_dim=embeddings.shape[0], output_dim=embeddings.shape[1], weights=[embeddings],
                      input_length=len(x_val))(x_val)
    x_val = x_val.numpy()
    x_val = np.mean(x_val, axis=0)
    X_val_.append(x_val)
X_val = np.array(X_val_)

y_train = data_train['Nhom'].values
y_val = data_val['Nhom'].values
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(y_train)
y_train = label_encoder.transform(y_train)
y_val = label_encoder.transform(y_val)


if args.model == "nn":
    model = Sequential()
    model.add(Dense(1024, activation='relu', input_shape=(100, )))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(7, activation='softmax'))
    model.summary()

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    checkpoint = ModelCheckpoint(filepath='model/tf-idf/NN/model.h5',
                                monitor='val_accuracy',
                                verbose=1,
                                save_best_only=True)

    model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=256, epochs=10, verbose=1, callbacks=[checkpoint])
    y_pred = model.predict(X_val)
    y_pred = np.argmax(y_pred, axis=1)
    print(classification_report(y_val, y_pred, target_names=list(label_encoder.classes_)))

else:
    if args.model == "logistic-regression":
        model = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=10000)
    elif args.model == "naive-bayes":
        model = MultinomialNB()
    elif args.model == "svm":
        model = SVC(gamma='scale')
    elif args.model == "decision-tree":
        model = DecisionTreeClassifier()
    
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

print("-" * 60)
print(f"Model summary: extractor: word2vec, model: {args.model}" )
print(classification_report(y_val, y_pred, target_names=list(label_encoder.classes_)))
