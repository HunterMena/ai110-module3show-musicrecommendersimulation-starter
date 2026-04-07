# Reflection: Profile Comparison Notes

---

## High-Energy Pop vs. Chill Lofi

These two profiles sit at opposite ends of the energy spectrum and the results reflect that cleanly. High-Energy Pop topped out with Sunrise City (4.96 in the base run, 6.30 with valence/danceability added) — a song with high BPM, high danceability, and a bright valence. Chill Lofi's top pick was Library Rain (6.90), a slow, acoustic track with energy of 0.35. The genre bonus did most of the work in both cases: when genre and mood both fire, the score gap between #1 and #2 is large enough that the numeric features only matter for tie-breaking. This makes sense — genre is the coarsest filter and it should narrow the field before energy and tempo refine it.

---

## Chill Lofi vs. Deep Intense Rock

Both profiles have clear genre matches in the catalog (lofi has 3 songs; rock has 1), but the rock catalog is much thinner. Lofi's top 2 results both matched genre and mood, while the rock profile's #1 (Storm Runner) was the only song that hit both. After that, the rock profile had to fall back on mood-only or numeric-only matches, and the scores dropped sharply from 6.70 to 4.24. This exposes a catalog skew problem: genres with more songs get better recommendations simply by having more chances to match. A user who loves rock is penalized by dataset size, not by taste.

---

## High-Energy Pop vs. Conflicting (High Energy + Sad Mood)

The conflicting profile requested `mood: sad` with `genre: pop` and `energy: 0.9`. Because `sad` doesn't appear anywhere in songs.csv, the mood bonus was never awarded — effectively the profile silently became a High-Energy Pop profile without the mood requirement. The top results (Gym Hero, Sunrise City) were identical to the standard pop profile, just in a different order because the mood tie-breaker was gone. This is a real filter bubble: the user asked for something specific and the system quietly ignored it. In a real app, this would need a warning or a fallback.

---

## Deep Intense Rock vs. Edge Case (Numeric Only)

The rock profile had clear winners because two strong categorical signals (genre + mood) separated Storm Runner from the pack immediately. The Numeric-Only profile had no categorical anchors, so all five recommendations scored between 3.90 and 4.04 — a range of just 0.14 points. The "winner" (Moonlit Cabin) was essentially random; any song with middling values across the board looked equally valid. This comparison shows that the categorical features aren't just convenience — they are structurally necessary for the scoring function to produce meaningful rankings in a small catalog.

---

## Edge Case (Numeric Only) vs. Perfect Mid-Values

Both profiles targeted center-of-range numeric values (energy 0.5, valence 0.5, etc.), but the mid-values profile also specified `genre: ambient` and `mood: focused`. Adding just those two fields pushed Spacewalk Thoughts from an unranked position all the way to #1 with a score of 5.41, while the rest of the list stayed nearly identical. This shows how much leverage the 2.0-point genre bonus has: a single categorical match is worth more than all five numeric similarity scores combined at their maximum values (max numeric total without genre/mood = 4.5). The implication is that users who don't know their preferred genre will always receive weaker, less personalized recommendations.
