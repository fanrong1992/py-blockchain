#!/usr/bin/python
#coding:utf-8

import config
import random
from ecdsa.util import PRNG
from ecdsa import SigningKey
from transaction import Transaction, TransactionInput

class Wallet:
    def __init__(self):
        rng = PRNG(str(random.random()))
        self.privateKey = SigningKey.generate(entropy=rng)
        self.publicKey = self.privateKey.get_verifying_key()
        self.UTXOs = {}

    def getBalance(self):
        total = 0
        for item in config.UTXOs.items():
            UTXO = item[1]
            if UTXO.isMine(self.publicKey):
                self.UTXOs[UTXO.id] = UTXO
                total += UTXO.value
        return total

    def sendFunds(self, _recipient, value):
        if self.getBalance() < value:
            print "#Not Enough funds to send transaction. Transaction Discarded."
            return None
        inputs = []
        total = 0
        # 需要用到的output
        for item in self.UTXOs.items():
            UTXO = item[1]
            total += UTXO.value
            inputs.append(TransactionInput(UTXO.id))
            if total > value:
                break
        newTransaction = Transaction(self.publicKey, _recipient, value, inputs)
        newTransaction.generateSignature(self.privateKey)

        for i in inputs:
            del self.UTXOs[i.transactionOutputId]

        return newTransaction

