# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    wallet = models.ForeignKey('wallet.Wallet')
    opening_balance = models.IntegerField()
    closing_balance = models.IntegerField()


class Wallet(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def credit(self, amount):
        last_transaction = self.get_last_transaction()

        if last_transaction:
            opening_balance = last_transaction.closing_balance
            closing_balance = opening_balance + amount
        else:
            opening_balance = 0
            closing_balance = amount
        Transaction.objects.create(wallet=self,
                                   amount=amount,
                                   opening_balance=opening_balance,
                                   closing_balance=closing_balance)

    def debit(self, amount):
        self.debit(0-amount)

    def get_balance(self):
        return self.get_last_transaction().closing_balance if self.get_last_transaction() else 0

    def get_last_transaction(self):
        last_transaction = None
        transactions = Transaction.objects.filter(wallet=self).order_by('-created')
        if transactions.count() > 0:
            last_transaction = transactions.last()
        return last_transaction

    @classmethod
    def user_balance(cls, user):
        user_wallet = Wallet.objects.filter(owner=user)
        if user_wallet.count() > 0:
            return user.get_balance()
        return 0

    @classmethod
    def credit_user(cls, user, amount):
        user_wallet = Wallet.objects.get_or_create(owner=user)
        user_wallet.credit(amount)

    @classmethod
    def debit_user(cls, user, amount):
        Wallet.credit_user(user, 0-amount)
