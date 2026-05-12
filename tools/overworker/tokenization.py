"""Tokenization engine - converts repo content into tokens."""
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class Token:
    value: str
    type: str
    frequency: int
    context: str


@dataclass
class TokenizedRepo:
    tokens: List[Token]
    total_tokens: int
    unique_tokens: int
    token_distribution: Dict[str, int]
    metadata: Dict


class RepoTokenizer:
    def __init__(self):
        pass
    
    def tokenize_repo(self, files: List[Tuple[str, str]]) -> TokenizedRepo:
        all_tokens = []
        for file_path, content in files:
            all_tokens.extend(self._tokenize_file(file_path, content))
        
        counter = Counter(t.value for t in all_tokens)
        for token in all_tokens:
            token.frequency = counter[token.value]
        
        token_distribution = {}
        for token in all_tokens:
            token_distribution[token.type] = token_distribution.get(token.type, 0) + 1
        
        return TokenizedRepo(
            tokens=all_tokens, total_tokens=len(all_tokens),
            unique_tokens=len(counter), token_distribution=token_distribution,
            metadata={"files_processed": len(files), "avg_tokens_per_file": len(all_tokens) / len(files) if files else 0}
        )
    
    def _tokenize_file(self, file_path, content):
        file_type = self._get_file_type(file_path)
        if file_type == 'code': return self._tokenize_code(file_path, content)
        elif file_type == 'config': return self._tokenize_config(file_path, content)
        else: return self._tokenize_text(file_path, content)
    
    def _get_file_type(self, file_path):
        if any(file_path.endswith(e) for e in ['.py', '.js', '.ts', '.tsx', '.jsx', '.rs', '.go', '.java', '.rb', '.php']): return 'code'
        if any(file_path.endswith(e) for e in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']): return 'config'
        return 'text'
    
    def _tokenize_code(self, file_path, content):
        tokens = []
        for line_num, line in enumerate(content.split('\n'), 1):
            func_match = re.search(r'def\s+(\w+)|function\s+(\w+)|const\s+(\w+)\s*=', line)
            if func_match:
                func_name = next(g for g in func_match.groups() if g)
                tokens.append(Token(value=func_name, type='code', frequency=0, context=f"{file_path}:{line_num}"))
            endpoint_match = re.search(r'@(route|get|post|put|delete)\([\'"]([\'"]+)[\'"]\)', line)
            if endpoint_match:
                tokens.append(Token(value=endpoint_match.group(2), type='endpoint', frequency=0, context=f"{file_path}:{line_num}"))
        return tokens
    
    def _tokenize_config(self, file_path, content):
        tokens = []
        for match in re.finditer(r'(\w+)\s*[:=]\s*[\'"']?([^\'"\n]+)[\'"']?', content):
            tokens.append(Token(value=match.group(1), type='config', frequency=0, context=file_path))
        return tokens
    
    def _tokenize_text(self, file_path, content):
        return [Token(value=w, type='text', frequency=0, context=file_path) for w in re.findall(r'\b\w+\b', content.lower()) if len(w) > 3]
    
    def get_top_tokens(self, tokenized_repo, n=20):
        return sorted(tokenized_repo.tokens, key=lambda t: t.frequency, reverse=True)[:n]
    
    def get_endpoint_tokens(self, tokenized_repo):
        return [t for t in tokenized_repo.tokens if t.type == 'endpoint']
