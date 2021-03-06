"""
backend/server.py
~~~~~~~~~~~~~~~~~

Main entry point to the backend server for dynamic content. All operation
should be asynchronous, blocking call should be called in a separate process.

Any HTTP traffic to /api is routed here from NGINX.
"""

import os

from sanic import Sanic
from rest_response import ok, error

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
MUSIC_PATH = os.path.join(CURRENT_PATH, 'music')

app = Sanic(__name__)  # pylint: disable=invalid-name
app.config.LOGO = None

@app.route('/api')
async def index(_requests):
    """ Index endpoint. """
    return ok(version='0.1.0')


@app.route('/api/music')
async def music(_requests):
    """ Return an JSON array of music. """
    try:
        # Use a in-memory DB to store this data when available.
        return ok(music_list=os.listdir(MUSIC_PATH))

    except Exception as e:
        print(e)
        return error()


if __name__ == '__main__':
    # Sanic is not exposed to the internet directly, all traffic to /api
    # should be routed here by NGINX.
    app.run(host='0.0.0.0', port=8001, debug=True)
