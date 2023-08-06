# nn6 -- Neural Network 6

## Install

```
$ pip install nn6
```

## Example

```py
import ai6

def f(p):
	[x,y] = p
	return x*x + y*y

p = [1.0, 3.0]
ai6.gd(f, p)
```
