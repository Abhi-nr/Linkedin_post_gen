# LinkedIn Post Generator Using YouTube API & NLP

This project automatically generates engaging LinkedIn posts based on trending YouTube videos or specific video inputs. It utilizes the YouTube Data API to fetch video metadata and a trained Multi-Layer Perceptron (MLP) model to generate insightful and context-aware post captions.

---

## Features

- Fetches trending or user-specified YouTube videos using YouTube Data API
- Uses a trained MLP model to generate LinkedIn-style post captions
- Emulates a professional tone suitable for LinkedIn audience
- Can be extended to multiple platforms or analytics pipelines

---

## Tech Stack

- Python
- YouTube Data API v3
- Scikit-learn / TensorFlow (for NLP)
- Pandas / NumPy
- NLTK / TextBlob (optional for preprocessing)

---

## NLP Model Training Overview

The NLP model was trained on a custom dataset of LinkedIn posts and corresponding YouTube video features, including:

- Video title
- Description
- View count, like count, comment count
- Tags and category

Input features were preprocessed and vectorized before training the NLP for post-style text generation.


