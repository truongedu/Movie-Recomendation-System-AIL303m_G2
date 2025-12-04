from flask import Flask, render_template, request, redirect
import random

from movie_recommend_system import rating_df, users_movies_matrix, get_popular_top_rated_movies, recommend_movies_for_new_user

app = Flask(__name__)


@app.route('/')
def home():
    """
    Hiển thị trang chủ với các phim phổ biến để người dùng đánh giá.
    """
    
    popular_movies = get_popular_top_rated_movies(rating_df, n_recommend=20)
    # Chuyển DataFrame thành list of dictionaries để dễ dàng duyệt trong template
    return render_template('index.html', movies=popular_movies.to_dict(orient='records'))


@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Nhận đánh giá từ người dùng, gọi hàm gợi ý và hiển thị kết quả.
    """
    movie_ratings = {}
    for movie_id, rating in request.form.items():
        if int(rating) > 0:
            movie_ratings[int(movie_id)] = float(rating)
            
    # Nếu người dùng không đánh giá phim nào, quay lại trang chủ
    if not movie_ratings:
        return redirect('/')

    new_user_id = random.randint(1000000, 2000000)

    
    recommendations = recommend_movies_for_new_user(
        user_id=new_user_id,
        movie_ratings=movie_ratings,
        users_movies_matrix=users_movies_matrix,
        rating_df=rating_df,
        n_recommend=8 # Lấy 8 phim gợi ý
    )

    # Gửi kết quả đến trang recommendations.html để hiển thị
    return render_template('recommendations.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)