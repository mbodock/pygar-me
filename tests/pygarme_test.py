# encoding: utf-8

import mock
import unittest

from pygar_me import Pygarme, PygarmeApiError
from pygar_me.transaction import Transaction

from .mocks import fake_request, fake_request_fail, fake_request_list


class PygarmeTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = 'keydeteste'

    def test_can_instantiate(self):
        pagarme = Pygarme(self.api_key)
        self.assertIsInstance(pagarme, Pygarme)

    def test_invalid_api(self):
        with self.assertRaises(ValueError):
            pagarme = Pygarme('')

    def test_start_transaction(self):
        pagarme = Pygarme(self.api_key)
        transaction = pagarme.start_transaction(amount=314, card_hash='hashcard')
        self.assertIsInstance(transaction, Transaction)

    def test_start_transaction_invalid_amount(self):
        pagarme = Pygarme(self.api_key)
        with self.assertRaises(ValueError):
            transaction = pagarme.start_transaction(amount=None, card_hash='hashcard')

    def test_start_transaction_invalid_card_hash(self):
        pagarme = Pygarme(self.api_key)
        with self.assertRaises(ValueError):
            transaction = pagarme.start_transaction(amount=314, card_hash='')

    def test_start_transaction_invalid_payment_method(self):
        pagarme = Pygarme(self.api_key)
        with self.assertRaises(ValueError):
            transaction = pagarme.start_transaction(amount=314, card_hash='hashcard', payment_method='rice_bag')

    def test_start_transaction_invalid_installments(self):
        pagarme = Pygarme(self.api_key)
        with self.assertRaises(ValueError):
            transaction = pagarme.start_transaction(amount=314, card_hash='hashcard', installments=0)

    @mock.patch('requests.get', mock.Mock(side_effect=fake_request))
    def test_find_transaction_by_id(self):
        pagarme = Pygarme(self.api_key)
        transaction = pagarme.find_transaction_by_id(314)
        self.assertIsInstance(transaction, Transaction)

    @mock.patch('requests.get', mock.Mock(side_effect=fake_request_list))
    def test_get_all_transaction(self):
        pagarme = Pygarme(self.api_key)
        transactions = pagarme.all_transactions(page=2,count=3)
        self.assertTrue(len(transactions) == 1)

    @mock.patch('requests.get', mock.Mock(side_effect=fake_request_fail))
    def test_get_all_transaction_fails(self):
        pagarme = Pygarme(self.api_key)
        with self.assertRaises(PygarmeApiError):
            transactions = pagarme.all_transactions(page=2,count=3)
