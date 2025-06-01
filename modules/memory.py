import json
import os

_memory_buffer = []

def get_user_profile():
    profile_path = os.path.join('data', 'profile.json')
    with open(profile_path, 'r') as f:
        return json.load(f)

def add_to_memory(prompt, response):
    _memory_buffer.append({'prompt': prompt, 'response': response})
    if len(_memory_buffer) > 20:
        _memory_buffer.pop(0)

def get_memory():
    return list(_memory_buffer) 