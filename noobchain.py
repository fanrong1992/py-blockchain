#coding:utf-8

import config
from block import Block
from wallet import Wallet
from transaction import Transaction, TransactionOutput, TransactionInput

def isChainValid():
    hashTarget = '0' * config.difficulty
    tempUTXOs = {}
    tempUTXOs[genesisTransaction.outputs[0].id] = genesisTransaction.outputs[0]
    for i in range(1, len(config.blockchain)):
        curblock = config.blockchain[i]
        preblock = config.blockchain[i-1]
        if curblock.hash != curblock.calculateHash():
            print 'Current Hashes not equal'
            return False
        if preblock.hash != curblock.previousHash:
            print 'Previous Hashes not equal'
            return False
        if curblock.hash[:config.difficulty] != hashTarget:
            print '#This block hasnt been mined'
            return False
        for t in range(len(curblock.transactions)):
            curTransaction = curblock.transactions[t]
            if not curTransaction.verifySignature():
                print '#Signature on Transaction %d is Invalid' % t
                return False
            if curTransaction.getInputsValue() != curTransaction.getOutputsValue():
                print '#Inputs are not equal to outputs on Transaction %d' % t
                return False
            for i in curTransaction.inputs:
                tempOutput = tempUTXOs[i.transactionOutputId]
                if tempOutput == None:
                    print '#Referenced input on Transaction %d is Missing' % t
                    return False
                if i.UTXO.value != tempOutput.value:
                    print '#Referenced input Transaction %d value is Invalid' % t
                    return False
                del tempUTXOs[i.transactionOutputId]
            for o in curTransaction.outputs:
                tempUTXOs[o.id] = o
            if curTransaction.outputs[0].reciepient != curTransaction.reciepient:
                print '#Transaction %d output reciepient is not who it should be' % t
                return False
            if curTransaction.outputs[1].reciepient != curTransaction.sender:
                print '#Transaction %d output change is not sender' % t
                return False
    print 'Blockchain is valid'
    return True

walletA = Wallet()
walletB = Wallet()
coinbase = Wallet()

# 将coinbase里的100个coin给A
genesisTransaction = Transaction(coinbase.publicKey, walletA.publicKey, 100, None)
genesisTransaction.generateSignature(coinbase.privateKey)
genesisTransaction.transactionId = "0"
genesisTransaction.outputs.append(TransactionOutput(genesisTransaction.reciepient, genesisTransaction.value, genesisTransaction.transactionId))
config.UTXOs[genesisTransaction.outputs[0].id] = genesisTransaction.outputs[0]

print "Creating and Mining Genesis block... "
genesis = Block("0")
genesis.addTransaction(genesisTransaction)
genesis.mineBlock(config.difficulty)
config.blockchain.append(genesis)

# testing
block1 = Block(genesis.hash)
print "walletA's balance is: %f" % walletA.getBalance()
print "walletA is attempting to send funds (40) to walletB..."
block1.addTransaction(walletA.sendFunds(walletB.publicKey, 40))
block1.mineBlock(config.difficulty)
config.blockchain.append(block1)
print "walletA's balance is: %f"  % walletA.getBalance()
print "walletB's balance is: %f"  % walletB.getBalance()

block2 = Block(block1.hash)
print "walletA is attempting to send more funds (1000) than it has..."
block2.addTransaction(walletA.sendFunds(walletB.publicKey, 1000))
block2.mineBlock(config.difficulty)
config.blockchain.append(block2)
print "walletA's balance is: %f" % walletA.getBalance()
print "walletB's balance is: %f" % walletB.getBalance()

block3 = Block(block2.hash)
print "walletB is attempting to send funds (20) to walletA..."
block3.addTransaction(walletB.sendFunds(walletA.publicKey, 20))
print "walletA's balance is: %f" % walletA.getBalance()
print "walletB's balance is: %f" % walletB.getBalance()

isChainValid()
