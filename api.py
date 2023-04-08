from flask import Flask, jsonify, render_template, request
import pickle
import numpy as np
import pandas as pd

popular_df = pd.read_pickle(open('popular.pkl','rb'))
pt = pd.read_pickle(open('pt.pkl','rb'))
books = pd.read_pickle(open('books.pkl','rb'))
similarity_scores = pd.read_pickle(open('similarity_scores.pkl','rb'))

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    data = []

    book_name = list(popular_df['Book-Title'].values),
    author=list(popular_df['Book-Author'].values),
    image=list(popular_df['Image-URL-M'].values),
    votes=list(popular_df['num_ratings'].values),
    rating=list(popular_df['avg_rating'].values)
    print(f"this is book_name {book_name}")
    return jsonify({
        'book_name': book_name,
        'author': author,
        'image': image,
        'votes': votes,
        'rating': rating,
        })
    # return render_template('index.html',
    #                        book_name = list(popular_df['Book-Title'].values),
    #                        author=list(popular_df['Book-Author'].values),
    #                        image=list(popular_df['Image-URL-M'].values),
    #                        votes=list(popular_df['num_ratings'].values),
    #                        rating=list(popular_df['avg_rating'].values)
    #                        )


@app.route('/<string:book_name>/<int:books_count>',methods=['post'])
def recommend(book_name, books_count):
    # user_input = request.form.get('user_input')
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:books_count+1]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return jsonify(data)




if __name__ == '__main__':
    app.run(debug = True)