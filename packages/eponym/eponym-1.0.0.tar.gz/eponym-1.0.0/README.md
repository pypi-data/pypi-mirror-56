# Eponym

Eponym seeks to become a decent username generator. So far this repository includes two handpicked lists of *Descriptors* and *Things* and a basic username generator function. At one point a flexible generator will be added.

### Usage

```python
from eponym import generate_username

print(generate_username())

"""Example outputs:
'ExitedArrogantPlant2873'
'PotentialRetroDiscoverer7701'
'SelfishCheatingBamboo0926'
'SimpleChirpyCarrot6735'
"""
```

### Custom generator

The inbuilt generator currently has no options such as `pattern` or `max_length`. If you want to build a custom generator using the Eponym data, take a look at the `eponym/generator.py` file.
