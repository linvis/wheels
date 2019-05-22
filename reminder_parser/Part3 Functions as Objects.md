---
Review_need: False
Review_date: 2019-05-22
Review_times: 1
---

# Part3 Functions as Objects

## Chapter 5 First-Class Function

**Functions in Python are first-class objects**

这句话什么意思呢，是说Python里的函数，本身就是一个对象(类对象)，因此它有以下特性

* Created at runtime

  运行时创建

* Assigned to a variable or element in a data structure

  可以赋值给其他变量

* Passed as an argument to a function

  可以接收参数传递

* Returned as the result of a function

  可以返回函数结果

```Python
def func(n):
  return n

f = func
f(1)
	1
  
# 函数作为参数, len就是参数
sorted(fruits, key=len)
```

[more reference](https://foofish.net/function-is-first-class-object.html)

### Anonymous Functions

也就是lambda

```
sorted(fruits, key=lambda word: word[::-1])
```



### The Seven Flavors of Callable Objects

* *User-defined functions*

  Created with def statements or lambda expressions.

* *Built-in functions*

  A function implemented in C (for CPython), like len or time.strftime.

* *Built-in methods*

  Methods implemented in C, like dict.get.

* *Methods*

  Functions defined in the body of a class.

* *Classes*

  When invoked, a class runs its __new__ method to create an instance, then __in it__ to initialize it, and finally the instance is returned to the caller. Because there is no new operator in Python, calling a class is like calling a function. (Usually calling a class creates an instance of the same class, but other behaviors are possible by overriding __new__.

* *Class instances*

  If a class defines a __call__ method, then its instances may be invoked as functions.

* *Generator functions*

  Functions or methods that use the yield keyword. When called, generator functions return a generator object.

### From Positional to Keyword-Only Parameters

可变参数，可以传list或dict给函数

```Python
def func(name, *content, **attrs):
  pass
# contest是一个list，attrs是一个字典
```

### Retrieving Information About Parameters

检查函数参数

```python
def clip(text, max_len=80):
	pass

>> clip.__defaults__
80

>>> clip.__code__ # doctest: +ELLIPSIS 
<code object clip at 0x...>

>>> clip.__code__.co_varnames 
('text', 'max_len', 'end', 'space_before', 'space_after')
>>> clip.__code__.co_argcount 
2

# 可以通过atrribute获取参数信息
# 实际上
from inspect import signature
sig = signature(clip)
>> str(sig)
'(text, max_len=80)'
>>> for name, param in sig.parameters.items():
				print(param.kind, ':', name, '=', param.default)
POSITIONAL_OR_KEYWORD : text = <class 'inspect._empty'> POSITIONAL_OR_KEYWORD : max_len = 80
```

### Function Annotations

静态类型解释

```Python
def clip(text:str, max_len:'int > 0'=80) -> str:
  pass

>>> clip.__annotations__ 
{'text': <class 'str'>, 'max_len': 'int > 0', 'return': <class 'str'>}
```

这里限制了传入参数类型，返回类型，实际上，这只是个注释，Python运行的时候，并不会做真正的类型检查

### The operator Module

```Python
from operator import itemgetter

sorted(metro_data, key=itemgetter(1)):
```

### Freezing Arguments with functools.partial

什么意思呢，我可以冻结一部分参数

比如mul接收两个参数，我冻结其中一个为3，

```python
from operator import mul
from functools import partial
triple = partial(mul, 3)
triple(7)
21
```



## Chapter 6 Design Patterns with Firsh-Class Functions

一种设计模式

首先，Python的设计哲学里，function和其他变量一样，就是一个变量，这有点C里函数指针的味道，当function被当做一个普通的变量后，就会有很大的自由度来使用function。

### 两种设计模式

一个购物问题，根据订单总价，和订单里商品的数量，从多个打折策略里，选择一个提供给用户。

#### 面向对象

```python
# 父类
class Promotion:
  def discount():
    ...
    
class Promotion1(Promotion):
  def discount():
     ...
      
class Promotion2(Promotion):
  def discount():
     ... 
```



这里，订单策略是一个类，不同的策略是它的子类，它一个问题是，很重，不够灵活，如果我需要对每个策略比较下，找一个最好的策略，就要加很多额外的代码，因为类的调用比较复杂。



#### 面向函数

```python
def Promotion():
	...
    
def Promotion1():
     ...
      
def Promotion2():
     ... 

```

但是如果是函数，我就可以把函数当成一个普通的变量，调用就很简单，可以把它当成一个普通的函数参数，直接传递。

封装成list，max(list)，找最优也会容易，