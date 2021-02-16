#!/usr/bin/python3
'''
title           : blockchain.py
author          : Kritika Garg
date_created    : 2021-02-09
date_modified   : 2021-02-16
usage           : python blockchain.py
                  python blockchain.py > output.txt 
python_version  : 3.8
description     : A blockchain implemenation (CS864, Spring 21, ODU) 
References      : [1] http://adilmoujahid.com/posts/2018/03/intro-blockchain-bitcoin-python/
                  [2] https://youtu.be/SSo_EIwHSd4
'''

import sys
import Crypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import random
import datetime


			
class Blockchain():
	def __init__(self, miner_key, transactions):
		print("Creating empty blockchain...")
		self.blockchain = []
		#add genesis block
		self.genesis_block, self.genesis_block_hash = self.new_block(0,miner_key,{},None)
		self.blockchain.append(self.genesis_block)

	def new_block(self, seqn, miner_key, trans, prev_hash):
		self.seqn = seqn
		if seqn == 0: 
			data = '0' #For genesis block
			trans.update({"seqn" : self.seqn, "mSign" : '0'})
		else:
			trans["seqn"] = self.seqn  #field_7
			data = 	''.join([str(v) for k,v in trans.items()])
		block_hash = SHA256.new(data.encode('utf-8')).hexdigest()
		trans["prev_hash"] = prev_hash  #field_8
		miner_data = f'{trans["mSign"]}{trans["seqn"]}{trans["prev_hash"]}' #6-8
		trans["minerSign"] = Transactions.Sign(self, miner_data.encode('utf-8'), miner_key[1])
		return(trans, block_hash)
		
	def add_blocks(self): 
		prev_hash = self.genesis_block_hash			
		for seq_i in range(1,len(transactions)+1):
			trans = transactions[seq_i-1]
			block, block_hash = self.new_block(seq_i,miner_key,trans, prev_hash)
			self.blockchain.append(block)	
			prev_hash = block_hash #connecting blocks with prev_hash
		self.verify_chain(self.blockchain)
		return(self.blockchain)	

	def verify_chain(self, blockchain):
		print("Verifying validity of blockchain....")
		Valid_block = True
		for i in range(1,len(blockchain)-1):
			chain = blockchain[i]
			data = 	''.join([str(v) for k,v in chain.items() if k not in ['prev_hash','minerSign']])
			block_hash = SHA256.new(data.encode('utf-8')).hexdigest()
			prev_hash = blockchain[i+1]["prev_hash"]
			if block_hash != prev_hash:
				Valid_block = False
				print(f"Invalid Blockchain: Block #{i} is altered!!!!")
				break   
		if Valid_block == True:		
			print("Blockchain is valid!")
		print("\n")	
		print("-----------------------------------")	



class Transactions():
	def __init__(self, n, No_of_customers, No_of_merchants):
		self.n = n  #No_of_transactions
		print(f"Generate {No_of_customers} key pairs for customers..")
		self.cKeys = [self.generate_key_pairs() for i in range(0,No_of_customers)]
		print(f"Generate {No_of_merchants} key pairs for merchants..")
		self.mKeys = [self.generate_key_pairs() for i in range(0,No_of_merchants)]

	def generate_key_pairs(self):
		private_key = RSA.generate(2048)
		public_key   = private_key.publickey().exportKey("PEM") 
		return(public_key, private_key)	


	def Sign(self, data, private_key):
		# hash the data
		data_hash = SHA256.new(data)#.hexdigest()
		# encrypting the hash with the private key to sign the transaction
		signature = PKCS1_v1_5.new(private_key).sign(data_hash)
		return(signature)			
		
	def random_date(self):
		start = datetime.date(2015, 1, 1)
		end = datetime.date.today()
		rdate = start + (end - start) * random.random()
		return(rdate.strftime("%m/%d/%Y"))

	def gen_transactions(self):
		print(f"Generate {self.n} random transactions..")
		transactions = []
		for i in range(0,self.n):
			M = random.randint(1,2)
			C = random.randint(1,5)
			cPrivKey = self.cKeys[C - 1][1]
			mPrivKey = self.mKeys[M - 1][1]
			trans = {	
				"cPubKey" : self.cKeys[C - 1][0].decode("utf-8"),  #field_1
				"mPubKey" : self.mKeys[M - 1][0].decode("utf-8"),  #field_2
				"date" : self.random_date(),          #field_3
				"amount" : round(random.uniform(0, 100),2) #field_4
				}
			#data = f'{trans["cPubKey"]}{trans["mPubKey"]}{trans["date"]}{trans["amount"]}'
			data = 	''.join([str(v) for k,v in trans.items()])
			data = data.encode('utf-8')		
			trans["cSign"] = self.Sign(data, cPrivKey)   #field_5
			trans["mSign"] = self.Sign(data+trans["cSign"], mPrivKey) #field_6
			transactions.append(trans)
			print(f'{i}: M{M}({trans["mPubKey"][100:117]}) C{C}({trans["cPubKey"][100:117]}) {trans["date"]} ${trans["amount"]}')
		print("\n")
		return(transactions)

	def search_transactions(self, participant, blockchain):
		#search for transactions by public key
		Name,idx = participant.lower()
		nPubKey = Name+"PubKey" #keyname
		if Name+"Keys" == 'cKeys':
			nKeys = self.cKeys
		elif Name+"Keys" == 'mKeys':
			nKeys = self.mKeys
		PubKey = nKeys[int(idx) - 1][0].decode("utf-8")  
		participant_transactions =[]
		print(f'Printing all transactions for {participant}')
		for trans in blockchain[1:]:
			if trans[nPubKey] == PubKey:
				participant_transactions.append(trans)
				print(f'{trans["seqn"]}: {trans["mPubKey"][100:117]} {trans["cPubKey"][100:117]} {trans["date"]} ${trans["amount"]}')
		print("-----------------------------------")
		return(participant_transactions)
	




if __name__ == '__main__':
	No_of_customers = int('5')
	No_of_merchants = int('2')
	No_of_transactions = int('25')	
	t1 = Transactions(No_of_transactions, No_of_customers, No_of_merchants)
	transactions = t1.gen_transactions()

	print("Generate 1 key pair for miner..")
	miner_key = t1.generate_key_pairs()

	full_chain = Blockchain(miner_key, transactions)
	print("Adding Transactions to the Blockchain...")
	blockchain = full_chain.add_blocks()

	print("Demonstrating detection of tampered block in the blockchain: \n")
	print("Incrementing the amount in block 10 by $10.00")
	block_trans = blockchain[10]
	print(f'Initial amount: {block_trans["amount"]}')
	block_trans["amount"] += 10.00
	print(f'New amount: {block_trans["amount"]}')
	full_chain.verify_chain(blockchain)
	
	print("-----------------------------------")
	print("Demonstrating how to search for transactions using public key: \n")
	participants = ["C3","M2"]
	for p in participants:
		p_transactions = t1.search_transactions(p, blockchain)







