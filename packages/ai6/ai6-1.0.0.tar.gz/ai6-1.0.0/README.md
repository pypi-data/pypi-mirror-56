# ai6 -- Artificial Intelligence Examples

## Install

```
$ pip install ai6
```

## Example

```py
import nn

def f(p):
	[x,y] = p
	return x*x + y*y

p = [1.0, 3.0]
nn.gradientDescendent(f, p)
```
