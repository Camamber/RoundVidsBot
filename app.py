import cherrypy
import os
from bot import Bot

API_TOKEN = '543482719:AAGSzOTxA8AEoYIU8h8IAVfAlTHWbLLkRb0'

WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length)
            bot.update(json_string)
        else:
            raise cherrypy.HTTPError(403)


config = {
    'global': {
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': int(os.environ.get('PORT', WEBHOOK_PORT)),
    }
}
bot = Bot()
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, config=config)
