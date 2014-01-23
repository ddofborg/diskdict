#!/usr/bin/python -u
# -*- encoding: utf-8 -*-

import random
import sys
import os
from diskdict import DiskDict
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def test_basics():
	print "Starting basis test, cache_size=2:"
	print "  ",
	d = DiskDict(cache_size=2)
	d[1] = 1
	d[2] = 4
	d[3] = 9
	d[4] = 16
	d[5] = 25
	assert( str(d) == '{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}' )
	print ".",
	assert( len(d) == 5 )
	print ".",
	d[10] = 100
	d[20] = 400
	d[30] = 900
	d[40] = 1600
	d[50] = 2500
	assert( str(d) == '{1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 40: 1600, 10: 100, 50: 2500, 20: 400, 30: 900}' )
	print ".",
	assert( len(d) == 10 )
	print ".",
	d[1] = -1
	d[2] = -4
	d[3] = -9
	d[4] = -16
	d[5] = -25

	assert( str(d) == '{1: -1, 2: -4, 3: -9, 4: -16, 5: -25, 40: 1600, 10: 100, 50: 2500, 20: 400, 30: 900}' )
	print ".",
	assert( len(d) == 10 )
	print ".",

	del d[1]
	assert( len(d) == 9 )
	print ".",

	assert( str(d.counters) == "{'mem_hits': 6, 'misses': 0, 'set_ops': 15, 'get_ops': 25, 'mem_items': 1, 'disk_items': 8, 'disk_hits': 19, 'del_ops': 1}" )
	print ".",
	print
	print "  Counters: " + str(d.counters)

	print "all rests passed."

def speed_test_w(n,s):
	print " ",
	c=0
	p = min(100000,int(n/10))
	for i in range(n):
		if c % p == 0:
			print str(int(round(float(c) / n * 100))) + '%',
		d['a'+str(i)] = ( i*i, s )
		c += 1
	print 'done',

def speed_test_r(n,s):
	print " ",
	c=0
	p = min(100000,int(n/10))
	for i in range(n):
		if c % p == 0:
			print str(int(round(float(c) / n * 100))) + '%',
		x = d['a'+str(i)]
		c += 1
	print 'done',

def speed_test_rnd(n,s):
	print " ",
	r = range(n)
	random.shuffle(r)
	c=0
	p = min(100000,int(n/10))
	for i in r:
		if c % p == 0:
			print str(int(round(float(c) / n * 100))) + '%',
		x = d['a'+str(i)]
		c += 1
	print 'done',


if __name__ == '__main__':

	test_basics()
	print


	import timeit

	n = 100000

	print "Starting speed test with {} 1k strings, cache_size=0:".format( str(n) )

	s = "'" + 'a' * 1024 + "'"
	d = DiskDict(cache_size=0)

	t = int( n/timeit.timeit('speed_test_w({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Write   : n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	t = int( n/timeit.timeit('speed_test_r({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Read SEQ: n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	t = int( n/timeit.timeit('speed_test_rnd({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Read RND: n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	print "  Counters: " + str(d.counters)
	print "done."
	print

	n = 100000

	print "Starting speed test with {} 100 item lists, cache_size=0:".format( str(n) )

	s = range(100)
	d = DiskDict(cache_size=0)

	t = int( n/timeit.timeit('speed_test_w({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Write   : n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	t = int( n/timeit.timeit('speed_test_r({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Read SEQ: n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	t = int( n/timeit.timeit('speed_test_rnd({},{})'.format(n,s), setup='from __main__ import speed_test_w,speed_test_r,speed_test_rnd', number=1) )
	print " >> Read RND: n={}, s={}/{}, ops/s={}".format( n, type(s), len(s), t )

	print "  Counters: " + str(d.counters)
	print "done."
	print
