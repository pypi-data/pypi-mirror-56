An observable-ish pattern with `dask`'s pub sub model.

https://docs.dask.org/en/latest/futures.html#actors


```python
    import distributed, dataclasses, typing, munch, itertools, toolz
```

Use threads on the in-process client


```python
    client = distributed.Client(processes=False); client
```




<table style="border: 2px solid white;">
<tr>
<td style="vertical-align: top; border: 0px solid white">
<h3 style="text-align: left;">Client</h3>
<ul style="text-align: left; list-style: none; margin: 0; padding: 0;">
  <li><b>Scheduler: </b>inproc://10.8.0.40/15634/1</li>
  <li><b>Dashboard: </b><a href='http://localhost:8787/status' target='_blank'>http://localhost:8787/status</a>
</ul>
</td>
<td style="vertical-align: top; border: 0px solid white">
<h3 style="text-align: left;">Cluster</h3>
<ul style="text-align: left; list-style:none; margin: 0; padding: 0;">
  <li><b>Workers: </b>1</li>
  <li><b>Cores: </b>8</li>
  <li><b>Memory: </b>17.18 GB</li>
</ul>
</td>
</tr>
</table>



The `Observable` class is built to comply with the `distributed` client actor model.


```python
    class Observable:
        value = munch.Munch()
        def dlink(self, source, target=None, callable=None):
            source = id(source[0]), source[1]
            if target and callable is None: callable = toolz.partial(setattr, *target)
            if target: target = id(target[0]), target[1]
            self.value.update({source:{target:callable}})

        def link(self, source, target=None, callable=None):
            self.dlink(source, target, callable), self.dlink(target, source, callable)

        def trigger(self, source): 
            toolz.juxt(*self.value[id(source[0]), source[1]].values())(getattr(*source))
```

Create our `pubsub` client.


```python
    pubsub = client.submit(Observable, actor=True).result()
```

Demonstrate the efficacy with `Thing`.


```python
    @dataclasses.dataclass(unsafe_hash=True, eq=True)
    class Thing: a: int = 10
```


```python
    t = Thing(a=10)
    s = Thing(20)
    assert s != t
```

Link the traits.


```python
    pubsub.link((t, 'a'), (s, 'a'))
    t.a = 30
    assert s != t
```

`s` has not changed yet because we have no asked to update it yet.  We should likely over the `__setattr__` method for usability.


```python
    pubsub.trigger((t, 'a'))
    __import__('time').sleep(.1) # it seems now there race conditions!
    assert s.a == t.a == 30
```

go back the other way.


```python
    s.a = 40
    pubsub.trigger((s, 'a'))
    __import__('time').sleep(.1)
    assert t.a == 40
```
