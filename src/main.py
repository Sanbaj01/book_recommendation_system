import numpy
import pandas
from sklearn.metrics.pairwise import cosine_similarity
from logger import logging


books = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Books.csv')
logging.info('Books read')
users = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Users.csv')
logging.info('Users read')
ratings = pandas.read_csv('/home/sanbaj/Python Projects/fun python practise/book-recommender-system/data/book-recommendation-system/Ratings.csv')
logging.info('Ratings read')

# Popularity Based Recommendation System

ratings_with_name = ratings.merge(books,on='ISBN')

num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_rating_df.rename(columns={'Book-Rating':'num_ratings'},inplace=True)

avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df.rename(columns={'Book-Rating':'avg_rating'},inplace=True)

popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')

popular_df = popular_df[popular_df['num_ratings']>=250].sort_values('avg_rating',ascending=False).head(50)

popular_df = popular_df.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Image-URL-M','num_ratings','avg_rating']]

# Collaborative Filtering Based Recommender System

# Taking only the suggestions of verocious readers
x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
verocious_readers = x[x].index

filtered_rating =ratings_with_name[ratings_with_name['User-ID'].isin(verocious_readers)]

y = filtered_rating.groupby('Book-Title').count()['Book-Rating']>=50
famous_books = y[y].index

final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]
final_ratings

# final_ratings.drop_duplicates()

pivot_table = final_ratings.pivot_table(index='Book-Title', columns='User-ID',values='Book-Rating')
pivot_table.fillna(0, inplace=True)

similarity_scores = cosine_similarity(pivot_table)

def recommend(book_name):
    # index fetch
    index = numpy.where(pivot_table.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse = True)[1:6]

    data = []
    for i in similar_items:
        print(pivot_table.index[i[0]])

book = input('Enter book name: ')
print(recommend(book))