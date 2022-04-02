from collections import Counter
from collections.abc import Callable
from collections.abc import Hashable

"""
file: hashtable.py
description: This program generates a hashtable containing linked nodes. A chained hash table gets formed and no duplicate
values are added.
language: python3
author: Shreya Pramod, sp3045@rit.edu

"""

class ChainNode:
	"""

	The ChainNode class creates linked nodes which must be present at each entry of the hashtable.

	"""

	__slots__ = 'key', 'value', 'link'

	def __init__(self, key: any, value: any):
		self.key = key
		self.value = value
		self.link = None

class HashMap:
	"""

	The HashMap class creates the hashtable in which the linked Nodes are stored. A key, value pair is sent everytime
	a new entry is to be added to the hashtable.

	"""

	__slots__ = 'table', 'initial_num_buckets', 'load_limit', 'size', 'cap','key'

	def __init__(self, initial_num_buckets: int = 10, load_limit: float = 0.75):
		'''
		Create a new empty hash table.
		:param initial_num_buckets: starting number_of_buckets
		:param load_limit: See class documentation above.
		:param hash_func: the hash function used to compute the entry's location into the hash table
		:return: None
		'''

		self.size = 0
		self.cap = initial_num_buckets
		self.load_limit = load_limit
		self.table = [None] * self.cap
		# hash_func = hash_func(str(hash_func))

	def hash_func(self, key):

		"""
		Defines the hash function.
		:param key 	The key value for which the hash value is to be determined.
		:return: 	returns the hash value for the respective key.
		"""

		return ord(key[0].lower())-ord('a')

	def add(self, key, value):

		"""
		This function adds the linked nodes to the hash table. If another linked node is to be added then it would go to
		the link of the previous node.
		:param key 	The key value which is to be added to the hash table.
		:param key	The value of the key which is to be added to the hashtable as a linked node.

		"""

		sizeCount = 0
		index = self.hash_func(key) % self.cap
		presentNode = self.table[index]

		if self.table[index] is None:
			self.table[index] = ChainNode(key, value)
			sizeCount += 1
			return

		while presentNode is not None and self.table[index].key[0] == key[0]:
			oldNode = presentNode
			presentNode = presentNode.link
			if presentNode is None:
				oldNode.link = ChainNode(key, value)
				sizeCount += 1
				return

		oldNode = presentNode
		while presentNode is not None and self.table[index].key != key:
			oldNode = presentNode
			presentNode = presentNode.link
		oldNode.link = ChainNode(key, value)
		sizeCount += 1

		# rehashing
		if sizeCount / self.cap > self.load_limit:
			old = self.table
			self.size = 0
			self.cap = 2 * self.cap
			self.table = [None]*self.cap

			for entry in old:
				if entry is not None:
					self.put(entry[0], entry[1])

	def remove(self, key):

		"""
		This function find the location of the key, value pair and removes the linked node from the existing chain in the
		hash table.
		:param key 	The key value of the linked node present in the hash table.

		"""
		index = self.hash_func(key) % self.cap
		if self.table[index] is None:
			raise KeyError("Invalid Key")

		presentNode = self.table[index]
		oldNode = None
		while presentNode != None and presentNode.key != key:
			oldNode = presentNode
			presentNode = presentNode.link
		if presentNode is not None:
			if oldNode is None:
				self.table[index] = presentNode.link
			else:
				oldNode.link = oldNode.link.link

		if self.size / self.cap < (self.load_limit-1):
			old = self.table
			self.cap = 0.5*self.cap
			self.table = [None] * self.cap

			for entry in old:
				if entry is not None:
					self.put(entry[0], entry[1])

	def contains(self, key: Hashable):
		"""
		This function checks if a certain key is present in the hash table or not.
		:param key 	The key value that is present in the hashtable.

		"""
		index = self.hash_func(key) % self.cap

		if self.table[index] is None:
			return False

		presentNode = self.table[index]
		if self.table[index] is not None and self.table[index].key[0] != key[0]:
			index += 1
			if index == self.cap:
				index = 0
		oldNode = None
		while self.table[index].key[0] == key[0] and self.table[index].key!=key and presentNode.key != key:
			oldNode =presentNode
			if presentNode.link is None:
				return False
			presentNode = presentNode.link
		for i in range(self.cap):
			if self.table[i] is None:
				continue
			else:
				presentNode = self.table[i]
				if self.table[i] is not None and presentNode.link is None and key==presentNode.key:
					return True
				while presentNode.link is not None:
					presentNode = presentNode.link
					if key==presentNode.key:
						return True
		return self.table[index] is None

	def get(self, key):

		"""
		This function return the value of the specific key that is passed to the function.
		:param key 		The key value that is present in the hashtable.
		:return value 	The value of the key passed to the hash table.

		"""
		if self.contains(key)==True:
			index = self.hash_func(key) % self.cap
			presentNode = self.table[index]

			while self.table[index].key[0] == key[0] and self.table[index].key != key and presentNode.key != key:
				if presentNode.link is None:
					return False
				presentNode = presentNode.link
			return presentNode.value

	def imbalance(self):
		"""
		the average length of all non-empty chains minus 1, or 0 if hash table is empty
		:return avgValue 	The average value calculated.

		"""
		if self.table is None:
			return 0
		else:
			val = 1
			totVal = 0
			for i in range(self.cap):
				if self.table[i] is None:
					continue
				else:
					totVal+=1
					presentNode = self.table[i]
					if self.table[i] is not None and presentNode.link is None:
						val+=1
					while presentNode.link is not None:
						presentNode = presentNode.link
						val+=1
			avgVal = (val / totVal)-1
		return avgVal

	def __iter__(self):#->Iterator[Tuple[Hashable,Any]]
		"""
		returns an iterator for the current entries in the map
		:return avgValue 	The average value calculated.

		"""
		return Counter(self.table[:])

def testMap() -> None:
	"""
	This is a test function to test the different functionalities of the hash table.

	"""
	map = HashMap()
	map.add('ashley', 20)
	map.add('alicey', 10)
	map.add('amy', 50)
	map.add('orange', 30)

	print(map.remove('orange'))
	print(map.remove('ashley'))
	# map.remove('apple')

	print(map.contains('apple'))
	print(map.get('apple'))

	print(map.imbalance())

if __name__ == '__main__':
	testMap()