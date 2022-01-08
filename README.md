# YammerHustNetwork

## Install dependencies
```
pip install selenium
pip install underthesea
pip install tensorflow
pip install gensim
```

## How to crawl data

### Crawl with Selenium
You need to download [chromedriver](https://chromedriver.chromium.org/downloads) and a microsoft account of HUST network 

```
python yammer_crawler.py \ 
    --username your_username \
    --password your_password \
    --driver_path /path/to/driver/chromedriver.exe
```

### Crawl with Rest API
```
python yammerAPI.py \
    --username your_username \
    --password your_password \
    --driver_path /path/to/driver/chromedriver.exe
```


## Train the model
### Train the model with count-vector or tf-idf features
```
python train_tf_idf.py \
    --extractor tf-idf \  # choices: ["count-vector", "tf-idf"]
    --model nn  # choices: ["logistic-regression", "naive-bayes", "svm", "decision-tree", "nn"]
```

### Train the model with word2vec features
```
python train_w2v.py \
    --model nn  # choices: ["logistic-regression", "naive-bayes", "svm", "decision-tree", "nn"]
```

## Colab demo
[[Colab]](https://colab.research.google.com/drive/1SALaUX-XbNKiLHzsdtY5tRvOBHZrcpZD#scrollTo=qcFJRcxCcapl)