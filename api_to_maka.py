from flask import Flask, jsonify, request
from flask_cors import CORS
app = app = Flask(__name__)
CORS(app)

articles = []


@app.route('/art/get/<int:artnum>', methods=['GET'])
def getart(artnum):
    if articles:
        for i in articles:
            if i['id'] == artnum:
                return jsonify(i)
    else:
        return {'message': 'wygląda na to że nie mamy jeszcze artykułów lub nastąpił reset'}
    
    return jsonify({'message': 'Artykuł o tym id nie istnieje'}), 404

article_counter = 1

@app.route('/art/addart', methods=['POST'])
def add_art():
    global article_counter
    data = request.get_json()
    
    new_art = {
        'id': article_counter,
        'title': data.get('title'),
        'body': data.get('body')
    }
    forbiden = ['<', '>', '&lt;', '&gt;', '{', '}', '/', '!', '@', '#', '$', '%', '^', '&', '*']
    chars = new_art['title'] + new_art['body']


    if  len(new_art['title']) < 31 and len(new_art['body']) < 1001:
            if any(char in forbiden for char in chars):
                return jsonify({'mes': f'BAD REQUESTS {new_art}'})
            else:
                articles.append(new_art)
                article_counter += 1 
                return jsonify({"message": "Success", "id": new_art['id']}), 201
    else:
        return jsonify({'nice': 'try'})
    
@app.route('/all', methods=['GET'])
def getall():
    return jsonify(articles)
    

if __name__ == '__main__':  
   app.run()
