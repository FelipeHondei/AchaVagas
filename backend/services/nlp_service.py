from __future__ import annotations

import logging
from functools import cached_property
from typing import Iterable

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.config import get_settings

log = logging.getLogger(__name__)
settings = get_settings()


class NLPService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)

    @cached_property
    def nlp(self):
        try:
            return spacy.load(settings.spacy_model)
        except OSError:
            log.warning("spaCy model %s not found. Loading blank 'pt' pipeline.", settings.spacy_model)
            return spacy.blank("pt")

    def extract_skills(self, text: str) -> list[str]:
        doc = self.nlp(text)
        return [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

    def similarity(self, profile_text: str, job_texts: Iterable[str]) -> list[float]:
        corpus = [profile_text, *job_texts]
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        return similarities.tolist()

