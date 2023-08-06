from setuptools import setup

long_description = """

This module add some useful features to Python inner classes :


```python
 class MyOuter:
    @inner
    class MyInner:
       def hello(self):
           print('Hello')
```

### outer attribute

The inner class gain an 'outer' attribute that reference its outer class.

```python
  >>> MyOuter.MyInner.outer 
  <class '__main__.MyOuter'>
```


### inner derivation
 
When the outer class is derived, the inner class is also derived in order
to point at the derived outer class.

```python
 class MyChildOuter(MyOuter):
    pass

 >>> MyChildOuter.MyInner.outer
 <class '__main__.MyChildOuter'>
```

### carried inheritance

When the inner class is redefined in an outer subclass, it will automatically
derivate from the inner class of the outer superclass.


```python
  class MyChildOuter(MyOuter):
     class MyInner:
       pass

  >>> MyChildOuter.MyInner().hello()
  Hello
```

###  inner instantiation
 
the outer attribute of an inner instance store it's outer instance

```python
  outer = MyOuter()
  
  >>> outer
  <__main__.MyOuter object at 0x03BAA990>
  >>> outer.MyInner().outer
  <__main__.MyOuter object at 0x03BAA990>
```

"""

setup(
    name="inner-class",
    version="0.2",
    description="Advanced inner classes for Python",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="S.Keim",
    author_email="s.keim@free.fr",
    license="MIT",
    py_modules=["inner"],
    zip_safe=True,
    test_suite="test",
    url="https://github.com/sebkeim/inner-class",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

