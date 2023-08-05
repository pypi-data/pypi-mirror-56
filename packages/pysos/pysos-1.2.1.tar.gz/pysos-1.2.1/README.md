pySOS: Simple Objects Storage
=============================

> persistant dictionaries and lists for python

This is ideal for lists or dictionaries which either need persistence,
are too big to fit in memory or both.

There are existing alternatives like `shelve`, which are very good too.
There main difference with `pysos` is that:

- the data is stored in plain text format
- it provides both persistent dicts *and* lists
- objects must be json "dumpable" (no cyclic references, etc.)
- it's fast (much faster than `shelve` on windows, but slightly slower than native `dbms` on linux)
- it's unbuffered by design: when the function returns, you are sure it has been written on disk
- it's safe: even if the machine crashes in the middle of a big write, data will not be corrupted
- it is platform independent, unlike `shelve` which relies on an underlying `dbm` implementation, which may vary from system to system

Usage
-----

`pip install pysos`

Dictionaries:
```
import pysos
db = pysos.Dict('somefile')
db['hello'] = 'persistence!'
```

Lists:
```
import pysos
db = pysos.List('somefile')
db.append('it is now saved in the file')
```


Implementation notes
--------------------

### Is it thread safe?

No. It's not thread safe.
In practice, synchronization mechanisms are typically desired on a higher level.

### Why not make it async writes?

In the original version, there was a switch to choose between sync and async mode.
However, it turned out to have only a relatively small impact on overall performance.
Less than 25% on the hardware/OS/data I tested if I remember right.
Since the benefits seem rather low, I removed the flag and the associated code altogether, 
in order to ensure safety by default.
IMHO, it's preferable to loose a few microseconds rather than data upon a crash.


### Why not use memory mapped files?

I experimented with that too. In my experience, with the hardware/OS/data I tested,
it turned out to ...*suck*. Using memory mapped files lead to inconsistent and unpredictible performance,
often much slower than direct file access.

