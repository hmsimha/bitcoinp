app live at [http://bitcoin-p.appspot.com](http://bitcoin-p.appspot.com) and (nearly) ready for production use

#Bitcoin with padding
**JSONP-enabled bitcoin conversion**

A jsonp enabled api aimed at making bitcoin data from around the internet more accessible and consumable by aggregating api data from the most popular bitcoin exchanges (and platforms that 'provide bitcoin exchange services' such as coinbase) and delivering it to anyone who wants to utilize it on their static page, application, or widget without having to build a backend to do the same thing.

For example if someone wants to simulate a storefront on their ~~geocities~~ neocities page, they can define a function to handle the price of bitcoin from their preferred exchange and in their preferred currency and invoke that function by passing it as a query parameter to the bitcoinp api with the proper request.

One possible use would be if someone has a neocities/github/google page where they advertise a product they sell that they want displayed in btc alongside the fiat price:

    My Wasabi flavored pop tarts cost ¥<span id="yen">800</span> yen (or <span id="btc"></span> BTC) each.
    
    <script type="text/javascript">
    function convert(response)
    {
      var yen = document.getElementById("yen").textContent;
      var rate = response["jpy_to_btc"];
      document.getElementById("btc").textContent = (rate*yen).toFixed(3);
    }
    </script>
    <script src="http://bitcoin-p.appspot.com/bitstamp/jpy/btc?callback=convert" type="text/javascript"></script>

result:

`My Wasabi flavored pop tarts cost ¥800 yen (or 0.013 BTC) each.`

*[see it on codepen](http://codepen.io/anon/pen/HkfuA)*

Other uses would be building a full-fledged currency conversion calculator like preev.com, but with more sources, or providing a view on bitcoin prices from within a smartphone application.

Bitcoinp provides an api for providing a quote to or from btc from any supported fiat currency (see ISO 4217 codes at bottom) from any supported exchange. If the exchange doesn't support a fiat currency directly (such as if someone wants the btc_to_usd rate from cavirtex), it uses fiat_to_fiat exchange rates provided by Coinbase's API to perform the conversion behind the scenes. If the request includes a 'callback' query parameter, the resulting response will include the JSON formatted object wrapped in the callback.

All requests will take the form:  
'/:platform/:base\_currency\_code/:quote\_currency\_code'

where :platform is one of the following supported platforms:

* "coinbase"
* "btc-e"
* "bitstamp"
* "bitfinex"
* "cavirtex"
* "vaultofsatoshi

and :base\_currency\_code and :quote\_currency\_code are either 'btc' or one of the fiat currencies supported by Coinbase (see bottom for full list and details)

Note: The two currency codes must not be the same. Also, if a platform other than coinbase is specified, one of the currencies must be 'btc'

bitcoinp will also handle a request of the form '/:platform/:currency' by converting it to /:platform/btc/:currency if :currency is a supported fiat code, or /:platform/btc/usd if :currency is 'btc'

Additionally, the request may take the form '/:platform' if the application developer wants their application to receive the entire API response as received by bitcoinp's API aggregation cron job

Responses will have the following format:

`mycallback({"${currency}_to_$(currency)": ${exchange_rate}, "timestamp": ${timestamp}});`

Examples:
---

request:  
`GET /coinbase/btc/usd?callback=myfunction`  
response:  
`myfunction{"btc_to_usd": 598.0746, "timestamp": 1403938400.415413}`

request:  
`GET /coinbase/cad/usd`  
response:  
`{"timestamp": 1403942407.8936901, "cad_to_usd": 0.915344}`

*// only coinbase can be used as the platform for converting between fiat:*  
request:  
`GET /btc-e/cad/usd`  
response:  
`error code: 400`  

*// returns the btc rate against usd even though VoS delivers rate data against cad by default*  
request:  
`GET /vaultofsatoshi/btc` or `GET /vaultofsatoshi/usd`  
response:  
`{"timestamp": 1404077352.836355, "btc_to_usd": 576.66672}`

*// returns the unprocessed response for the platform's api call if only the platform is provided*  
request:  
`GET /bitstamp`  
response:   
`{"volume": "6968.11004501", "last": "594.85", "timestamp": "1403942936", "bid": "594.24", "vwap": "588.39", "high": "600.00", "low": "575.00", "ask": "594.85"}`

##Supported currency abbreviations:
Currency abbreviations use ISO 4217 currency codes. See [wikipedia.org/ISO\_currency\_code](http://en.wikipedia.org/wiki/ISO_currency_code) for more details.
['aed', 'afn', 'all', 'amd', 'ang', 'aoa', 'ars', 'aud', 'awg', 'azn', 'bam', 'bbd', 'bdt', 'bgn', 'bhd', 'bif', 'bmd', 'bnd', 'bob', 'brl', 'bsd', 'btn', 'bwp', 'byr', 'bzd', 'cad', 'cdf', 'chf', 'clp', 'cny', 'cop', 'crc', 'cup', 'cve', 'czk', 'djf', 'dkk', 'dop', 'dzd', 'eek', 'egp', 'ern', 'etb', 'eur', 'fjd', 'fkp', 'gbp', 'gel', 'ghs', 'gip', 'gmd', 'gnf', 'gtq', 'gyd', 'hkd', 'hnl', 'hrk', 'htg', 'huf', 'idr', 'ils', 'inr', 'iqd', 'irr', 'isk', 'jmd', 'jod', 'jpy', 'kes', 'kgs', 'khr', 'kmf', 'kpw', 'krw', 'kwd', 'kyd', 'kzt', 'lak', 'lbp', 'lkr', 'lrd', 'lsl', 'ltl', 'lvl', 'lyd', 'mad', 'mdl', 'mga', 'mkd', 'mmk', 'mnt', 'mop', 'mro', 'mur', 'mvr', 'mwk', 'mxn', 'myr', 'mzn', 'nad', 'ngn', 'nio', 'nok', 'npr', 'nzd', 'omr', 'pab', 'pen', 'pgk', 'php', 'pkr', 'pln', 'pyg', 'qar', 'ron', 'rsd', 'rub', 'rwf', 'sar', 'sbd', 'scr', 'sdg', 'sek', 'sgd', 'shp', 'sll', 'sos', 'srd', 'std', 'svc', 'syp', 'szl', 'thb', 'tim', 'tjs', 'tmm', 'tnd', 'top', 'try', 'ttd', 'twd', 'tzs', 'uah', 'ugx', 'usd', 'uyu', 'uzs', 'vef', 'vnd', 'vuv', 'wst', 'xaf', 'xcd', 'xof', 'xpf', 'yer', 'zar', 'zmk', 'zwl']