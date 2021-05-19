# TicTacToe
Blockchain based TicTacToe program that uses proof of work concept and makes use of PubNub API to facilitate block exchange

REQUIREMENTS TO EXECUTE PROGRAM:
Since Alice is making the first move, Bob program must be running in terminal first so that he can be listening, Next, Run Alice program to initiate the Tic Tac Toe game. The program will continue running automatically until 9 moves are completed. Then the game ends and both programs terminate.
Altogether, there will only be 3 files in the submission folder. Two are Programs and 1 is the block0.json that Alice is meant to read during runtime

Programs:
-	A3_Alice.py
-	A3_Bob.py
Order of running:
-	Run A3_Bob.py by typing python3 A3_Bob.py first in terminal
-	Next, Run A3_Alice.py by typing python3 A3_Alice.py

For your convenience, the text files for Alice and Bob will be stored in separate folders called Alice_Blocks and Bob_Blocks respectively.

Alice_Blocks will contain:
-	A3_Alice.py
-	Block0.json
-	Block0.txt to Block9.txt
Bob_Blocks will contain:
-	A3_Bob.py
-	Block1.txt to Block9.txt


During the runtime, the history of the game will be generated In the form of Text files on both Alice and Bob’s side. These files of course will tally with one another on both sides. In total, Alice will have Text files of block0 to block9 while Bob will only have block1 to block9. The exchange of Json Blocks during the game is done though PubNub channels and is sent as a message instead of a file. 
