from flask import Response #manejar respuesta http
from flask_restful import Resource #para crear la clase de tipo recurso

from .book.modedels import Book #importamos modulo 

#obtener todos los libros
class BookApi(Resource): #clase de tipo recurso
    def get(self):
        books = Book.objects.to_json() #convertir a json
        return Response(books, mimetype="application/json", status=200) # retornar libros, declaramos el tipo json, forzamos status 200 aunque por defecto es 200
        