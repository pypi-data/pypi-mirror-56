#!python

from __future__ import division, print_function  # Python 2 and 3 compatibility
from array import array
from collections import Counter, defaultdict, deque, namedtuple
from dataclasses import make_dataclass
from fractions import Fraction
from functools import wraps
from random import random, choice
from typing import Iterable, Optional, Tuple, Union

from .online import Var
from .stats import Distro, Sample
from .utils import (binsearch, invert_dict, LogMethodCalls,
                    merge_data_containing_ints, p)


class Histogram:

    __slots__ = ("about", "source_text", "word_to_freq", "table",
                 "dim_priority", "distro", "sample", "_make_histogram_skipped")

    def __init__(self, source_text=None, word_to_freq=None):
        """Takes text or its histogram as input."""
        self.source_text = source_text
        self.word_to_freq = (word_to_freq
                             if word_to_freq else self._make_histogram())
        self._make_histogram_skipped = bool(word_to_freq)
        self.distro = Distro(self.word_to_freq)
        self.sample = Sample(self.distro)

    def __get_item__(self, key):
        try:
            return self.distro[key]
        except ValueError as e:
            raise e

    def __len__(self):
        return len(self.distro)

    def _make_histogram(self):
        word_to_freq = defaultdict(int)

        for line in self.source_text:
            for word in self.line_as_words(line):
                sword = "".join(word)
                word_to_freq[sword] += 1
                new_freq = word_to_freq[sword]
        return word_to_freq

    @property
    def tokens(self):
        return self.distro.tokens

    @property
    def types(self):
        return self.distro.types

    @property
    def histogram(self):
        return self.word_to_freq

    @property
    def unique_words(self):
        return len(self.word_to_freq)

    @staticmethod
    def line_as_words(line):
        """Given a string of words, yield the next word as a list."""
        word = []
        for char in line:
            if char == " ":
                yield Histogram.strip_non_alnums(word)
                word = []
            else:
                word.append(char)
        if len(word):
            yield Histogram.strip_non_alnums(word)

    @staticmethod
    def bin_search(array, prob):
        """Search for the lowest matching probability in array consisting of
        namedtuples."""
        lo = 0
        hi = len(array) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if (array[mid].cumulative <= prob and
                (mid == len(array) - 1 or array[mid + 1].cumulative > prob)):
                return mid
            if array[mid].cumulative < prob:
                lo = mid + 1
            else:
                hi = mid
        return None

    @staticmethod
    def is_valid_start_char(char):
        """Checks if given character is valid at the start of a string"""
        allowed_start_chars = {"$", "£"}
        return char.isalnum() or char in allowed_start_chars

    @staticmethod
    def is_valid_end_char(char):
        """Checks if given character is valid at the end of a string"""
        allowed_end_chars = {"%"}
        return char.isalnum() or char in allowed_end_chars

    @staticmethod
    def strip_non_alnums(string):
        """Custom strip for removing all non-alphanumeric characters."""
        start = 0
        while start < len(string) and not Histogram.is_valid_start_char(
                string[start]):
            start += 1
        end = len(string) - 1
        while end >= 0 and not Histogram.is_valid_end_char(string[end]):
            end -= 1
        return string[start:end + 1]

    def similarity(self, other_histogram):
        return self.distro.similarity(other_histogram.distro)

    def frequency(self, word):
        return self.word_to_freq[word]

    def as_cumulative_freqs(self):
        freqs_list = []
        cumulative_freq = 0.
        for i in range(self.about.max + 1):
            if i in self.freq_to_words:

                freqs_list.append(
                    namedtuple("Item",
                               "freq cumulative words")(i, cumulative_freq,
                                                        self.freq_to_words[i]))
                cumulative_freq += Fraction(i, self.total_words) * len(
                    self.freq_to_words[i])
        return freqs_list

    def rand_word(self):
        return self.sample.randword()

    def as_list_of_lists(self):
        return [[word, freq] for word, freq in self.word_to_freq.items()]

    def as_list_of_tuples(self):
        return [(word, freq) for word, freq in self.word_to_freq.items()]

    def plot(self):
        words, freqs = zip(*self.freq_to_words.items())

        plt.bar(range(len(data)), freqs, tick_label=words)
        #plt.savefig('bar.png')
        plt.show()


class Listogram(Distro, metaclass=LogMethodCalls,
                logs_size=4):  #, metaclass=LogMethodCalls, logs_size=8):
    """Listogram is a histogram implemented as a subclass of the list type."""
    __slots__ = ("temp_word_to_freq", "sampler", "_logs_")

    def __init__(self, word_list=None):
        """Initialize this histogram as a new list and count given words."""

        # hold a temporary array as new (word,counts) get added.
        # add these to new Listogram object when add_count method calls are
        # finished.
        self.temp_word_to_freq = []

        if word_list is not None:
            super().__init__(tuple(Counter(word_list).items()))
        else:
            super().__init__({})
        self.sampler = Sample(self)

    def add_count(self, word, count=1):
        """Increase frequency count of given word by given count amount."""
        # build temp array; duplicates are handled later
        self.temp_word_to_freq.append((word, count))

    def frequency(self, word):
        """Return frequency count of given word, or 0 if word is not found."""
        self.rebuild_with_latent_wordcounts()
        return self.get(word, 0)

    def __contains__(self, word):
        """Return boolean indicating if given word is in this histogram."""
        return super().__contains__(word)

    def _index(self, target):
        """Return the index of entry containing given target word if found in
        this histogram, or None if target word is not found."""
        self.rebuild_with_latent_wordcounts()
        return self.index_of(target)

    def index_of(self, target):
        """Return the index of entry containing given target word if found in
        this histogram, or None if target word is not found."""
        self.rebuild_with_latent_wordcounts()
        idx = bin_search(self.word_to_freq, target, key=lambda x: x[0])
        if idx > -1:
            return idx

    def sample(self):
        """Return a word from this histogram, randomly sampled by weighting
        each word's probability of being chosen by its observed frequency."""
        self.rebuild_with_latent_wordcounts()
        return self.sampler.randword()

    def rebuild_with_latent_wordcounts(self):
        """Reconstructs object if last method called was add_count."""
        if len(self._logs_) > 2 and self._logs_[-1 - 2].name == "add_count":
            # if the most recent class or instance method call wasn't add_count,
            # re-initialize current object.
            super().__init__(
                merge_data_containing_ints(self.word_to_freq,
                                           self.temp_word_to_freq))
            self.sampler = Sample(self)


class Dictogram(Distro, metaclass=LogMethodCalls, logs_size=4):
    """Dictogram is a histogram implemented as a subclass of the dict type."""
    __slots__ = ("temp_word_to_freq", "sampler", "_logs_")

    def __init__(self, word_list=None):
        """Initialize this histogram as a new dict and count given words."""

        # Temporarily hold the (word,count) added from add_count, which will
        # be added to a new distribution as part of a new Dictogram
        self.temp_word_to_freq = defaultdict(int)

        if word_list is not None:
            super().__init__(dict(Counter(word_list)))
        else:
            super().__init__({})
        self.sampler = Sample(self)

    def items(self):
        return self.word_to_freq.items()

    def add_count(self, word, count=1):
        """TIME EXPENSIVE: must call super().__init__() every time
        Increase frequency count of given word by given count amount."""
        self.temp_word_to_freq[word] += count

    def frequency(self, word):
        """Return frequency count of given word, or 0 if word is not found."""
        self.rebuild_with_latent_wordcounts()
        return self.get(word, 0)

    def sample(self):
        """Return a word from this histogram, randomly sampled by weighting
        each word's probability of being chosen by its observed frequency."""
        self.rebuild_with_latent_wordcounts()
        return self.sampler.randword()

    def rebuild_with_latent_wordcounts(self):
        """Reconstructs object if last method called was add_count."""
        if len(self._logs_) > 2 and self._logs_[-1 - 2].name == "add_count":
            # if the most recent class or instance method call wasn't add_count,
            # re-initialize current object.
            super().__init__(
                merge_data_containing_ints(self.word_to_freq,
                                           self.temp_word_to_freq))
            self.sampler = Sample(self)


class Codagram:
    """A datastructure for code statistics and comparisons."""
    pass
