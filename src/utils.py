"""
US2T - Utility functions
"""

import json
import re
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np


def extract_json(text: str) -> List[Dict]:
    """
    Extract JSON array from text.
    
    Args:
        text: Text containing JSON
        
    Returns:
        List of dictionaries
    """
    if not text:
        return []
    
    start = text.find("[")
    if start == -1:
        return []
    
    bracket = 0
    end = -1
    
    for i in range(start, len(text)):
        if text[i] == "[":
            bracket += 1
        elif text[i] == "]":
            bracket -= 1
            if bracket == 0:
                end = i
                break
    
    if end == -1:
        return []
    
    candidate = text[start:end + 1]
    
    # Clean JSON
    candidate = candidate.replace("'", '"')
    candidate = re.sub(r',\s*}', '}', candidate)
    candidate = re.sub(r',\s*]', ']', candidate)
    candidate = re.sub(r'\\"', '"', candidate)
    
    try:
        obj = json.loads(candidate)
        if isinstance(obj, list):
            return obj
    except:
        pass
    
    return []


def repair_json(text: str) -> List[Dict]:
    """
    Try to repair malformed JSON.
    
    Args:
        text: Malformed JSON text
        
    Returns:
        List of dictionaries
    """
    if not text:
        return []
    
    start = text.find("[")
    if start == -1:
        return []
    
    text = text[start:]
    
    # Fix common issues
    text = text.replace("'", '"')
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)
    text = re.sub(r'\\"', '"', text)
    
    # Add missing closing brackets
    while text.count("{") > text.count("}"):
        text += "}"
    while text.count("[") > text.count("]"):
        text += "]"
    
    try:
        obj = json.loads(text)
        if isinstance(obj, list):
            return obj
    except:
        pass
    
    return []


def calculate_similarity(text1: str, text2: str, embedder=None) -> float:
    """
    Calculate semantic similarity between two texts.
    
    Args:
        text1: First text
        text2: Second text
        embedder: Sentence transformer model
        
    Returns:
        Similarity score between 0 and 1
    """
    if embedder is None:
        return 0.0
    
    try:
        emb1 = embedder.encode(text1)
        emb2 = embedder.encode(text2)
        
        similarity = np.dot(emb1, emb2) / (
            np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-8
        )
        
        return float(similarity)
    except:
        return 0.0


def load_benchmark(project_path: str) -> List[Dict]:
    """
    Load benchmark stories from JSON file.
    
    Args:
        project_path: Path to stories.json file
        
    Returns:
        List of stories
    """
    with open(project_path, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    return stories


def save_benchmark_results(results: List[Dict], output_path: str) -> None:
    """
    Save benchmark results to file.
    
    Args:
        results: List of results
        output_path: Output file path
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)


def format_test_case_table(test_cases: List) -> pd.DataFrame:
    """
    Format test cases as pandas DataFrame.
    
    Args:
        test_cases: List of TestCase objects
        
    Returns:
        DataFrame with test cases
    """
    data = []
    for tc in test_cases:
        data.append({
            "ID": tc.id,
            "Type": tc.type,
            "Preconditions": tc.preconditions,
            "Input": tc.input,
            "Steps": tc.steps,
            "Expected Result": tc.expected_result,
            "Covered AC": ", ".join(tc.covered_ac) if tc.covered_ac else "",
            "Explanation": tc.explanation
        })
    
    return pd.DataFrame(data)
