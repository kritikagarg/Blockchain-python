# Blockchain Implementation In Python

## Requirements:
- require python(>=3.6)
- pip install pycrypto

## Run the program
- python blockchain.py or python blockchain.py > output.txt

## Working
A simple implementation of the blockchain for logging transactions with a single miner. The blockchain is implemented in python3.

### Generate random transactions
"N" random transactions are generated, for a given number of transactions(N), the number of customers(C) and noumber of merchants(M). The default value of N is 25, C is 5 and M is 2.  

Each transaction has the following fields:
<ol start="1">
  <li>Customer’s public key</li>
  <li>Merchant’s public key</li>
  <li>Transaction date (mmddyyyy)</li>
  <li>Transaction amount (xxxxxx.xx)
  <li>Customer’s signature over the concatenation of fields 1-4
  <li>Merchant’s digital signature over the concatenation of fields 1-5.
</ol>

### Initiate Blockchain
Once the new Blockchain is initiated, genesis block is created. Each transaction is added to a new block and then following fields added by the miner:
<ol start="7">
  <li>Block sequence number (for genesis block, block sequence number = 0) 
  <li>Hash of the previous block’s fields 1-7.
  <li>Miner’s digital signature over the concatenation of fields 6-8.
</ol>

### Validite the blockchain & detect tampered block
The prev hash field allows to create the chain of blocks and also helps in verifying the validity of the blockchain. To verify the blockchain, the hash of the block based on fields 1-7 is calculated again. This calculated hash is compared with the prev_hash value in the next block to validate the blockchain.

Demonstrating detection of tampered block in the blockchain: 
```
Incrementing the amount in block 10 by $10.00
Initial amount: 72.43
New amount: 82.43
Verifying validity of blockchain....
Invalid Blockchain: Block #10 is altered!!!!
```

### Search for transactions for a given participant(Merchant/Customer)

For a given participant, ex. C3,M2, all the transactions are collected by searching using participant's public key.

Demonstrating how to search for transactions using public key: 
```
Printing all transactions for C3
2: WC2IzJ/I4vPPl43hV SK1wOwenO1b8QwRgU 08/04/2020 $38.26
8: WC2IzJ/I4vPPl43hV SK1wOwenO1b8QwRgU 02/13/2019 $96.36
9: sSx6obgsd661JEQDw SK1wOwenO1b8QwRgU 07/22/2015 $50.85
12: WC2IzJ/I4vPPl43hV SK1wOwenO1b8QwRgU 08/10/2018 $63.39
```
