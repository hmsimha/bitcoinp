import json, webapp2, time
from google.appengine.api import memcache, urlfetch

#PLATFORMS, API.rate_and_timestamp, and urls in ratefetch.py need to be
#amended in order for a new platform to be supported

PLATFORMS = {
"coinbase": {"currency": "usd", "path": ["btc_to_usd"]},
"bitstamp": {"currency": "usd", "path": ["last"]},
"bitfinex": {"currency": "usd", "path": ["last_price"]},
"cavirtex": {"currency": "cad", "path": ["ticker", "BTCCAD", "last"]},
"vaultofsatoshi": {"currency": "cad", "path": ["data", "price", "value"]},
"btc-e": {"currency": "usd", "path": ["ticker", "last"]}}

class API(webapp2.RequestHandler):


  def __init__(self, request=None, response=None):
    #This is nearly the same as the original webapp2 RequestHandler __init__()
    #with the only difference being that if the request contains a callback
    #parameter, the response is wrapped in it before being written
    self.initialize(request, response)
    write = self.response.write
    self.response.write = lambda msg: write(self.jsonpad(msg))

  def platformratebtcusd(self):
    platform = self.platform
    path = PLATFORMS[platform].get('path')
    platformcurrency = PLATFORMS[platform].get('currency')
    rate = memcache.get(platform) or {}
    for segment in path:
      rate = rate.get(segment) or {}
    rate = float(rate)
    if platformcurrency != 'usd' and rate:
      rate = float(self.coinbase.get(platformcurrency + '_to_usd'))*rate
    return rate

  def rate_and_timestamp(self):
    coinbase = self.coinbase
    if self.platform == 'coinbase':
      return {self.rep: coinbase.get(self.rep), 
        "timestamp": coinbase.get("timestamp")}
    platformfetch = memcache.get(self.platform) or {}
    timestamp = platformfetch.get('timestamp')
    btcusd = self.platformratebtcusd()
    rep = self.rep
    if self.rep == 'btc_to_usd':
      return {self.rep: btcusd, "timestamp": timestamp}
    if self.rep == 'usd_to_btc':
      return {self.rep: 1/btcusd, "timestamp": timestamp}
    #get fiat_to_fiat currency conversion from coinbase
    if rep[0:3] == 'btc':
      fiatexchange = float(coinbase.get('usd_to_' + rep[7:10]))
    else: fiatexchange = float(coinbase.get('usd_to_' + rep[0:3]))
    if self.rep[0:3] == 'btc':
      return {self.rep: btcusd*fiatexchange, "timestamp": timestamp}
    return {self.rep: 1/(btcusd*fiatexchange), "timestamp": timestamp}

  def smartpath(self):
    #break up path into platform, from currency, and to currency
    #if only one path segment, expand to two by assuming from=btc, to=usd
    splitpath = [x for x in self.request.path.lower().split('/') if x]
    if len(splitpath) == 2:
      if splitpath[1] == 'btc':
        splitpath.append('usd')
      else:
        splitpath.append(splitpath[1])
        splitpath[1] = 'btc'
    return splitpath

  def jsonpad(self, response):
    if type(response) == dict: response = json.dumps(response)
    if self.request.get('callback'):
      return (self.request.get('callback') + '(' + response + ');')
    return response

  def get(self):
    self.response.headers["Content-Type"] = "application/json"
    path = self.smartpath()
    platform = path[0]
    if platform not in PLATFORMS or not(1 <= len(path) <= 3):
      self.abort(404)
    if len(path) == 1: self.response.write(memcache.get(platform)); return
    #create set of fiat currency abbreviations:
    fiatkeys = {str(y[0:3]) for y in memcache.get('coinbase')
      if y[0:3] not in ['tim', 'btc']}
    if (path[1] == path[2] or
      path[1] not in fiatkeys.union({'btc'}) or
      path[2] not in fiatkeys.union({'btc'}) or
      (path[1] in fiatkeys and path[2] in fiatkeys and platform != 'coinbase')
      ): self.abort(400)
    self.rep = path[1] + '_to_' + path[2]
    self.coinbase = memcache.get('coinbase') or {}
    self.platform = platform
    self.platformfetch = memcache.get(platform) or {}
    self.response.write(self.rate_and_timestamp())

app = webapp2.WSGIApplication([('/.*', API)], debug=True)