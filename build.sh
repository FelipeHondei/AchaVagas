#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Baixar modelo do spaCy (use o modelo pequeno para economizar espaço)
python -m spacy download en_core_web_sm

# Se usar NLTK, baixe os dados necessários
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"