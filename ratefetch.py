import json, webapp2, time
from google.appengine.api import memcache, urlfetch

URLS = {
  "coinbase": "https://coinbase.com/api/v1/currencies/exchange_rates",
  "bitstamp": "https://www.bitstamp.net/api/ticker/",
  "bitfinex": "https://api.bitfinex.com/v1/ticker/BTCUSD",
  "cavirtex": "https://cavirtex.com/api2/ticker.json",
  "vaultofsatoshi": "http://api.vaultofsatoshi.com/public/recent_transactions?order_currency=btc&payment_currency=cad",
  "btc-e": "https://btc-e.com/api/2/btc_usd/ticker"}

class CronPage(webapp2.RequestHandler):
 def get(self):

  fetches = {k:urlfetch.fetch(v) for k,v in URLS.items()}
  responses = {}
  for platform in fetches:
    if (fetches[platform].status_code == 200):
      #the following bit of trickery combines the dict representation of the
      #platform response with an additional key/value for datetime
      responses[platform] = dict({"timestamp": time.time()},
        **json.loads(fetches[platform].content))
  memcache.set_multi(responses)

app = webapp2.WSGIApplication([('/fetchrates', CronPage)], debug=True)


