from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/api/list', methods=['GET'])
def show_average():

    averages = list(db.price.find({},{'_id': False}).sort({'average': -1}))
    return jsonify({'average_list': averages})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)