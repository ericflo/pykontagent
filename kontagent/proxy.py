import urllib

from optparse import OptionParser

from twisted.web import client
from twisted.web.server import Site
from twisted.web.resource import Resource

from twisted.internet.task import deferLater
from twisted.internet import reactor

from twisted.python import log
from twisted.python.logfile import DailyLogFile

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
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename', default='log.txt',
        help='log data to to FILE', metavar='FILE')
    parser.add_option('-d', '--dir', dest='directory', default='.',
        help='store log files in DIRECTORY', metavar='DIRECTORY')
    parser.add_option('-p', '--port', dest='port', default=8880,
        help='listen on port PORT', metavar='PORT')
    (options, args) = parser.parse_args()
    root = KontagentProxyResource()
    factory = Site(root)
    print 'Proxying Kontagent requests on port %s' % (options.port,)
    print 'Logging Kontagent requests to file %s in directory %s' % (
        options.filename, options.directory
    )
    log_file = DailyLogFile(options.filename, options.directory)
    log.startLogging(log_file, setStdout=False)
    reactor.listenTCP(int(options.port), factory)
    reactor.run()