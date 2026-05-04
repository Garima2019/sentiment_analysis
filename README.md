# 🔬 SentiScope — Sentiment Analysis App

> Real-time NLP sentiment classification powered by **TF-IDF + Logistic Regression**, served through an interactive Streamlit interface.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

---

## 📌 Overview

SentiScope is a lightweight, production-ready sentiment analysis application that classifies free-form text — movie reviews, product feedback, social media posts — as **positive** or **negative** in real time, along with a confidence score.

The model is trained on the **IMDB Movie Reviews Dataset** (50,000 samples) and achieves approximately **~89% accuracy** on held-out test data using a classical NLP pipeline.

---

## ✨ Features

- **Real-time prediction** — classify text instantly with a confidence score
- **Preprocessing pipeline** — automatic lower-casing and noise stripping
- **Confidence bar** — visual probability indicator for each prediction
- **Technical details** — inspect vector shape and processed text in the UI
- **Documentation page** — full architecture and setup guide built into the app
- **About Me page** — developer profile and project stats

---

## 🏗️ Architecture

```
Raw Text
   │
   ▼
clean_text()          # lowercase + strip non-alpha characters
   │
   ▼
TfidfVectorizer       # 5,000-feature sparse matrix
   │
   ▼
LogisticRegression    # binary classifier (positive / negative)
   │
   ▼
predict_proba()       # class label + confidence score
```

---

## 📁 File Structure

```
sentiment-analyzer/
├── app.py               # Streamlit front-end (UI + pages)
├── main.py              # Training script + clean_text() helper
├── model.pkl            # Serialised Logistic Regression model
├── vectorizer.pkl       # Serialised TF-IDF vectorizer
├── IMDB Dataset.csv     # Raw dataset (download separately — see below)
└── requirements.txt     # Python dependencies
```

---

## 🚀 Getting Started

### 1 — Clone the repository

```bash
git clone https://github.com/garima2019/sentiment-analyzer.git
cd sentiment-analyzer
```

### 2 — Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
streamlit>=1.30.0
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
```

### 3 — Download the dataset

Download **IMDB Dataset.csv** from Kaggle and place it in the project root:

🔗 [Sentiment Analysis of IMDB Movie Reviews — Kaggle](https://www.kaggle.com/code/lakshmi25npathi/sentiment-analysis-of-imdb-movie-reviews)

### 4 — Train the model

```bash
python main.py
```

This generates `model.pkl` and `vectorizer.pkl` in the project root.

### 5 — Launch the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🤖 Model Details

| Property | Value |
|---|---|
| Algorithm | Logistic Regression (L2 regularisation) |
| Vectorizer | TF-IDF (`max_features=5000`) |
| Train / Test split | 80% / 20% (`random_state=42`) |
| Dataset | IMDB Movie Reviews (50,000 samples) |
| Test Accuracy | ~89% |
| Output classes | `positive`, `negative` |

### Preprocessing (`clean_text`)

```python
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    return text
```

Steps:
1. **Lowercase** — normalise casing
2. **Strip non-alpha** — remove punctuation, digits, and special characters

---

## 📊 Performance

```
              precision    recall    f1-score
  negative       0.89       0.88       0.89
  positive       0.88       0.90       0.89
  accuracy                            0.89
```

> Results evaluated on 10,000 held-out IMDB reviews.

---

## 🛣️ Roadmap

- [ ] Replace Logistic Regression with fine-tuned DistilBERT
- [ ] Add neutral / mixed sentiment class
- [ ] Expose REST endpoint via FastAPI
- [ ] Add SHAP token-level explainability
- [ ] Deploy to Streamlit Community Cloud / HuggingFace Spaces
- [ ] Support batch CSV upload for bulk inference

---

## 👩‍💻 Author

**Garima Agrawal** — ML Engineer & NLP Researcher

I build intelligent, data-driven tools that make machine learning **accessible, explainable, and production-ready**.

| | |
|---|---|
| 🔗 GitHub | [github.com/garima2019](https://github.com/garima2019) |
| 💼 LinkedIn | [linkedin.com/in/garima-agrawal-291a78185](https://www.linkedin.com/in/garima-agrawal-291a78185/) |
| 🌐 Portfolio | [garimaagw01.wixsite.com/garima_portfolio](https://garimaagw01.wixsite.com/garima_portfolio) |
| ✉ Email | garima.agw01@gmail.com |

---

## 📄 License

This project was developed for academic purposes to predicts sentiment of text (positive/negative).

---

## 🙏 Acknowledgements

- [IMDB Dataset — Kaggle](https://www.kaggle.com/code/lakshmi25npathi/sentiment-analysis-of-imdb-movie-reviews) for the training data
- [scikit-learn](https://scikit-learn.org/) for the ML toolkit
- [Streamlit](https://streamlit.io/) for the rapid application framework
