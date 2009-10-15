import hashlib
import httplib
import socket
import time
import urllib

VAR_MAP = {
    'sender_uid': 's',
    'recipient_uids': 'r',
    'recipient_uid': 'r',
    'template_id': 't',
    'tracking_tag': 'u',
    'short_tracking_tag': 'su',
    'subtype_1': 'st1',
    'subtype_2': 'st2',
    'subtype_3': 'st3',
    'channel_type': 'tu',
    'ip_address': 'ip',
    'page_address': 'u',
    'birth_year': 'b',
    'gender': 'g',
    'city': 'ly',
    'country': 'lc',
    'state': 'ls',
    'postal': 'lp',
    'friend_count': 'f',
    'goal_count_id': 'gcn',
    'value': 'v',
}

CHANNEL_TYPES = (
    'feedpub',
    'stream',
    'feedstory',
    'multifeedstory',
)

class KontagentError(Exception):
    pass

class Kontagent(object):
    def __init__(self, api_key, secret_key, test=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.test = test
    
    def invite_sent(self, sender_uid, recipient_uids, template_id=None,
                    tracking_tag=None, subtype_1=None, subtype_2=None):
        return self._request('ins', locals())
    
    def invite_click_response(self, installed, tracking_tag, recipient_uid=None,
                              template_id=None, subtype_1=None, subtype_2=None):
        data = locals()
        data.update({'tu': 'inr'})
        return self._request('inr', data)
    
    def notification_sent(self, sender_uid, recipient_uids, tracking_tag,
                          template_id=None, subtype_1=None, subtype_2=None):
        return self._request('nts', locals())
    
    def notification_click_response(self, installed, tracking_tag,
                                    recipient_uid=None, template_id=None,
                                    subtype_1=None, subtype_2=None):
        data = locals()
        data.update({'tu': 'ntr'})
        return self._request('ntr', data)
    
    def notification_email_sent(self, sender_uid, recipient_uids, tracking_tag,
                                template_id=None, subtype_1=None,
                                subtype_2=None):
        return self._request('nes', locals())
    
    def notification_email_response(self, installed, tracking_tag,
                                    recipient_uid=None, subtype_1=None,
                                    subtype_2=None):
        data = locals()
        data.update({'tu': 'nei'})
        return self._request('nei', data)
    
    def post(self, sender_uid, channel_type, tracking_tag, subtype_1=None,
             subtype_2=None, subtype_3=None):
        if channel_type not in CHANNEL_TYPES:
            raise KontagentError('Invalid channel type entered (%s)' % (
                channel_type,))
        return self._request('pst', locals())
    
    def post_response(self, recipient_uid, channel_type, installed,
                      subtype_1=None, subtype_2=None, subtype_3=None,
                      tracking_tag=None):
        if channel_type not in CHANNEL_TYPES:
            raise KontagentError('Invalid channel type entered (%s)' % (
                channel_type,))
        return self._request('psr', locals())
    
    def application_added(self, sender_uid, tracking_tag=None,
                          short_tracking_tag=None):
        return self._request('apa', locals())
    
    def application_removed(self, uid):
        return self._request('psr', {'s': uid})
    
    def undirected_communication_click(self, sender_uid, channel_type,
                                       installed, subtype_1=None,
                                       subtype_2=None, short_tracking_tag=None):
        return self._request('ucc', locals())
    
    def page_request(self, sender_uid, ip_address=None, page_address=None):
        return self._request('pgr', locals())
    
    def user_information(self, sender_uid, birth_year=None, gender=None,
                         city=None, country=None, state=None, postal=None,
                         friend_count=None):
        return self._request('cpu', locals())
    
    def goal_counts(self, sender_uid, **kwargs):
        data = kwargs
        data.update({'sender_uid': sender_uid})
        return self._request('gci', data)
    
    def revenue_tracking(self, sender_uid, value):
        return self._request('mtu', locals())
    
    def _request(self, msg_type, data):
        path = self._get_path(msg_type)
        qs = self._get_qs(data)
        if self.test:
            domain = 'api.test.kontagent.net'
        else:
            domain = 'api.geo.kontagent.net'
        try:
            conn = httplib.HTTPConnection(domain)
            conn.request('GET', path + '?' + qs)
            response = conn.getresponse().read()
        except (socket.error, httplib.HTTPException, ValueError):
            raise KontagentError('Error in sending request')
        return response
    
    def _get_qs(self, raw_data):
        data = {}
        # First, we need to substitute the keys with the correct values, and
        # remove any references to 'self' that may be left over.
        # We also munge the values into proper strings in the expected format
        # in this function as well.
        for key, val in raw_data.iteritems():
            if key == 'self' or not val:
                continue
            if isinstance(val, list):
                val = ','.join(map(str, val))
            elif val is True:
                val = '1'
            elif val is False:
                val = '0'
            else:
                val = str(val)
            data[VAR_MAP.get(key, key)] = val
        # Now we add a timestamp
        data['ts'] = str(time.time() * 1e6)
        # FInally we build up a signature and sign it
        sig = []
        for key in sorted(data.keys()):
            sig.extend((key, '=', data.get(key)))
        sig.append(self.secret_key)
        data['an_sig'] = hashlib.md5(''.join(sig)).hexdigest()
        # URL-Encode the parameters and return the value
        return urllib.urlencode(data)
    
    def _get_path(self, msg_type):
        return '/api/v1/%s/%s/' % (self.api_key, msg_type)