import json, webapp2
from google.appengine.api import memcache, urlfetch

"""
  In order to support a new platform, two things need to be amended:
  PLATFORMS in api.py, and
  URLS in ratefetch.py
"""

PLATFORMS = {
"coinbase": {"currency": "usd", "path": ["btc_to_usd"]},
"bitstamp": {"currency": "usd", "path": ["last"]},
"bitfinex": {"currency": "usd", "path": ["last_price"]},
"cavirtex": {"currency": "cad", "path": ["ticker", "BTCCAD", "last"]},
"vaultofsatoshi": {"currency": "cad", "path": ["data", 0, "price", "value"]},
"btc-e": {"currency": "usd", "path": ["ticker", "last"]}}

class API(webapp2.RequestHandler):


  def __init__(self, request=None, response=None):
    """
    This is nearly the same as the original webapp2 RequestHandler __init__()
    with the only difference being that if the request contains a callback
    parameter, the response is wrapped in it before being written
    """
    self.initialize(request, response)
    write = self.response.write
    self.response.write = lambda msg: write(self.jsonpad(msg))

  def platformratebtcusd(self):
    platform = self.platform
    path = PLATFORMS[platform].get('path')
    platformcurrency = PLATFORMS[platform].get('currency')
    rate = memcache.get(platform) or {}
    for segment in path:
      if type(segment) == str:
        rate = rate.get(segment) or {}
      elif type(segment) in {int, float} and len(rate) > segment:
        rate = rate[segment]
      else:
        rate = None
    rate = float(rate)
    if platformcurrency != 'usd' and rate:
      rate *= float(self.coinbase.get(platformcurrency + '_to_usd'))
    return rate

  def rate_and_timestamp(self):
    coinbase = self.coinbase
    curpair = self.curpair
    base = self.base
    quote = self.quote
    if self.platform == 'coinbase':
      if 'usd' in curpair or 'btc' in curpair:
        rate = float(coinbase.get(curpair))
      else:
        rate = (float(coinbase.get(base + '_to_usd')) *
          float(coinbase.get('usd_to_'+ quote)))
      return {curpair: rate, "timestamp": coinbase.get("timestamp")}
    platformfetch = memcache.get(self.platform) or {}
    timestamp = platformfetch.get('timestamp')
    btcusd = self.platformratebtcusd()
    if curpair == 'btc_to_usd':
      return {curpair: btcusd, "timestamp": timestamp}
    if curpair == 'usd_to_btc':
      return {curpair: 1/btcusd, "timestamp": timestamp}
    #get fiat_to_fiat currency conversion from coinbase
    if base == 'btc':
      fiatexchange = float(coinbase.get('usd_to_' + quote))
    else: fiatexchange = float(coinbase.get('usd_to_' + base))
    if base == 'btc':
      return {curpair: btcusd*fiatexchange, "timestamp": timestamp}
    return {curpair: 1/(btcusd*fiatexchange), "timestamp": timestamp}

  def smartpath(self):
    #break up path into platform, base, and quote
    #if only one path segment, expand to two by assuming base=btc, quote=usd
    splitpath = [x for x in self.request.path.lower().split('/') if x]
    if len(splitpath) == 2:
      if splitpath[1] == 'btc':
        splitpath.append('usd')
      else:
        splitpath.append(splitpath[1])
        splitpath[1] = 'btc'
    if len(splitpath) != 3:
      splitpath = [splitpath[0], None, None]
    return splitpath

  def jsonpad(self, response):
    if type(response) == dict:
      if self.base and self.quote:
        response = {k: float(v) for k, v in response.items()}
      response = json.dumps(response)
    if self.request.get('callback'):
      return (self.request.get('callback') + '(' + response + ');')
    return response

  def get(self):
    self.response.headers["Content-Type"] = "application/json"
    smartpath = self.smartpath()
    platform = self.platform = smartpath[0]
    # get currency pair as base and quote ('quote' is preferred to 'counter')
    # see http://en.wikipedia.org/wiki/Currency_pair
    base = self.base = smartpath[1]
    quote = self.quote = smartpath[2]
    if platform not in PLATFORMS or len(smartpath) != 3:
      self.abort(404)
    if not(smartpath[1] and smartpath[2]): self.response.write(memcache.get(platform)); return
    # create set of supported ISO 4217 currency codes
    # see README for more information
    fiatkeys = {str(y[0:3]) for y in memcache.get('coinbase')
      if y[0:3] not in ['tim', 'btc']}
    if (base == quote or
    base not in fiatkeys.union({'btc'}) or
    quote not in fiatkeys.union({'btc'}) or
    (base in fiatkeys and quote in fiatkeys and platform != 'coinbase')):
      self.abort(400)
    self.curpair = base + '_to_' + quote
    self.coinbase = memcache.get('coinbase') or {}
    self.platformfetch = memcache.get(platform) or {}
    self.response.write(self.rate_and_timestamp())

app = webapp2.WSGIApplication([('/.*', API)], debug=True)