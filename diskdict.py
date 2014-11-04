# -*- encoding: utf-8 -*-

import tempfile
import cPickle as pickle


class DiskDict(dict):

	def __init__(self, init=None, cache_size=500000):
		if init == None:
			init = dict()
		self._counters = { 'mem_hits' : 0, 'disk_hits' : 0, 'misses' : 0,
			'get_ops' : 0, 'set_ops' : 0, 'del_ops' : 0, 'mem_items' : 0,
			'disk_items' : 0, }
		self.cache_size = cache_size
		self.cache = {}
		self.disk_index = {}
		self.storage_seek_at_end = False
		try:
			self.storage_fd = tempfile.TemporaryFile(mode='w+b',prefix='diskdict-')
		except:
			raise

		if len(init):
			for k in init:
				self[k] = init[k]


	def __setitem__(self, k, v):
		self._counters['set_ops'] += 1

		if k in self.cache: # Make sure to overide the existing memory dict before adding it
			self.cache[k] = v
		elif self._counters['mem_items'] < self.cache_size:
			self.cache[k] = v
			self._counters['mem_items'] += 1
		else:
			try:
				if not self.storage_seek_at_end:
					self.storage_fd.seek(0,2) # Seek to EOF
					self.storage_seek_at_end = True

				if k not in self.disk_index:
					self._counters['disk_items'] += 1

				self.disk_index[k] = self.storage_fd.tell()
				pickle.dump(v, self.storage_fd)
			except:
				raise


	def __getitem__(self, k):
		self._counters['get_ops'] += 1

		if k in self.cache:
			self._counters['mem_hits'] += 1
			return self.cache[k]
		elif k in self.disk_index:
			try:
				self._counters['disk_hits'] += 1
				self.storage_fd.seek(self.disk_index[k])
				self.storage_seek_at_end = False
				data = pickle.load(self.storage_fd)
				# FIXME: If data is an instance of a class it will return an
				# empty class without the data. Possible because an object has
				# references to another instances which are in memory.
				return data
			except:
				raise
		else:
			self._counters['misses'] += 1
			raise KeyError( k )


	def __delitem__(self, k):
		self._counters['del_ops'] += 1
		if k in self.cache:
			del self.cache[k]
			self._counters['mem_items'] -= 1
		elif k in self.disk_index:
			del self.disk_index[k]
			self._counters['disk_items'] -= 1


	def __str__(self):
		return unicode( { k : self[k] for k in iter(self) } )


	def __iter__(self):
		for it in (self.cache, self.disk_index):
			for el in it:
				yield el


	def __len__(self):
		return self._counters['mem_items'] + self._counters['disk_items']


	@property
	def counters(self):
		self.storage_fd.seek(0,2) # Seek to EOF
		self.storage_seek_at_end = True
		self._counters['len'] = len(self)
		self._counters['cache_file_size'] = self.storage_fd.tell()
		return self._counters


	def keys(self):
		return [k for k in iter(self)]


	def values(self):
		return [self[k] for k in iter(self)]


	def get(self, k, d=None):
		try:
			return self[k]
		except KeyError:
			return d


	def set(self, k, v):
		self[k] = v


	def items(self):
		return [(k, self[k]) for k in iter(self)]


