"""
Command line runner for the Music Recommender Simulation.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


def main() -> None:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    songs = load_songs(os.path.join(base_dir, "data", "songs.csv"))

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 45)
    print("  Top Recommendations for Your Profile")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}  |  Energy: {user_prefs['energy']}")
    print("=" * 45)

    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f} / 7.50")
        print(f"    Why   : {explanation}")

    print("\n" + "=" * 45)


if __name__ == "__main__":
    main()
