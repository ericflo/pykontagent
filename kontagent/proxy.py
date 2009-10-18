import sys
import urllib

from twisted.web import client
from twisted.web.server import Site
from twisted.web.resource import Resource

from twisted.internet.task import deferLater
from twisted.internet import reactor

from twisted.python import log

class KontagentProxyResource(Resource):
    isLeaf = True
    
    def proxy_request(self, path, args):
        # Re-build the querystring from the args
        qs = urllib.urlencode([(k, v[0]) for k, v in args.iteritems()])
        # Construct the URL to the actual kontagent server
        url = ''.join(('http://api.geo.kontagent.net', path, '?', qs))
        # Log the request for our records
        log.msg(url)
        # Send the request to their servers
        d = client.getPage(url=url)
        # Do a single 2-second fallback if their server starts to fall over.
        d.addErrback(lambda e: deferLater(reactor, 2, client.getPage, url=url))
        return d
    
    def render_GET(self, request):
        '''
        Respond immediately, but defer a request to the Kontagent servers.
        '''
        path = request.path
        args = request.args
        d = deferLater(reactor, 0.001, self.proxy_request, path, args)
        return 'ok'

if __name__ == '__main__':
    root = KontagentProxyResource()
    factory = Site(root)
    log.startLogging(sys.stdout)
    reactor.listenTCP(8880, factory)
    reactor.run()