from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('BOOK\popular.pkl','rb'))
pt = pickle.load(open('BOOK\pt.pkl' , 'rb'))
book = pickle.load(open('BOOK\_book_set.pkl' , 'rb'))
similar_score = pickle.load(open('BOOK\similar_score.pkl' , 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular_df['Book-Title'].values),
                            author = list(popular_df['Book-Author'].values),
                            img = list(popular_df['Image-URL-M'].values),
                            votes = list(popular_df['Num_of_rating'].values),
                            rating = list(popular_df['Avg_of_rating'].values))


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_book' , methods = ['post'])
def recommend(): #data set function

    user_input = request.form.get('user_input')
    
    index = np.where(pt.index == user_input)[0][0]
    similar_item = sorted(list(enumerate(similar_score[index])) , key=lambda z:z[1] , reverse=True) [1:6]
    data = []
    for i in similar_item:
       # print(pt.index[i[0]])
       item = []
       temp_df = book[book['Book-Title'] == pt.index[i[0]]]
       item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
       item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
       item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)
       item.extend(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values)
       
       data.append(item)
    #print(data)
    return render_template('recommend.html' , data = data)


if __name__ == '__main__':
    app.run(debug=True)



