import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure required NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class TextPreprocessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        # Adding domain-specific noise to ignore
        self.stop_words.update(['http', 'https', 'www', 'com'])

    def clean_text(self, text: str) -> list[str]:
        """
        Transforms raw text into a list of cleaned, stemmed tokens.
        """
        if not text:
            return []

        # 1. Lowercase and remove non-alphanumeric characters
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)

        # 2. Tokenize by whitespace
        tokens = text.split()

        # 3. Filter stopwords and apply Stemming
        cleaned_tokens = [
            self.stemmer.stem(token) 
            for token in tokens 
            if token not in self.stop_words and len(token) > 1
        ]

        return cleaned_tokens

# Singleton instance for easy import in main.py and tests
_preprocessor = TextPreprocessor()
clean_text = _preprocessor.clean_text