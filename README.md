# Blockchain Implementation In Python

## Requirements:
- require python(>=3.6)
- pip install pycrypto

## Run the program
- python blockchain.py or python blockchain.py > output.txt

## Working
The blockchain is implemented in python3. For a given number, "N" random transactions are made. Each transaction has the following fields:
1. Merchant_id
2. customer_id
3. Customer’s public key
4. Merchant’s public key
5. Transaction date (mmddyyyy)
6. Transaction amount (xxxxxx.xx)
7. Customer’s signature over the concatenation of fields 1-4
8. Merchant’s digital signature over the concatenation of fields 1-5.


Once the new Blockchain is initiated, genesis block is created. Each transaction is added to a block and then updated with following fields.   
1. Block sequence number (for genesis block, block sequence number = 0) 
2. Hash of the previous block’s fields 1-7.
3. Miner’s digital signature over the concatenation of fields 6-8.

The previous hash field allows to create the chain of blocks and also helps in verifying the validity of the blockchain.
