#!/usr/bin/python
#coding:utf-8
import config
from strutils import StringUtils

class Transaction:
    def __init__(self, pubkey_from, pubkey_to, value, inputs):
        self.transactionId = ""
        self.sender = pubkey_from
        self.reciepient = pubkey_to
        self.value = value
        self.inputs = inputs
        self.outputs = []
        self.sequence = 0

    def generateSignature(self, prikey):
        data = self.sender.to_string() + self.reciepient.to_string() + str(self.value)
        self.signature = StringUtils.applyECDSASig(prikey, data)

    def verifySignature(self):
        data = self.sender.to_string() + self.reciepient.to_string() + str(self.value)
        return StringUtils.verifyECDSASig(self.sender, data, self.signature)

    def processTransaction(self):
        if self.verifySignature() == False:
            print "#Transaction Signature failed to verify"
            return False
        # 收集交易input（确保他们是未花费的）
        #print self.inputs
        for i in self.inputs:
            i.UTXO = config.UTXOs[i.transactionOutputId]
        #print "self.getInputsValue():"
        #print self.getInputsValue()
        if self.getInputsValue() < config.minimumTransaction:
            print "#Transaction Inputs too small: " + self.getInputsValue()
            return False
        # 产生交易输出
        leftOver = self.getInputsValue() - self.value
        self.transactionId = self.calculateHash()
        # 发送value给reciptient
        self.outputs.append(TransactionOutput(self.reciepient, self.value, self.transactionId))
        # 发送找零给sender
        self.outputs.append(TransactionOutput(self.sender, leftOver, self.transactionId))
        for o in self.outputs:
            config.UTXOs[o.id] = o
        # 从UTXO删除交易inputs当做花费
        for i in self.inputs:
            if i.UTXO == None:
                continue
            del config.UTXOs[i.UTXO.id]
        return True

    # 返回输入值的和
    def getInputsValue(self):
        total = 0
        for i in self.inputs:
            if i.UTXO == None:
                continue
            total += i.UTXO.value
        return total
    # 返回输出值的和
    def getOutputsValue(self):
        total = 0
        for o in self.outputs:
            total += o.value
        return total

    def calculateHash(self):
        self.sequence += 1
        return StringUtils.sha256(self.sender.to_string() + self.reciepient.to_string() + str(self.value) + str(self.sequence))

class TransactionInput:
    def __init__(self, transactionOutputId):
        self.transactionOutputId = transactionOutputId
        self.UTXO = None # 包含未使用的交易output

class TransactionOutput:
    def __init__(self, pubkey_to, value, parentTransactionId):
        self.reciepient = pubkey_to
        self.value = value
        self.parentTransactionId = parentTransactionId
        self.id = StringUtils.sha256(pubkey_to.to_string()+str(value)+parentTransactionId)

    def isMine(self, publicKey):
        return publicKey == self.reciepient
