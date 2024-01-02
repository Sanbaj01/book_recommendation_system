from flask import Flask, request, jsonify
import pandas
from utils import book_recommendation

books = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Books.csv')
users = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Users.csv')
ratings = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Ratings.csv')


app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        if not request.is_json:
            print("HELLO HELLO HELLO")
            return jsonify({"error": "Invalid JSON data"}), 400
        print('@'*10)
        data = request.get_json()
        book_name = data.get("book_name", "")
        print(book_name)
        if not book_name:
            return jsonify({"error": "Text is missing"}), 400
        recommend = book_recommendation(books, users, ratings, book_name)
        print(recommend)

        return recommend
    
    except Exception as e:
        print(e)
        return jsonify({"error":str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
        


