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
        actualdata = json.loads(innerdata)

        #open a text file
        nsgfile = open("Block" + str(actualdata["TxID"]) +".txt","a")
        #write to the file 
        nsgfile.write(innerdata)
        nsgfile.write("\n")
        nsgfile.close()

        #Extracting the info from the previous Block
        TxID = int(actualdata["TxID"])
        #Unsubscribe and End Program
        if(TxID == 9):
            pubnub.unsubscribe_all()
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
        transactions.append("Bob")
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
        if(TxID == 2):
            createAndSend(tx)
        if(TxID == 4):
            createAndSend(tx)
        if(TxID == 6):
            createAndSend(tx)
        if(TxID == 8):
            createAndSend(tx)


def my_publish_callback(envelope, status):
    print(envelope, status)

#Code used to open a new TextFile and Send data to pubnub channel
def createAndSend(tx):
    #Create a text file with the same number as new JsonBlock and Write to it
    # fileName = "Block"+ str(TxID)
    # file2 = open(fileName + ".txt","w+")
    # file2.write(tx)
    # print("{}.txt created...".format(fileName))
    # file2.close()

    #Send JsonBlock to the pubnub channel
    pubnub.publish()\
    .channel("Channel-pdpe6rydz")\
    .message({"sender": pnconfig.uuid, "content": tx})\
    .pn_async(my_publish_callback)



pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-5c8d0c48-6f47-11eb-a8a4-8af6467359f5"
pnconfig.publish_key = "pub-c-b4a923ec-f243-4185-8128-5997bb995e15"

pubnub = PubNub(pnconfig)

pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe()\
    .channels("Channel-pdpe6rydz")\
    .with_presence()\
    .execute()\





