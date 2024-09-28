from db import DB
from flask import Flask, jsonify
from models import NewsModel
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'qwerty123'
db = DB()
NewsModel(db.get_connection()).init_table()

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, location='form')
parser.add_argument('content', type=str, required=True, location='form')


def abort_if_news_not_found(news_id):
    if not NewsModel(db.get_connection()).get(news_id):
        abort(404, message="News {} not found".format(news_id))


class News(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        news = NewsModel(db.get_connection()).get(news_id)
        return jsonify({'news': news})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        NewsModel(db.get_connection()).delete(news_id)
        return jsonify({'success': 'OK'})


class NewsList(Resource):
    def get(self):
        news = NewsModel(db.get_connection()).get_all()
        return jsonify({'news': news})

    def post(self):
        args = parser.parse_args()
        news = NewsModel(db.get_connection())
        news.insert(args['title'], args['content'])
        return jsonify({'success': 'OK'})


api.add_resource(NewsList, '/news')
api.add_resource(News, '/news/<int:news_id>')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
