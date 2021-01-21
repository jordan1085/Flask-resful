from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] ={
    'db' : 'mongoflask'
}

app.config['SECRET_KEY'] = "4545a4s5a4s15a4s5a4s541"

app.debug = True

db = MongoEngine(app)

#controladores
from proyect_app.book.controllers import bookBp
app.register_blueprint(bookBp)

#RestApi
from flask_restful import Api
from proyect_app.restful.controllers import BookApi, BookApiId, CategoryBookApiId, TagAddBookApiId, TagRemoveBookApiId, AddressAddBookApiId, AddressRemoveBookApiId, CategoryApi, CategoryApiId, TagApi, TagApiId

api = Api(app)
api.add_resource(BookApi,'/api/book')
api.add_resource(BookApiId,'/api/book/<string:id>')
api.add_resource(CategoryBookApiId,'/api/book/set_category/<string:id>')
api.add_resource(TagAddBookApiId,'/api/book/add_tag/<string:id>')
api.add_resource(TagRemoveBookApiId,'/api/book/remove_tag/<string:id>')
api.add_resource(AddressAddBookApiId,'/api/book/add_address/<string:id>')
api.add_resource(AddressRemoveBookApiId,'/api/book/remove_address/<string:id>')

api.add_resource(CategoryApi,'/api/category')
api.add_resource(CategoryApiId,'/api/category/<string:id>')

api.add_resource(TagApi,'/api/tag')
api.add_resource(TagApiId,'/api/tag/<string:id>')