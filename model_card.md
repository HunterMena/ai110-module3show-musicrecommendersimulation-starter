# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Goal / Task

VibeFinder tries to suggest songs a user will enjoy based on their stated taste preferences. It does not predict anything — it scores every song in a catalog against a profile and returns the top 5 matches. Think of it as a search engine for vibe, not a prediction model.

---

## 3. Data Used

- **Size:** 17 songs
- **Features per song:** id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, electronic, classical, reggae, metal, soul, holiday
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, nostalgic, calm, energetic, laid-back, aggressive, yearning, festive
- **Limits:** 17 songs is too small for a real app. Several moods (sad, romantic, melancholic) and genres (country, hip-hop, R&B) are missing entirely. The dataset skews toward mid-to-high energy tracks.

---

## 4. Algorithm Summary

For each song, the system awards points in two stages:

1. **Categorical checks** — if the song's genre matches the user's favorite genre, add 2 points. If the mood matches, add 1 point. These are all-or-nothing: you either get the full bonus or zero.

2. **Numeric closeness** — for each numeric feature the user cares about (energy, valence, tempo, danceability, acousticness), calculate how close the song's value is to the user's target. A perfect match scores the full weight; a far-off value scores near zero. Energy gets the highest weight (up to 2 points) because it's the strongest signal for how a song feels. Valence gets 1 point. Tempo, danceability, and acousticness each get 0.5 points.

All points are added together (max 7.5) and songs are ranked from highest to lowest. The top 5 are returned with a plain-language explanation of why each one scored the way it did.

---

## 5. Observed Behavior / Biases

**Genre dominance:** The 2-point genre bonus is large enough that a mediocre genre-match beats a great cross-genre song almost every time. A pop song with average energy will outscore a perfect-energy jazz song just because of genre.

**Silent mood miss:** If the user's requested mood doesn't exist in the catalog (e.g., "sad"), the mood bonus never fires and the system returns genre-driven results with no warning. The user has no idea their mood preference was ignored.

**Score compression without categories:** When genre and mood are left out of the profile, all 17 songs cluster in a narrow score range (~3.9–4.0) and the ranking becomes nearly random. Numeric features alone can't meaningfully separate songs in a catalog this small.

**Catalog skew:** Genres with more songs (lofi has 3, pop has 2) naturally produce better results than genres with only 1 song (rock, ambient). A rock fan is penalized not because the algorithm is wrong, but because the data is thin.

---

## 6. Evaluation Process

Six profiles were tested — three standard and three adversarial:

| Profile | Purpose |
|---|---|
| High-Energy Pop | Baseline: genre + mood + energy all well-represented |
| Chill Lofi | Baseline: low-energy, acoustic-leaning catalog match |
| Deep Intense Rock | Baseline: thin catalog — only 1 true genre match |
| Conflicting (High Energy + Sad Mood) | Adversarial: mood not in catalog |
| Numeric Only | Edge case: no genre or mood provided |
| Perfect Mid-Values | Edge case: all features at 0.5, genre is rare |

Standard profiles produced expected results — the right songs rose to the top and the score gaps were large. The two biggest surprises: (1) the Numeric-Only profile tied all five recommendations within 0.14 points, proving that categorical features are structurally necessary; (2) the Conflicting profile silently fell back to genre-only results with no indication the mood was unmatched.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Classroom demonstration of how content-based filtering works
- Exploring how scoring weights affect recommendation quality
- Learning how to represent user preferences as data

**Not intended for:**
- Real users choosing music to listen to
- Any catalog larger than a few dozen songs (the weights were tuned for this dataset)
- Making decisions about what music is "good" or "popular"
- Users who expect their taste to be learned over time — this system has no memory and does not update from feedback

---

## 8. Ideas for Improvement

1. **Mood fallback:** Map missing moods to the closest available one (e.g., sad → yearning, energetic → intense) so users with underrepresented moods still get personalized results instead of silent genre-only output.

2. **Diversity penalty:** After scoring, check if the top 5 are all from the same genre. If so, swap in the highest-scoring song from a different genre to prevent a filter bubble when the catalog is small.

3. **Data-driven tempo normalization:** Instead of dividing by a fixed 80 BPM, compute the actual tempo range from the catalog and normalize against that, so the tempo feature has consistent influence regardless of catalog composition.

---

## 9. Personal Reflection

**Biggest learning moment:** The hardest part wasn't writing the scoring logic — it was realizing how much a small catalog distorts every result. When only 1 song matches a genre, the recommender isn't really recommending; it's just finding the only option. That made it clear why real systems need thousands of items before the math actually means anything.

**How AI tools helped, and when I double-checked:** AI was useful for quickly drafting the scoring formula and suggesting the `sorted()` vs `.sort()` distinction. But I had to verify the output manually — the formula looked right syntactically but I still needed to run it against real profiles to confirm the weights felt balanced. The adversarial profiles were the real test, not code review.

**What surprised me about simple algorithms:** Even with seven hand-crafted rules and no machine learning at all, the output *feels* personalized. When Sunrise City came back as #1 for the pop/happy/0.8 profile with a clean reason ("genre match, mood match, energy closeness"), it felt like the system understood the user. That's a useful reminder: the "magic" in a recommender isn't always the model — it's the transparency and the framing.

**What I'd try next:** I'd add a second pass after scoring that checks result diversity, and I'd build a simple feedback loop — thumbs up or down — that adjusts the genre weight up or down for the next run. That would turn VibeFinder from a static filter into something that actually learns.
