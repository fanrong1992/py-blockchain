#!/usr/bin/python
#coding:utf-8

import hashlib

class StringUtils:
    @staticmethod
    def sha256(msg):
        sh = hashlib.sha256()
        sh.update(msg)
        return sh.hexdigest()

    @staticmethod
    def applyECDSASig(prikey, inputs):
        return prikey.sign(inputs)

    @staticmethod
    def verifyECDSASig(pubkey, data, signature):
        return pubkey.verify(signature, data)

    @staticmethod
    def getMerkleRoot(transactions):
        count = len(transactions)
        previousTreeLayer = []
        for transaction in transactions:
            previousTreeLayer.append(transaction.transactionId)
        treeLayer = previousTreeLayer
        while count > 1:
            treeLayer = []
            for i in range(1, len(previous)):
                treeLayer.append(sha256(previousTreeLayer[i-1]+previousTreeLayer[i]))
            count = len(treeLayer)
            previousTreeLayer = treeLayer
        merkleRoot = treeLayer[0] if len(treeLayer) == 1 else ""
        return merkleRoot
