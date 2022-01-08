import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dropout, Dense, Activation, Flatten, Conv2D, MaxPooling2D, Bidirectional, LSTM
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, LearningRateScheduler, EarlyStopping
from keras.models import Model, load_model
import argparse

parser = argparse.ArgumentParser(description='Train model')
parser.add_argument('--extractor', default="tf-idf", choices=["count-vector", "tf-idf"])
parser.add_argument('--model', default="nn", choices=["logistic-regression", "naive-bayes", "svm", "decision-tree", "nn"])

args = parser.parse_args()


data_train = pd.read_csv('data/train.csv')
data_val = pd.read_csv('data/valid.csv')

X_train = data_train['NoiDung'].values
y_train = data_train['Nhom'].values
X_val = data_val['NoiDung'].values
y_val = data_val['Nhom'].values

label_encoder = LabelEncoder()
label_encoder.fit(y_train)
y_train = label_encoder.transform(y_train)
y_val = label_encoder.transform(y_val)

X_train.shape, X_val.shape, y_train.shape, y_val.shape

count_vect = CountVectorizer(ngram_range=(1,1), max_df=0.8, max_features=None)
tfidf_transformer = TfidfTransformer()
X_train_counts = count_vect.fit_transform(X_train)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_val_counts = count_vect.transform(X_val)
X_val_tfidf = tfidf_transformer.transform(X_val_counts)

if args.extractor == "count-vector":
    X_train = X_train_counts
    X_val = X_val_counts
elif args.extractor == "tf-idf":
    X_train = X_train_tfidf
    X_val = X_val_tfidf

if args.model == "nn":
    X_train = X_train.toarray()
    X_val = X_val.toarray()
    model = Sequential()
    model.add(Dense(1024, activation='relu', input_shape=(5404, )))
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
print(f"Model summary: extractor: {args.extractor}, model: {args.model}" )
print(classification_report(y_val, y_pred, target_names=list(label_encoder.classes_)))
