# Read Python3 Source File With Correct Encoding

according to <https://www.python.org/dev/peps/pep-0263/>,
python3 source file encoding are default to be `utf-8`.

But `open()`'s encoding will be `gbk` on windows,
So don't use `open` without encoding to read a python3 source file. 


example:

```python
from read_source import get_encoding, read
print(get_encoding('tests/source/gb18030/dash-star-dash.py')) # gb18030
with read('tests/source/gb18030/dash-star-dash.py') as f:
    print(f.read()) 
    # -*- coding: gb18030 -*-
```