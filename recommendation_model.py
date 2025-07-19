import random

# Dummy song database
song_database = {
    "folk": ["Wilderness", "Hollow Heart", "Moonlit Song"],
    "country": ["Dust in My Boots", "Silver Strings", "Open Fields"],
    "rock": ["Shattered Sky", "Blazing Trails", "Heavy Heart"],
    "pop": ["Echoes of Us", "Shining Lights", "Dancing Shadows"]
}

def get_recommendations(user_input):
    # Basic keyword matching for genres
    for genre, songs in song_database.items():
        if genre.lower() in user_input.lower():
            return random.sample(songs, min(3, len(songs)))
    # Default fallback
    return ["No songs found matching your preference. Try another genre."]
