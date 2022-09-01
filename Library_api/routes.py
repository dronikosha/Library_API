from sanic import Sanic, response, exceptions
from tables import books


def routes(app):
    @app.route('/books', methods=['GET'])
    async def get_books(request):
        query = books.select()
        books_list = await app.db.fetch_all(query)
        return response.json(books_list)

    @app.route('/books', methods=['POST'])
    async def add_book(request):
        query = books.insert().values(
            title=request.json['title'],
            author=request.json['author'],
            year=request.json['year']
        )
        last_record_id = await app.db.execute(query)
        return response.json({'id': last_record_id})

    @app.route('/books/<book_id:int>', methods=['PUT'])
    async def update_book(request, book_id):
        query = books.update().where(books.c.id == book_id).values(
            title=request.json['title'],
            author=request.json['author'],
            year=request.json['year']
        )
        await app.db.execute(query)
        return response.json({'status': 'success'})

    @app.route('/books/<book_id:int>', methods=['DELETE'])
    async def delete_book(request, book_id):
        query = books.delete().where(books.c.id == book_id)
        await app.db.execute(query)
        return response.json({'status': 'success'})
