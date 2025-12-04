# NerdFlix – Movie Recommendation System

A simple movie recommendation web system built with Flask and Collaborative Filtering, using a real-world movie rating dataset.  
Users quickly rate a few movies, and the system recommends movies that match their preferences based on the rating history of similar users.

---

## Main Features

- Home page displays about 20 popular movies (poster, title, genres).
- Users select a rating from 0–5 stars for movies they have watched.
- After submitting the ratings, the system:
  - Creates a new user (`new_user`),
  - Computes similarity to other users using cosine similarity,
  - Recommends 8 movies with the highest predicted scores.
- The recommendations page shows:
  - Poster
  - Title
  - Genres
  - A link that redirects directly to the movie’s IMDb page (`https://www.imdb.com/title/ttXXXXXXX`).

The UI is customized in a “Netflix clone” style (NerdFlix) with a background video.

---

## Dataset Used

This project uses the **MovieLens 1M** dataset from GroupLens Research. This is a standard (**stable benchmark dataset**) often used in recommendation systems.

* **Source URL**: [https://grouplens.org/datasets/movielens/](https://grouplens.org/datasets/movielens/)
* **Topic**: Movie Ratings.
* **Scale (MovieLens 1M)**:
    * **Number of Ratings**: 1 million (1,000,000) ratings.
    * **Number of Users**: 6,000 users.
    * **Number of Movies**: 4,000 movies.

---

## Technologies Used

- Python 3.x
- Flask – Web framework
- Pandas, NumPy – Data processing
- scikit-learn – `cosine_similarity` for collaborative filtering
- HTML/CSS + Bootstrap Icons – Frontend UI

---

## Suggested Project Structure

```bash
project_root/
│
├─ app.py
├─ movie_recommend_system.py
│
├─ data/
│   ├─ 100k_final_dataset.csv
│   └─ userId_movieId_matrix.pkl
│
├─ KNN/
│   ├─ KNNBasic_Build_Project_AIL303.ipynb
│   ├─ KNNBasic_from_surprise_Project_AIL303.ipynb
│   ├─ Movie_recomend_System.ipynb
│   └─ Sparse_KNN_test.ipynb
│
├─ templates/
│   ├─ index.html
│   └─ recommendations.html
│
└─ README.md
