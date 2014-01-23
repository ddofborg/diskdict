# -*- encoding: utf-8 -*-

import collections
import tempfile
import marshal as pickle
import os
import sys


class DiskDict():

	def __init__(self,init={},cache_size=1000000):
		self.counters = { 'mem_hits' : 0, 'disk_hits' : 0, 'misses' : 0, 'get_ops' : 0, 'set_ops' : 0,
			'del_ops' : 0, 'mem_items' : 0, 'disk_items' : 0 }
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
		if k in self.cache: # Make sure to overide the existing memory dict before adding it
			self.cache[k] = v
		elif self.counters['mem_items'] < self.cache_size:
			self.cache[k] = v
			self.counters['mem_items'] += 1
		else:
			try:
				if not self.storage_seek_at_end:
					self.storage_fd.seek(0,2) # Seek to EOF
					self.storage_seek_at_end = True

				if k not in self.disk_index:
					self.counters['disk_items'] += 1

				self.disk_index[k] = self.storage_fd.tell()
				pickle.dump(v, self.storage_fd)

			except:
				raise

		self.counters['set_ops'] += 1


	def __getitem__(self, k):
		self.counters['get_ops'] += 1

		if k in self.cache:
			self.counters['mem_hits'] += 1
			return self.cache[k]
		elif k in self.disk_index:
			try:
				self.counters['disk_hits'] += 1
				self.storage_fd.seek(self.disk_index[k])
				self.storage_seek_at_end = False
				data = pickle.load(self.storage_fd)
				return data
			except:
				raise
		else:
			self.counters['misses'] += 1
			raise KeyError( k )


	def __delitem__(self, k):
		if k in self.cache:
			del self.cache[k]
			self.counters['mem_items'] -= 1
		elif k in self.disk_index:
			del self.disk_index[k]
			self.counters['disk_items'] -= 1

		self.counters['del_ops'] += 1


	def __str__(self):
		return str( { el : self[el] for el in self.__iter__() } )


	def __iter__(self):
		for it in (self.cache, self.disk_index):
			for el in it:
				yield el


	def __len__(self):
		return self.counters['mem_items'] + self.counters['disk_items']

