class Node:
	def __init__(self, value):
		self.value = value
		self.next: Node = None
		self.prev: Node = None

class Queue:
	def __init__(self, max_size: int) -> None:
		self.size = 0
		self.max_size = max_size
		self.first: Node = None
		self.last: Node = None

	def add(self, value):
		n = Node(value)
		if self.size == 0:
			self.first = n
			self.last = n
			self.size += 1
			return
		self.size += 1
		self.first.prev = n
		n.next = self.first
		self.first = n
		if self.size > self.max_size:
			self.remove()

	def remove(self):
		p = self.last.prev
		self.last = p
		self.last.next = None
		self.size -= 1

	def __iter__(self):
		self.it = self.first
		return self

	def __next__(self):
		p = self.it
		if p == None:
			raise StopIteration
		self.it = self.it.next
		return p.value