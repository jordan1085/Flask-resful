from flask import Response
from flask_restful import Resource, fields, marshal_with, reqparse

from werkzeug.exceptions import BadRequest


from proyect_app.book.models import Book, Category, Tag, Dimention, Address

cate_tags_fields = {
        '_id': fields.String,
        'name': fields.String 
}

cate_tags_fields_api = {
        'pk': fields.String,
        'name': fields.String 
}

address_fields = {
    'country': fields.String,
    'direction': fields.String 
}

dimention_fields = {
    'x': fields.Integer,
    'y': fields.Integer,
    'z': fields.Integer,
}

resource_fields = {
    '_id': fields.String,
    'name': fields.String,
    'content': fields.String,
    'dimention': fields.Nested(dimention_fields),
    'addresses': fields.Nested(address_fields),
    'category':fields.Nested(cate_tags_fields),
    'tags': fields.Nested(cate_tags_fields),
}

pipes = [
    {'$lookup': {
        'from' : Category._get_collection_name(),
        'localField': 'category',
        'foreignField': '_id',
        'as' : 'category'
    }},
    {
        '$unwind':"$category"
    },
    {'$lookup': {
        'from' : Tag._get_collection_name(),
        'localField': 'tags',
        'foreignField': '_id',
        'as' : 'tags'
    }},
    #{'$unwind':"$tags"}
]

class BookApi(Resource):

    @marshal_with(resource_fields,envelope='books')
    def get(self):

        books = Book.objects.aggregate(pipes)

        return list(books)

    @marshal_with(resource_fields, envelope='book')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        parser.add_argument('content', required=True, help="No mandastes el contenido")
        parser.add_argument('category_id', required=True, help="No mandastes la categoría")
        parser.add_argument('dimention-x', required=True, help="No mandastes la dimención x")
        parser.add_argument('dimention-y', required=True, help="No mandastes la dimención y")
        parser.add_argument('dimention-z', required=True, help="No mandastes la dimención z")
        
        args = parser.parse_args()

        book = Book(name=args['name'], content=args['name'])
        
        try:
            category = Category.objects.get(pk=args['category_id'])
        except Category.DoesNotExist:
            raise BadRequest('Categoria no existe') 
        
        book.category=category

        dimention = Dimention(x=args['dimention-x'], y=args['dimention-y'], z=args['dimention-z'])
        book.dimention = dimention

        book.save()
        #book = Book.objects.get(_id=book.pk)

        books = Book.objects(_id=book.pk).aggregate(pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return

        return book
        
    """def get(self):
        books = Book.objects.to_json()
        return Response(books, mimetype="application/json",status=200)"""

class BookApiId(Resource):
    @marshal_with(resource_fields, envelope='book')
    def get(self,id):
        books = Book.objects(_id=id).aggregate(pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return
        
        return book

    """ def get(self,id):
        book = Book.objects.get(_id=id).to_json()
        return Response(book, mimetype="application/json",status=200)"""

    @marshal_with(resource_fields, envelope='book')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        parser.add_argument('content', required=True, help="No mandastes el contenido")
        parser.add_argument('category_id', required=True, help="No mandastes la categoría")
        parser.add_argument('dimention-x', required=True, help="No mandastes la dimención x")
        parser.add_argument('dimention-y', required=True, help="No mandastes la dimención y")
        parser.add_argument('dimention-z', required=True, help="No mandastes la dimención z")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)
        book.name= args['name']
        book.content= args['content']

        try:
            category = Category.objects.get(pk=args['category_id'])
        except Category.DoesNotExist:
            raise BadRequest('Categoria no existe') 

        book.category=category

        dimention = Dimention(x=args['dimention-x'], y=args['dimention-y'], z=args['dimention-z'])
        book.dimention = dimention

        book.save()

        #print(book._id)
        #print(book.pk)

        #book = Book.objects.get(_id=book.pk)
        books = Book.objects(_id=id).aggregate(pipes)
        try:
            book = list(books)[0]
        except IndexError:
            return
        
        return book
    
    def delete(self,id):
        Book.objects(_id=id).delete()
        return {'msj':'ok'}


class CategoryBookApiId(Resource):

    @marshal_with(resource_fields, envelope='book')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('category_id', required=True, help="No mandastes la categoría")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        category = Category.objects.get(pk=args['category_id'])
        book.category=category

        book.save()

        books = Book.objects(_id=book._id).aggregate(pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return
        
        return book


class TagAddBookApiId(Resource):

    @marshal_with(resource_fields, envelope='book')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('tag_id', required=True, help="No mandastes el tag")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        tag = Tag.objects.get(pk=args['tag_id'])
        book.tags.append(tag)

        book.save()

        books = Book.objects(_id=id).aggregate(pipes)
        try:
            book = list(books)[0]
        except IndexError:
            return
        
        return book

class TagRemoveBookApiId(Resource):

    @marshal_with(resource_fields, envelope='book')
    def delete(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('tag_id', required=True, help="No mandastes el tag")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        tag = Tag.objects.get(pk=args['tag_id'])

        try:
            book.tags.remove(tag)
            book.save()
        except ValueError:
            pass

        books = Book.objects(_id=book._id).aggregate(pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return

        return book

class AddressAddBookApiId(Resource):

    @marshal_with(resource_fields, envelope='book')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('direction', required=True, help="No mandastes la dirección")
        parser.add_argument('country', required=True, help="No mandastes el país")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        address = Address(country=args['country'], direction=args['direction'])
        book.addresses.append(address)

        book.save()

        books = Book.objects(_id=id).aggregate(pipes)
        try:
            book = list(books)[0]
        except IndexError:
            return
        
        return book

class AddressRemoveBookApiId(Resource):

    @marshal_with(resource_fields, envelope='book')
    def delete(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('index', required=True, type=int, help="No mandastes el indice o no es entero")
        
        args = parser.parse_args()

        book = Book.objects.get(_id=id)

        try:
            book.addresses.pop(args['index'])
            book.save()
        except IndexError:
            pass

        books = Book.objects(_id=book._id).aggregate(pipes)

        try:
            book = list(books)[0]
        except IndexError:
            return

        return book


#-------------------------Categoria

class CategoryApi(Resource):

    @marshal_with(cate_tags_fields_api, envelope='categories')
    def get(self):
        return list(Category.objects.all())

    @marshal_with(cate_tags_fields_api, envelope='category')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        
        args = parser.parse_args()
        category = Category(name=args['name'])
        category.save()
        #category = Category.objects.get(pk=category.pk)

        return category
        
    """def get(self):
        books = Book.objects.to_json()
        return Response(books, mimetype="application/json",status=200)"""

class CategoryApiId(Resource):
    @marshal_with(cate_tags_fields_api, envelope='category')
    def get(self,id):
        return Category.objects.get(pk=id)

    @marshal_with(cate_tags_fields_api, envelope='category')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        
        args = parser.parse_args()

        category = Category.objects.get(pk=id)
        category.name= args['name']
        category.save()

        return category
    
    def delete(self,id):
        Category.objects(pk=id).delete()
        return {'msj':'ok'}



#-------------------------Tag

class TagApi(Resource):

    @marshal_with(cate_tags_fields_api, envelope='tags')
    def get(self):
        return list(Tag.objects.all())

    @marshal_with(cate_tags_fields_api, envelope='tag')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        
        args = parser.parse_args()
        tag = Tag(name=args['name'])
        tag.save()

        return tag

class TagApiId(Resource):
    @marshal_with(cate_tags_fields_api, envelope='tag')
    def get(self,id):
        return Tag.objects.get(pk=id)

    @marshal_with(cate_tags_fields_api, envelope='tag')
    def patch(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="No mandastes el nombre")
        
        args = parser.parse_args()

        tag = Tag.objects.get(pk=id)
        tag.name= args['name']
        tag.save()

        return tag
    
    def delete(self,id):
        Tag.objects(pk=id).delete()
        return {'msj':'ok'}