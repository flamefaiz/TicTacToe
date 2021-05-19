import hashlib
import json,os
import random
from pubnub.callbacks import SubscribeCallback 
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pprint import pprint
import json
import sys

Transaction = []

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass

    def presence(self, pubnub, presence):
        pprint(presence.__dict__)

    def message(self, pubnub, message):
        print(message.__dict__)
        y = (message.__dict__)
        jsonobj = json.dumps(y)
        message_content = (json.loads(jsonobj))
        innerdata = message_content["message"]["content"]
        #Dict representation of jsonObj
        actualdata = json.loads(innerdata)
        #open a text file
        nsgfile = open("Block" + str(actualdata["TxID"]) +".txt","a")
        #write to the file 
        nsgfile.write(innerdata)
        nsgfile.write("\n")
        nsgfile.close()

        #Extracting the info from the previous Block
        TxID = int(actualdata["TxID"])
        nonce = int(actualdata["Nonce"])
        Hash = actualdata["Hash"]
        transactions = []
        transactions = actualdata["Transaction"]
        Transaction.append(transactions[1])

        #TTT is Tic Tac Toe. Randomizes move that Alice/Bob will make
        TTT = random.randint(1, 9)
        diff = False
        while(diff == False):
            if TTT not in Transaction:
                diff = True
            else:
                TTT = random.randint(1, 9)
                
        transactions = []
        transactions.append("Alice")
        transactions.append(TTT)
        TxID = TxID + 1
        nonce = 0
        exit = True
        while(exit):
            HashAndNonce = innerdata + str(nonce)
            DataTBH = hashlib.sha256(HashAndNonce.encode()).hexdigest()
            #Checking whether hashed data's first two digits are 00, or else, 
            #Will increment nonce value and rehash
            if int(DataTBH[0:2],16) == 0:
                exit =False
            nonce = nonce + 1
            #Dumping info for next Block to be sent
            tx = json.dumps({'TxID': TxID, 'Hash':DataTBH,'Nonce':nonce,'Transaction': transactions},sort_keys=False, indent=4, separators=(',', ': '))

        #Will only create and send new Blocks if the TxID matches the Specific BlockNumbers
        #Alice is supposed to send
        if(TxID == 3):
            createAndSend(tx)
        if(TxID == 5):
            createAndSend(tx)
        if(TxID == 7):
            createAndSend(tx)
        if(TxID == 9):
            createAndSend(tx)
            Transaction.append(transactions[1])
            #Unsubscribe and End Program
            pubnub.unsubscribe_all()


def my_publish_callback(envelope, status):
    print(envelope, status)

#Code used to open a new TextFile and Send data to pubnub channel
def createAndSend(tx):
    #Create a text file with the same number as new JsonBlock and Write to it
    # fileName = "Block"+ str(TxID)
    # file2 = open(fileName+".txt","w+")
    # file2.write(tx)
    # print("{}.txt created...".format(fileName))
    # file2.close()

    #Send JsonBlock to the pubnub channel
    pubnub.publish()\
    .channel("Channel-pdpe6rydz")\
    .message({"sender": pnconfig.uuid, "content": tx})\
    .pn_async(my_publish_callback)

#Block 0 is processed differently than the other blocks since
#it is read directly from a file instead of from pubnub channel
def block0():
    os.getcwd()

    #open JsonFile and read data inside
    f = open("block0" + ".json","r")
    data = f.read()
    f.close()

    #Create a text file with the same number as JsonBlock and Write to it
    fileName = "Block"+ str(0)
    file2 = open(fileName+".txt","w+")
    file2.write(data)
    print("{}.txt created...".format(fileName))
    file2.close()

    #TTT is Tic Tac Toe. Randomizes move that Alice/Bob will make
    TTT = random.randint(1, 9)
    transactions = []
    transactions.append("Alice")
    transactions.append(TTT)
    #Append the move made to a local array so that i can keep track
    #of previous moves made and can randomize a number different
    #From the ones already made
    Transaction.append(TTT)

    Jsondata = json.loads(data)
    TxID = int(Jsondata["TxID"]) + 1
    hashData = 0
    nonce = 0
    exit = True
    while(exit):
        HashedJson = hashlib.sha256(data.encode()).hexdigest()
        #Concatenating the Last Block and Nonce value
        HashAndNonce = HashedJson + str(nonce)
        #Hashing the Concatenated Daa
        DataTBH = hashlib.sha256(HashAndNonce.encode()).hexdigest()
        #Checking whether hashed data's first two digits are 00, or else, 
        #Will increment nonce value and rehash
        if int(DataTBH[0:2],16) == 0:
            exit =False
        nonce = nonce + 1
        tx = json.dumps({'TxID': TxID, 'Hash':DataTBH,'Nonce':nonce,'Transaction': transactions},sort_keys=False, indent=4, separators=(',', ': '))

    createAndSend(tx)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-5c8d0c48-6f47-11eb-a8a4-8af6467359f5"
pnconfig.publish_key = "pub-c-b4a923ec-f243-4185-8128-5997bb995e15"

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())

block0()

pubnub.subscribe()\
    .channels("Channel-pdpe6rydz")\
    .with_presence()\
    .execute()\
