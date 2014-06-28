#Bitcoin, with padding
**JSONP-enabled bitcoin conversion**



*app is live at [http://bitcoin-p.appspot.com](http://bitcoin-p.appspot.com) and (nearly) ready for production use*

Allows client-side bitcoin pricing. For example if someone wants to simulate a storefront on their ~~geocities~~ neocities page, they can define a function to handle the price of bitcoin from their preferred exchange and in their preferred currency and invoke that function by passing it as a query parameter to the bitcoinp api with the proper request.

For example, if someone has a neocities/github/google page where they advertise a product they sell, along with the price in yen (jpy), they can also include the price in bitcoin using their preferred platform, bitstamp, as follows:


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

*see [example on codepen](http://codepen.io/anon/pen/HkfuA)*

Bitcoinp converts last traded price of bitcoin at multiple platforms to multiple currencies using fiat\_to\_fiat exchange rate information from Coinbase's API.

object response will be a JSON object of form:

`myfunction({"${currency}_to_$(currency)": ${exchange_rate}, "timestamp": ${timestamp}})`

When requested, the resulting object will be wrapped in callback specified as query parameter `?callback=myfunction`





Examples:
---
request:  
`GET /coinbase/btc/usd?callback=myfunction`  
response:  
`myfunction{"btc_to_usd": "598.0746", "timestamp": 1403938400.415413}`

request:  
`GET /coinbase/cad/usd`  
response:  
`{"timestamp": 1403942407.8936901, "cad_to_usd": "0.915344"}`

*//only coinbase can be used as the platform for converting between fiat:*  
request:  
`GET /btc-e/cad/usd`  
response:  
`error code: 400`  

*//returns the unprocessed response for the platform's api call if only the platform is provided*  
request:  
`GET /bitstamp`  
response:   
`{"volume": "6968.11004501", "last": "594.85", "timestamp": "1403942936", "bid": "594.24", "vwap": "588.39", "high": "600.00", "low": "575.00", "ask": "594.85"}`

##Currently supported platforms:
* "coinbase"
* "btc-e"
* "bitstamp"
* "bitfinex"
* "cavirtex"
* "vaultofsatoshi

##Supported currency abbreviations:  
* pkr
* cdf
* ron
* lsl
* mnt
* all
* ugx
* yer
* scr
* zmk
* aud
* cup
* ngn
* byr
* gmd
* vef
* gtq
* hrk
* djf
* mwk
* clp
* eur
* mga
* lrd
* rwf
* nok
* bif
* mop
* amd
* mxn
* tjs
* gel
* shp
* zwl
* kpw
* try
* crc
* aed
* gbp
* bam
* htg
* ars
* mdl
* btc
* btn
* sek
* kmf
* mur
* etb
* irr
* cny
* xof
* bdt
* pen
* ttd
* tmm
* wst
* bwp
* eek
* kzt
* rub
* omr
* mkd
* jod
* sbd
* iqd
* pln
* kes
* hkd
* cop
* mvr
* dzd
* srd
* idr
* krw
* bgn
* vuv
* ils
* bob
* dkk
* ltl
* twd
* kwd
* pgk
* bsd
* sos
* brl
* zar
* sgd
* uzs
* usd
* chf
* gip
* top
* bbd
* xpf
* pyg
* xaf
* huf
* gyd
* bmd
* rsd
* sdg
* kyd
* jmd
* std
* jpy
* azn
* czk
* lkr
* sll
* tnd
* gnf
* nzd
* lvl
* ern
* cve
* cad
* lbp
* tzs
* ang
* xcd
* khr
* myr
* bhd
* inr
* hnl
* lyd
* uah
* sar
* szl
* isk
* afn
* nad
* qar
* bnd
* mmk
* tim
* pab
* bzd
* fkp
* vnd
* uyu
* nio
* aoa
* lak
* kgs
* syp
* mad
* awg
* mzn
* php
* npr
* ghs
* egp
* svc
* fjd
* mro
* dop
* thb
