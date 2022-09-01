from databases import Database
from sanic import Sanic, exceptions, response
from environs import Env

from settings import Settings
from routes import routes

app = Sanic(__name__)
env = Env()
env.read_env()


def db_setup():
    app.db = (Database(env.str("DB_URL")))
    
    @app.listener('before_server_start')
    async def connect_db(app, loop):
        await app.db.connect()

    @app.listener('after_server_stop')
    async def disconnect_db(app, loop):
        await app.db.disconnect()


if __name__ == '__main__':

    app.config.from_object(Settings)
    
    db_setup()
    routes(app)
    app.run(host=app.config.HOST, port=app.config.PORT, debug=app.config.DEBUG)
