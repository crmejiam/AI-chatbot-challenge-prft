import yaml
import os
import difflib

KB_PATH = os.path.join(os.path.dirname(__file__), '../data/github_actions_faq.yaml')

def load_kb():
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        kb = yaml.safe_load(f)
    return kb['faqs']

def retrieve_relevant_entries(query, top_n=3):
    kb_entries = load_kb()
    # Use simple string similarity for demo purposes
    scored = []
    for entry in kb_entries:
        score = difflib.SequenceMatcher(None, query.lower(), entry['question'].lower()).ratio()
        scored.append((score, entry))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [entry for score, entry in scored[:top_n] if score > 0.3]  # Only return relevant

# Example usage:
# results = retrieve_relevant_entries("How do I use secrets?")
# for r in results:
#     print(r['question'], r['answer'])
