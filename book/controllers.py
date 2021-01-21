
from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from .models import Book, BookForm, Category, Dimention, Address, AddressForm, Tag

bookBp = Blueprint('book',__name__, url_prefix='/book')

@bookBp.route('/')
@bookBp.route('/<int:page>')
def index(page=1):
    #save_category()
    #save_tag()
    return get_list_paginate(page,BookForm(),AddressForm())

@bookBp.route('/add', methods=('GET','POST'))
def add():
    form=BookForm(request.form)
    addressForm=AddressForm(request.form)

    if request.method == 'GET':
        return redirect(url_for('book.index'))

    if request.method == 'POST' and form.validate():
        book = Book()
        book.setByForm(form,addressForm)
        book.save()
        #book = Book(name=form.name.data, content=form.content.data)
        #book.save()
        #print(form.csrf_token.data)

        #del form.csrf_token
        #del form.dimention.csrf_token
        #form.save()
        return redirect(url_for('book.index'))

    #if form.errors:
        #print(form.errors)

    return get_list_paginate(1,form,addressForm)

    #return render_template('book/add.html', form=BookForm())

@bookBp.route('/update/<string:id>', methods=('POST','GET'))
def update(id):

    if request.method == 'GET':
        return redirect(url_for('book.index'))

    book = Book.objects.get_or_404(_id=id)

    form=BookForm(request.form)
    addressForm=AddressForm(request.form)

    if request.method == 'POST' : #and form.validate()
        #book.name = form.name.data
        #book.content = form.content.data
        book.setByForm(form,addressForm)
        #--- fk dr
        #c = Category.objects.get(pk="5f79cd05d0f9966a402f22dd")
        #book.category = c
        #--- documento embebido
        #book.dimention = Dimention(x=1,y=2,z=3)
        #---- de array
        #book.addresses.append(Address(country="España", direction="Dirección test 2"))
        #book.addresses = [Address(country="España", direction="Dirección test 2"), Address(country="Venezuela", direction="Dirección test")]

        # dr muchos a muchos
        #tag = Tag.objects.get(pk="5f7a172edfad97d976e44be3")
        #tag2 = Tag.objects.get(pk="5f7a172edfad97d976e44be5")
        #book.tags.append(tag)
        #book.tags.append(tag2)
        #book.tags = [tag, tag2]

        book.save()
        return redirect(url_for('book.index'))
    
    print(form.errors)

    return get_list_paginate(1, form, addressForm)

@bookBp.route('/delete/<string:id>', methods=('POST',))
def delete(id):

    book = Book.objects(_id=id).delete()
    return redirect(url_for('book.index'))

#------------Funciones de ayuda

def get_list_paginate(page, form, addressForm):
    return render_template('book/index.html', books=Book.objects.paginate(page=page, per_page=3), form=form, addressForm=addressForm)

#------------Funciones json

@bookBp.route('get-detial-by-id/<string:id>')
def getDetailById(id):
    return jsonify(Book.objects.get(_id=id))

#------------Test

def save_tag():
    tag = Tag(name="Tag 1")
    tag.save()
    tag = Tag(name="Tag 2")
    tag.save()
    tag = Tag(name="Tag 3")
    tag.save()

def save_category():
    category = Category(name="Cate 1")
    category.save()
    category = Category(name="Cate 2")
    category.save()
    category = Category(name="Cate 3")
    category.save()

def update_document():
    book = Book.objects.get_or_404(_id='5f6f4b31c8be02ceb8437e8d')
    book.name = "Harry Potter"
    book.save()
    print(book)
    book = Book.objects.get_or_404(_id='5f6f4b31c8be02ceb8437e8d')
    print(book)

def get_document_by_id():
    #book = Book.objects.get(_id='5f6e6984c518f9eb5b412909')
    book = Book.objects.get_or_404(_id='5f6f4b31c8be02ceb8437e8d')
    print(book._id)

def save_document():
    book = Book(name="GOT", content="Vientos de invierno")
    book.save()

def delete_document():
    book = Book(name="GOT", content="Vientos de invierno")
    book.save()
    print(book.pk)
    #book.delete()

    Book.objects(_id=book.pk).delete()
    #print(book.pk)
    #print(book._id)
    #book.delete() # si va a funcionar
    #book = Book.objects(_id=book.pk).delete()
    

def get_document():
    book = Book.objects(name="GOT").first()
    print(book._id)
    print(book.name)

def get_documents():
    books = Book.objects(name="GOT").all()
    print(books)
    