#!/usr/bin/python
#coding:utf-8

import time
from strutils import StringUtils

class Block:
    def __init__(self, previousHash):
        self.previousHash = previousHash
        self.timeStamp = time.time()
        self.transactions = []
        self.nonce = 0
        self.merkleRoot = ""
        self.hash = self.calculateHash()

    def calculateHash(self):
        return StringUtils.sha256(self.previousHash+str(self.timeStamp)+str(self.nonce)+self.merkleRoot)

    def mineBlock(self, difficulty):
        self.merkleRoot = StringUtils.getMerkleRoot(self.transactions)
        target = '0'*difficulty
        while self.hash[0:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculateHash()
        print "Block Mined!!! : " + self.hash

    def addTransaction(self, transaction):
        if transaction == None:
            return False
        if self.previousHash != "0":
            if transaction.processTransaction() != True:
                print "Transaction failed to process. Discarded."
                return False
        self.transactions.append(transaction)
        print "Transaction Successfully added to Block"
        return True

