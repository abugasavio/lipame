# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    wallet = models.ForeignKey('wallet.Wallet')
    opening_balance = models.IntegerField(default=0)
    closing_balance = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(default=timezone.now())


class Wallet(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def credit(self, amount, reference=None):
        amount = int(amount)
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
                                   closing_balance=closing_balance,
                                   description=reference)
        return closing_balance

    def debit(self, amount, reference=None):
        return self.credit(0-amount, reference)

    def get_balance(self):
        return self.get_last_transaction().closing_balance if self.get_last_transaction() else 0

    def get_last_transaction(self):
        last_transaction = None
        transactions = Transaction.objects.filter(wallet=self)
        if transactions.count() > 0:
            last_transaction = transactions.last()
        return last_transaction

    @classmethod
    def user_balance(cls, user):
        user_wallet = Wallet.objects.filter(owner=user)
        if user_wallet.count() > 0:
            return user_wallet[0].get_balance()
        return 0

    @classmethod
    def credit_user(cls, user, amount, reference=None):
        user_wallet, _ = Wallet.objects.get_or_create(owner=user)
        return user_wallet.credit(amount, reference)

    @classmethod
    def debit_user(cls, user, amount, reference=None):
        return Wallet.credit_user(user, 0-amount, reference)
