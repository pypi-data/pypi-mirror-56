# realtweets: the world's most popular destination for real tweets

[![Build Status](https://travis-ci.com/escofresco/makeschool_fsp2_realtweets.svg?branch=master)](https://travis-ci.com/escofresco/makeschool_fsp2_realtweets)

[![codecov](https://codecov.io/gh/escofresco/makeschool_fsp2_realtweets/branch/master/graph/badge.svg)](https://codecov.io/gh/escofresco/makeschool_fsp2_realtweets)

# kiwi

kiwi is a Python library generating and using histograms of a large corpus.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install kiwi.

```bash
pip install kiwi
```
 
## Usage

```python
from kiwi.grams import Histogram

# Generate a histogram from a list of sentences
hist = Histogram(['A sentence here.',
                  'A sentence there.',
                  'A sentence anywhere.'])

# Generate a histogram from a text file
with open('corpus.txt', 'r') as file:
    file_hist = Histogram(file)

# Compare the similarity of two histograms
similarity = hist.similarity(file_hist)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
