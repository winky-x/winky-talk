"""
Compatibility layer that provides fuzzywuzzy API using RapidFuzz backend
"""
from rapidfuzz import fuzz, process
from rapidfuzz.utils import default_process

def ratio(s1, s2, processor=default_process):
    return fuzz.ratio(s1, s2, processor=processor)

def partial_ratio(s1, s2, processor=default_process):
    return fuzz.partial_ratio(s1, s2, processor=processor)

def token_sort_ratio(s1, s2, processor=default_process):
    return fuzz.token_sort_ratio(s1, s2, processor=processor)

def token_set_ratio(s1, s2, processor=default_process):
    return fuzz.token_set_ratio(s1, s2, processor=processor)

def extract(query, choices, processor=default_process, scorer=ratio, limit=5):
    return process.extract(
        query,
        choices,
        processor=processor,
        scorer=scorer,
        limit=limit
    )

def extractOne(query, choices, processor=default_process, scorer=ratio):
    return process.extractOne(
        query,
        choices,
        processor=processor,
        scorer=scorer
    )