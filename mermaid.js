const diagram = `
flowchart TD
    A([songs.csv]) --> B[Parse song row\nid · title · artist · genre · mood\nenergy · tempo_bpm · valence\ndanceability · acousticness]
    B --> C{song.genre ==\nuser.favorite_genre?}
    C -- Yes --> D[genre_match = 2.0]
    C -- No  --> E[genre_match = 0.0]

    D & E --> F{song.mood ==\nuser.favorite_mood?}
    F -- Yes --> G[mood_match = 1.0]
    F -- No  --> H[mood_match = 0.0]

    G & H --> I["energy_score = 2.0 × (1 − |song.energy − target_energy|)"]
    I --> J["valence_score = 1.0 × (1 − |song.valence − target_valence|)"]
    J --> K["tempo_score = 0.5 × max(0, 1 − |song.tempo_bpm − target_tempo| ÷ 80)"]
    K --> L["danceability_score = 0.5 × (1 − |song.danceability − target_danceability|)"]
    L --> M["acousticness_score = 0.5 × (1 − |song.acousticness − target_acousticness|)"]

    M --> N["total_score = genre_match + mood_match
    + energy_score + valence_score
    + tempo_score + danceability_score
    + acousticness_score"]

    N --> O[(Score cache\nsong_id → total_score)]
    O --> P{More songs\nin CSV?}
    P -- Yes --> B
    P -- No  --> Q[Sort all songs\nby total_score DESC]
    Q --> R([Top-N ranked recommendations])
`;

export default diagram;
