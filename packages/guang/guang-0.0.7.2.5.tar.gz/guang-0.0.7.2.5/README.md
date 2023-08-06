# Tools

[![image](https://img.shields.io/badge/Pypi_package-0.0.5-green.svg)](https://pypi.org/project/guang)
[![image](https://img.shields.io/badge/python-3.X-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-GNU_GPL--v3-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-K.y-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)



Scientific calculation of universal function library

# Examples

- Convert audio in .mp3/ .wav format to (sample rate=16k, single channel) .wav format

```python
from guang.Voice.convert improt cvt2wav
cvt2wav(orig_path, target_path, sr=16000)
```



* Convert a dictionary to dotable dictionary:

```python
from guang.Utilt.toolsFunc import dict_dotable
a = {'a':{'b':1}}
a = dict_dotable(a)
print(a.a.b)
```



```python

```

