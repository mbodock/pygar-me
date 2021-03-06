# encoding: utf-8

import json
import requests

from .exceptions import PygarmeTransactionApiError, PygarmeTransactionError, NotPaidException


class Transaction(object):
    BASE_URL = 'https://api.pagar.me/1/'

    def __init__(self, api_key=None, amount=None, card_hash=None,
            payment_method='credit_card', installments=1,
            postback_url=None, metadata={}, soft_descriptor=''):
        self.amount = amount
        self.api_key = api_key
        self.card_hash = card_hash
        self.payment_method = payment_method
        self.installments = installments
        self.postback_url = postback_url
        self.metadata = metadata
        self.soft_descriptor = soft_descriptor[:13]
        self.id = None

    def error(self, response):
        data = json.loads(response)
        e = data['errors'][0]
        error_string = e['type'] + ' - ' + e['message']
        raise PygarmeTransactionApiError(error_string)

    def charge(self):
        post_data = self.get_data()
        url = self.BASE_URL + 'transactions'
        pagarme_response = requests.post(url, data=post_data)
        if pagarme_response.status_code == 200:
            self.handle_response(json.loads(pagarme_response.content))
        else:
            self.error(pagarme_response.content)

    def handle_response(self, data):
        self.id = data['id']
        self.status = data['status']
        self.card = data['card']
        self.postback_url = data['postback_url']
        self.metadata = data['metadata']
        self.response_data = data

    def get_data(self):
        return self.__dict__()

    def __dict__(self):
        d = {
            'api_key': self.api_key,
        }
        if self.amount:
            d['amount'] = self.amount
            d['card_hash'] = self.card_hash
            d['installments'] = self.installments
            d['payment_method'] = self.payment_method
            d['soft_descriptor'] = self.soft_descriptor[:13]

        if self.metadata:
            d['metadata'] = self.metadata

        if self.postback_url:
            d['postback_url'] = self.postback_url
        return d

    def find_by_id(self, id=None):
        if not id or not isinstance(id, int):
            raise ValueError('Transaction id not suplied')
        url = self.BASE_URL + 'transactions/' + str(id)
        pagarme_response = requests.get(url, data=self.get_data())
        if pagarme_response.status_code == 200:
            self.handle_response(json.loads(pagarme_response.content))
        else:
            self.error(pagarme_response.content)

    def refund(self):
        if self.id is None:
            raise NotPaidException('Id not suplied')

        url = self.BASE_URL + 'transactions/' + str(self.id) + '/refund'
        pagarme_response = requests.post(url, data=self.get_data())
        if pagarme_response.status_code == 200:
            self.handle_response(json.loads(pagarme_response.content))
        else:
            self.error(pagarme_response.content)
