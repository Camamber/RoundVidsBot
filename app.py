import cherrypy
import os

API_TOKEN = '543482719:AAGSzOTxA8AEoYIU8h8IAVfAlTHWbLLkRb0'

WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        return '<h1>Xyi</h1>'

config = {
    'global': {
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': int(os.environ.get('PORT', WEBHOOK_PORT)),
    }
}

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, config=config)