from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; returns (total_score, reasons) with max 7.5 points."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0
    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy closeness: 0.0–2.0
    if "energy" in user_prefs:
        energy_score = 2.0 * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score:.2f})")

    # Valence closeness: 0.0–1.0
    if "valence" in user_prefs:
        valence_score = 1.0 * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += valence_score
        reasons.append(f"valence closeness (+{valence_score:.2f})")

    # Tempo closeness: 0.0–0.5
    if "tempo_bpm" in user_prefs:
        tempo_score = 0.5 * max(0, 1 - abs(song["tempo_bpm"] - user_prefs["tempo_bpm"]) / 80)
        score += tempo_score
        reasons.append(f"tempo closeness (+{tempo_score:.2f})")

    # Danceability closeness: 0.0–0.5
    if "danceability" in user_prefs:
        dance_score = 0.5 * (1 - abs(song["danceability"] - user_prefs["danceability"]))
        score += dance_score
        reasons.append(f"danceability closeness (+{dance_score:.2f})")

    # Acousticness closeness: 0.0–0.5
    if "acousticness" in user_prefs:
        acoustic_score = 0.5 * (1 - abs(song["acousticness"] - user_prefs["acousticness"]))
        score += acoustic_score
        reasons.append(f"acousticness closeness (+{acoustic_score:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top-k as (song, score, explanation) tuples."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    # sorted() returns a new list, leaving the original `songs` unchanged.
    # .sort() would mutate the list in place — we use sorted() here so the
    # caller's catalog order is preserved.
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
