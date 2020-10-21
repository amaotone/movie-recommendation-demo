import pandas as pd

import scipy.sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
import joblib
from tqdm import tqdm

# load data
review = pd.read_csv("./data/review.csv")
user_enc = LabelEncoder()
movie_enc = LabelEncoder()
review["user_id"] = user_enc.fit_transform(review.user_id)
review["movie_id"] = movie_enc.fit_transform(review.movie_id)
joblib.dump(movie_enc, "./model/movie_encoder.pkl")

# create review matrix
n_users = review.user_id.nunique()
n_movies = review.movie_id.nunique()
matrix = scipy.sparse.csr_matrix(
    (review.point, (review.user_id, review.movie_id)), shape=(n_users, n_movies)
)

# train models
for n_components in tqdm([10, 20, 30, 100, 200, 500, 1000, 2000]):
    model = TruncatedSVD(n_components)
    model.fit(matrix)
    joblib.dump(model, f"./model/svd_{n_components}.pkl")
