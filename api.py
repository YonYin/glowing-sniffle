import requests
import json
from auth_key import token
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)#filename='network.log',
#================================================================API Essentials================================================================
def api_request(request, payload, auth, method='get'):
    #Param :request: str of the endpoint to which to connect
    #Param :auth: bool whether token is required in the call parameters
    base_url = 'https://api.mybitx.com/api/1/'
    url = base_url + request

    if method == 'get':
        if auth:
            r = requests.get(url, params=payload, auth=token())
        elif not auth:
            r = requests.get(url, params=payload)
    elif method=='post':
        if auth:
            r = requests.post(url, data=payload, auth=token())
        elif not auth:
            r = requests.post(url, data=payload)
    elif method=='delete':
        if auth:
            r = requests.delete(url, data=payload, auth=token())
        elif not auth:
            r = requests.delete(url, data=payload)
    elif method=='put':
        if auth:
            r = requests.put(url, data=payload, auth=token())
        elif not auth:
            r = requests.put(url, data=payload)
    return r.json()

#================================================================MARKET DATA================================================================
#TESTED
#there has been an intitial test and this seems to be correct!
def getTicker(pair='XBTZAR'):
    #param :pair: str, currency pair ticker to request
    payload = {'pair' : pair}
    request = 'ticker'
    return api_request(request, payload, False)


def getAllTickers():
    payload = None
    request = 'tickers'
    return api_request(request, payload, False)

def getOrderBook(pair='XBTZAR'):
    #Param :pair: str of the currency pair (XBTZAR / ETHXBT)
    #Returns a list of bids and asks in the order book. Ask orders are sorted by price ascending.
    #  Bid orders are sorted by price descending. Note that multiple orders at the same price are not necessarily conflated.
    payload = {'pair': pair}
    request = 'orderbook'
    return api_request(request, payload, False)

def trades(pair='XBTZAR'):
    payload = {'pair' : pair}
    request = 'trades'
    return api_request(request, payload, False)

#================================================================Accounts================================================================

def createAccount(currency, name):
    payload = {'currency':currency, 'name':name}
    request = 'accounts'
    return api_request(request, payload, True, 'post')

def getAccounts():
    #Return the list of all accounts and their respective balances.
    payload = None
    request = 'balance'
    return api_request(request, payload, True)

def getTransactions(id, min_row, max_row):
    #maximum 1000 rows can be requested per call
    payload = {'min_row': min_row, 'max_row':max_row}
    request = '%s/transactions' % (id)
    return api_request(request, payload, True)

def getPendingTransactions(id):
    #Param :id: str, account number for which to call pending transactions
    payload = None
    request = "accounts/%s/pending" % (id)
    return api_request(request, payload, True)


#================================================================Orders================================================================

def listOrders(state='PENDING', pair='XBTZAR'):
    #list is truncated after 100 items
    payload = {'state':state, 'pair':pair}
    request = 'listorders'
    return api_request(request, payload, True)

def postLimitOrder(type, volume, price, base_account_id, counter_account_id, pair='XBTZAR'):
    #Param :pair: string, the currency pair to trade (should not need a change from default XBTZAR)
    #Param :type: string, 'BID' or 'ASK' limit order
    #Param :volume: string, amount of Bitcoin to buy or sell as a decimal string in units of bitcoin
    #Param :price: string, Limit price as a decimal string o units of ZAR/BTC
    #Param :base_account_id: string - optional, the base currency amount to use in the trade. STILL NEED TO ADD THE DEFAULT FUNCTIONALITY!
    #Param :counter_account_id: string - optional, the counter currency account to use in the trade. STILL NEED TO ADD THE DEFAULT FUNCTIONALITY!
    payload = {
    'pair' : pair,
    'type' : type,
    'volume' : volume,
    'price' : price,
    'base_account_id' : base_account_id,
    'counter_account_id' : counter_account_id
    }
    request = 'postorder'
    print(payload)
    return api_request(request, payload, True)

def postMarketOrder(type, counter_volume, base_volume, base_account_id, counter_account_id, pair='XBTZAR'):
    payload = {
    'pair' : pair,
    'type' : type,
    'counter_volume' : counter_volume,
    'base_volume' : base_volume,
    'base_account_id' : base_account_id,
    'counter_account_id' : counter_account_id
    }
    request = 'marketorder'
    return api_request(request, payload, True, 'post')

def stopPendingOrder(order_id):
    payload = {'order_id':order_id}
    request = 'stoporder'
    return api_request(request, payload, True, 'post')

def GetOrder(order_id):
    payload = {'order_id':order_id}
    request = 'orders'
    return api_request(request, payload, True)

def listTrades(since, limit, pair='XBTZAR'):
    #this endpoint might lag behind the latest data
    payload = {'since':since, 'limit':limit, 'pair':pair}
    request = 'listtrades'
    return api_request(request, payload, True)

def feeInformation(pair='XBTZAR'):
    payload = {'pair':pair}
    reqeust = 'fee_info'
    return api_request(request, payload, True)

#================================================================RECEIVE ADDRESSES================================================================

def receiveAddress(asset, address):
    #address is optional string parameter should return default if None is requested
    payload = {'asset':asset, 'address':address}
    request = 'funding_address'
    return api_request(request, payload, True)

def createReceiveAddress(asset='XBT'):
    payload = {'asset':asset}
    request = 'funding_address'
    return api_request(request, payload, True)

#================================================================WITHDRAWAL REQUESTS================================================================

def listWithdrawalRequests():
    payload = None
    request = 'withdrawals'
    return api_request(request, payload, True)

def requestWithdrawal(type, amount, beneficiary_id):
    #beneficiary_id is only required if there are more than one beneficiary listed on the account
    payload = {'type':type, 'amount':amount, 'beneficiary_id':beneficiary_id}
    request = 'withdrawals'
    return api_request(request, payload, True, 'post')

def getWithdrawalStatus(id):
    payload = None
    request = 'withdrawals/%s' % (id)
    return api_request(request, payload, True)

def cancelWithdrawal(id):
    #this can only be done if the status of the withdrawal is PENDING
    payload = None
    request = 'withdrawals/%s' % (id)
    return api_request(request, payload, True, 'delete')
#================================================================SEND================================================================

def send(amount, currency, address, description, message):
    payload = {'amount':amount, 'currency':currency, 'address':address, 'description':description, 'message':message}
    request = 'send'
    return api_request(request, payload, True, 'post')

#================================================================QUOTES================================================================

def createQuote(type, base_amount, pair):
    payload = {'type':type, 'base_amount':base_amount, 'pair':pair}
    request = 'quotes'
    return api_request(request, payload, True, 'post')

def getQuote(id):
    payload = None
    request = 'quotes/%s' % (id)
    return api_request(request, payload, True)

def exerciseQuote(id):
    payload = None
    request = 'quotes/%s' % (id)
    return api_request(request, payload, True, 'put')

def discardQuote(id):
    payload = None
    request = 'quotes/%s' % (id)
    return api_request(request, payload, True, 'delete')
