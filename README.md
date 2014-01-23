WHAT IS THIS?
=============

DiskDict is a replacement for Python `dict` object with one big difference.
When the number of items in the `dict` is larger than `cache_size`, the
disk will be used to store newly added data. This makes it possible for
the `dict` to contain more data than available in RAM. The drawback is that
the dict becomes much slower, but still usable.



USAGE EXAMPLE
=============

DiskDict could/should be used as a default `dict` object.


    d = DiskDict(cache_size=2)
    d[1] = 1
    d[2] = 4
    d[3] = 9
    d[4] = 16
    d[5] = 25

    # d == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

    d[10] = 100
    d[20] = 400
    d[30] = 900
    d[40] = 1600
    d[50] = 2500

    # d = {1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 40: 1600, 10: 100, 50: 2500, 20: 400, 30: 900}

    d[1] = -1
    d[2] = -4
    d[3] = -9
    d[4] = -16
    d[5] = -25

    # d = {1: -1, 2: -4, 3: -9, 4: -16, 5: -25, 40: 1600, 10: 100, 50: 2500, 20: 400, 30: 900}

    # d.counters == {'mem_hits': 6, 'misses': 0, 'set_ops': 15, 'get_ops': 25, 'mem_items': 2,
    #                'disk_items': 8, 'disk_hits': 19, 'del_ops': 0}



SPEED TESTS
===========


SSD Laptop cache_size=0
-----------------------

    Write   : n=1000000, s='a'*1024, ops/s=85607
    Read SEQ: n=1000000, s='a'*1024, ops/s=131875
    Read RND: n=1000000, s='a'*1024, ops/s=106608

    Write   : n=1000000, s=range(100), ops/s=28614
    Read SEQ: n=1000000, s=range(100), ops/s=27398
    Read RND: n=1000000, s=range(100), ops/s=26072


SSD Laptop cache_size=1000000
-----------------------------

    Write   : n=1000000, s='a'*1024, ops/s=316754
    Read SEQ: n=1000000, s='a'*1024, ops/s=704680
    Read RND: n=1000000, s='a'*1024, ops/s=409498


