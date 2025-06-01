import json
import os
from datetime import datetime

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def handle_calendar(user_input):
    calendar_path = os.path.join('data', 'calendar.json')
    profile_path = os.path.join('data', 'profile.json')
    calendar = load_json(calendar_path)
    profile = load_json(profile_path)
    prefs = profile.get('meeting_preferences', {})
    preferred_times = prefs.get('preferred_times', [])
    avoid_days = [d.lower() for d in prefs.get('avoid_days', [])]
    suggestions = []
    for date, slots in calendar.items():
        day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A').lower()
        if day_name in avoid_days:
            continue
        for slot in slots:
            for pref in preferred_times:
                if slot.startswith(pref.split('-')[0]):
                    suggestions.append(f"{date} {slot}")
    if not suggestions:
        return "No preferred slots available."
    return "Suggested slots:\n" + "\n".join(suggestions[:5]) 