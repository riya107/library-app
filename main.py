from flask import Flask,render_template,request
import json
from flask import jsonify
from flask.helpers import url_for
from werkzeug.utils import redirect
from datetime import date,timedelta

app=Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/collection',methods=['POST'])
def collection_page():
    username=request.form.get('Username')
    password=request.form.get('Password')

    with open('users.json','r') as users_file:
        users=dict(json.load(users_file))
    
    
    if(username not in users.keys()):
        return redirect(url_for('signup_page'))
    
    if(users[username]['Password']!=password):
        return redirect(url_for('invalid_password'))

    return render_template('mycollection.html',user=users[username])

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/issue',methods=['POST','GET'])
def issue_page():
    username=request.form.get('Username')
    password=request.form.get('Password')
    book=request.form.get('Book')

    with open('users.json','r') as users_file:
        users=dict(json.load(users_file))
    
    with open('available_books.json','r') as avail_books:
        categories=dict(json.load(avail_books))
    
    if(username not in users.keys()):
        return redirect(url_for('signup_page'))
    
    if(users[username]['Password']!=password):
        return redirect(url_for('invalid_password'))

    for category in categories:
        for category_book in categories[category]:
            if(category_book['Name']==book):
                remove_book=category_book
                categories[category].remove(category_book)

    remove_book['Issue Date']=str(date.today())
    remove_book['Due Date']=str(date.today()+timedelta(days=20))

    if('Books' not in users[username]):
        users[username]["Books"]={}
        users[username]["Books"][book]=remove_book

    else:
        users[username]["Books"][book]=remove_book


    with open('users.json','w') as users_file:
        json.dump(users,users_file)


    with open('available_books.json','w') as avail_books:
        json.dump(categories,avail_books)

    return render_template('collection.html',user=users[username])

@app.route('/return',methods=['POST'])
def return_book():
    returned_book=request.get_json()['returned_book']
    username=request.get_json()['username']

    with open('users.json','r') as users_file:
        users=dict(json.load(users_file))
    
    with open('available_books.json','r') as avail_books_file:
        avail_books=dict(json.load(avail_books_file))

    with open('all_books.json','r') as all_books_file:
        all_books=dict(json.load(all_books_file))

    for category in all_books:
        for book in all_books[category]:
            if book['Name']==returned_book:
                type_of_book=category
                book_dict=book

    avail_books[type_of_book].append(book_dict)
    
    del users[username]['Books'][returned_book]

    with open('available_books.json','w') as file:
        json.dump(avail_books,file)

    with open('users.json','w') as file:
        json.dump(users,file)

    return {'done':'done'}

@app.route('/invalid')
def invalid_password():
    return render_template('invalid.html')

@app.route('/take')
def take_books():
    with open('available_books.json','r') as books_file:
        books=dict(json.load(books_file))
    return render_template('take_books.html',books=books)

@app.route('/thankyou',methods=['POST'])
def thank_you():
    with open('users.json','r') as users_file:
        users=dict(json.load(users_file))

    name=request.form.get('Name')
    username=request.form.get('Username')

    for user in users:
        if(user==username):
            return render_template('already.html') 
    
    users[username]=request.form

    with open('users.json','w') as users_file:
        json.dump(users,users_file)

    return render_template('thankyou.html',name=name)

@app.route('/books',methods=['POST'])
def send_books():
    category=request.get_json()['category']
    with open('available_books.json','r') as books_file:
        books=dict(json.load(books_file))
    return jsonify(books[category])

if __name__=='__main__':
    app.run(debug=True)