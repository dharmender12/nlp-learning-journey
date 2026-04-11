# NLP Learning Journey

A practical, notebook-first learning repository for Natural Language Processing (NLP), Machine Learning (ML), and selected Deep Learning (DL) topics.

This project contains hands-on notebooks, small apps, datasets, and assignment files that document an end-to-end learning path from text preprocessing to embeddings, transformers, and model deployment concepts.

## Table of Contents

1. [Project Goals](#project-goals)
2. [What Is Inside This Repository](#what-is-inside-this-repository)
3. [Repository Structure](#repository-structure)
4. [Learning Modules and Notebooks](#learning-modules-and-notebooks)
5. [Datasets](#datasets)
6. [How to Run the Projects](#how-to-run-the-projects)
7. [Streamlit Apps](#streamlit-apps)
8. [Recommended Learning Order](#recommended-learning-order)
9. [Notes and Scope](#notes-and-scope)

## Project Goals

- Build strong fundamentals in NLP preprocessing and feature engineering.
- Practice classic ML algorithms on text and tabular data.
- Explore DL architectures used in NLP tasks.
- Implement practical mini-projects for sentiment analysis, multi-label classification, and text generation.
- Keep all learning artifacts in one place for revision and portfolio use.

## What Is Inside This Repository

- Jupyter notebooks covering NLP concepts, ML models, and DL workflows.
- A BBC news text corpus for topic/category experiments.
- CSV datasets for regression/classification practice.
- Streamlit demo apps in Python scripts.
- Assignment and notes files related to the learning journey.

## Repository Structure

```text
.
├── README.md
├── app.py
├── calc.py
├── *.ipynb
├── *.csv
├── bbc-fulltext/
│   └── bbc/
│       ├── README.TXT
│       ├── business/
│       ├── entertainment/
│       ├── politics/
│       ├── sport/
│       └── tech/
└── documents and notes (PDF/TXT/PNG)
```

## Learning Modules and Notebooks

### 1. NLP Basics and Text Preprocessing

- Bag_of_words.ipynb
- tf_idf.ipynb
- stop_word_removal.ipynb
- text_file.ipynb
- nltk_vs_spacy.ipynb
- Spacy.ipynb
- Vector_similarity_spacy.ipynb

### 2. Embeddings and Semantic Representations

- word_embedding.ipynb
- Sentence_embedding.ipynb
- sentiment_analysis_using_wordVec.ipynb
- Emotion_recognition_with_glove.ipynb

### 3. Sentiment Analysis and Hate Speech

- sentiment_analysis.ipynb
- Sentiment_analysis_DL.ipynb
- sentiment_Deep_learning.ipynb
- data_preparation_sentiment_using_DL.ipynb
- train_test_split_for_sent_ana_DL.ipynb
- intro_hate_speech.ipynb
- implementation_of_hate_speech.ipynb

### 4. Machine Learning Fundamentals

- Linear_regression.ipynb
- Logistic_regression.ipynb
- knn.ipynb
- svm.ipynb
- Decision_tree_vs_Random_forest.ipynb
- ml_vs_dl.ipynb

### 5. Deep Learning and Neural Architectures

- RNN_and_its_types.ipynb
- Types_of_Neural_network.ipynb
- CNN.ipynb
- intro_to_transformer.ipynb
- Multi_modal_nlp.ipynb

### 6. Applied NLP and Advanced Topics

- Multi_label_binarization.ipynb
- Multi_label_classification.ipynb
- CV_Parsing_nlp.ipynb
- Poetry_generation.ipynb
- Generative_AI.ipynb
- prompt_engineering.ipynb
- Model_deployment.ipynb
- project.ipynb

## Datasets

### BBC Full Text Dataset

Path: bbc-fulltext/bbc

- Categories: business, entertainment, politics, sport, tech
- Use case: topic classification, clustering, NLP feature engineering experiments
- Citation and license notes are available in bbc-fulltext/bbc/README.TXT

### CSV Files

- salary_data.csv
- Social_Network_Ads.csv

These are used in supporting ML practice notebooks.

## How to Run the Projects

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install core dependencies

```bash
pip install jupyter pandas numpy scikit-learn matplotlib seaborn nltk spacy textblob streamlit beautifulsoup4 requests emoji
```

Optional setup for NLTK/TextBlob data:

```bash
python -m textblob.download_corpora
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 3. Start Jupyter

```bash
jupyter notebook
```

Then open the notebook you want to run.

## Streamlit Apps

### Sentiment and URL Text Analysis App

File: app.py

Run:

```bash
streamlit run app.py
```

Features:

- Sentiment analysis for user input text.
- URL text scraping and sentence-wise sentiment breakdown.

### BMI Calculator App

File: calc.py

Run:

```bash
streamlit run calc.py
```

## Recommended Learning Order

1. Start with preprocessing notebooks (Bag of Words, TF-IDF, stop-word removal).
2. Move to classical ML notebooks (regression, KNN, SVM, trees/forests).
3. Continue with sentiment analysis pipelines.
4. Study embeddings and semantic similarity.
5. Explore DL architectures (RNN/CNN/Transformers).
6. Finish with advanced applications (multi-label NLP, generative and deployment topics).

## Notes and Scope

- This repository currently tracks NLP learning files and the BBC dataset folder.
- The skilee-ai folder is intentionally excluded from version tracking in this repo.
- Notebooks may require different package versions depending on the topic; if a notebook fails, install the missing library and rerun.
