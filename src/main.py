"""
Command line runner for the Music Recommender Simulation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


PROFILES = [
    {
        "name": "High-Energy Pop",
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.9, "valence": 0.85, "danceability": 0.85},
    },
    {
        "name": "Chill Lofi",
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.55, "tempo_bpm": 75, "acousticness": 0.80},
    },
    {
        "name": "Deep Intense Rock",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.95, "valence": 0.30, "tempo_bpm": 150, "danceability": 0.60},
    },
    # --- Adversarial / edge-case profiles ---
    {
        "name": "Conflicting: High Energy + Sad Mood",
        "prefs": {"genre": "pop", "mood": "sad", "energy": 0.9, "valence": 0.20},
    },
    {
        "name": "Edge Case: No Genre or Mood (Numeric Only)",
        "prefs": {"energy": 0.5, "valence": 0.5, "tempo_bpm": 100, "danceability": 0.5, "acousticness": 0.5},
    },
    {
        "name": "Edge Case: Perfect Mid-Values Across All Features",
        "prefs": {"genre": "ambient", "mood": "focused", "energy": 0.5, "valence": 0.5, "tempo_bpm": 100, "danceability": 0.5, "acousticness": 0.5},
    },
]


def run_profile(songs, profile, k=5):
    print("\n" + "=" * 50)
    print(f"  Profile: {profile['name']}")
    print(f"  Prefs  : {profile['prefs']}")
    print("=" * 50)
    recommendations = recommend_songs(profile["prefs"], songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 7.50")
        print(f"    Why   : {explanation}")
    print()


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    songs = load_songs(os.path.join(base_dir, "data", "songs.csv"))

    for profile in PROFILES:
        run_profile(songs, profile)


if __name__ == "__main__":
    main()
