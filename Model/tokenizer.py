import os
import re
import nltk
from Model.log import Logger
from typing import Dict, List
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class Tokenizer:
    logger = Logger(special_prefix="Tokenizer")
    SKIP_KEYS = {
        "position", "rotation", "scale", "anchor_left", "anchor_right",
        "anchor_top", "anchor_bottom", "margin_left", "margin_top",
        "visible", "__meta__", "resource_local_to_scene", "load_steps",
        "margin",
    }

    
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def process_files(self, file_map: Dict[str, str]) -> Dict[str, List[str]]:
        result = {}
        for name, path in file_map.items():
            if not os.path.isfile(path):
                self.logger.info(f"File not found: {path}")
                continue
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                tokens = self._tokenize_code(content, (path.split('.')[-1] if '.' in path else ""))
                normalized = self._normalize_tokens(tokens)
                result[name] = normalized
        self.logger.info(f"Processed {len(result)} files.")
        return result

    def _tokenize_code(self, text: str, filetype: str = "") -> List[str]:
        if filetype in ["tscn", "tres", "res"]:
            return self._tokenize_tscn_or_tres(text)
        else:
            return self._tokenize_script_code(text)


    def _tokenize_script_code(self, text: str) -> List[str]:
        self.logger.debug("Tokenizing code...")
        text = re.sub(r'//.*?$|/\*.*?\*/|#.*?$|"""(.*?)"""', '', text, flags=re.MULTILINE | re.DOTALL)
        tokens = re.findall(r'\b\w+\b', text)
        

        split_tokens = []
        for token in tokens:
            split_tokens.extend(self._split_identifier(token))
        return split_tokens

    def _split_identifier(self, identifier: str) -> List[str]:
        parts = re.sub(r'([a-z])([A-Z])', r'\1 \2', identifier)
        parts = parts.replace('_', ' ')
        return parts.lower().split()

    def _normalize_tokens(self, tokens: List[str]) -> List[str]:
        normalized = []
        skiped_tokens = []
        for t in tokens:
            t = t.lower()
            if not self._is_valid_token(t):
                skiped_tokens.append(t)
                continue
            if t in self.stop_words:
                skiped_tokens.append(t)
                continue
            t = self.stemmer.stem(t)
            normalized.append(t)
        return normalized

    def _is_valid_token(self, token: str) -> bool:
        rules = [
            lambda t: len(t) > 50,
            lambda t: len(t) <= 1,
            lambda t: t.isdigit(),
            lambda t: re.match(r'[a-z0-9]{5,}abq[a-z0-9]{10,}', t),
            lambda t: re.match(r'[a-zA-Z0-9]{15,}', t),
            lambda t: re.match(r'^(0x)?[a-f0-9]{6,}$', t),
            lambda t: re.search(r'(.)\1{3,}', t),
        ]
        return not any(rule(token) for rule in rules)
    
    def _tokenize_tscn_or_tres(self, text: str) -> List[str]:
        tokens = []
        for line in text.splitlines():
            line = line.strip()

            if not line or line.startswith(";") or line.startswith("#"):
                continue

            if line.startswith("[node") or line.startswith("[sub_resource") or line.startswith("[resource"):
                tokens.extend(re.findall(r'\b\w+\b', line))
                continue

            if "=" in line:
                key, value = map(str.strip, line.split("=", 1))
                if key.lower() in Tokenizer.SKIP_KEYS:
                    continue
                tokens.extend(re.findall(r'\b\w+\b', key))
                tokens.extend(re.findall(r'\b\w+\b', value))

        return tokens


