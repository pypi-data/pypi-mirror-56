from collections import defaultdict, deque
from fractions import Fraction
from math import ceil, floor, log2, log
from random import choice, randint, random, randrange
import unittest

import numpy as np

from kiwi.stats import Distro
from kiwi.utils import (binsearch, invert_dict, generate_samples,
                        histogram_similarity, ismethod, LogMethodCalls,
                        map_to_binary, merge_nonsequentials_containing_ints,
                        merge_data_containing_ints,
                        merge_sequentials_containing_ints, p, randints,
                        sample_size)
from .data import small_data


class UtilsTestSuite(unittest.TestCase):
    def test_invert_dict_norm(self):
        input = {"a": 3, "b": 1, "c": 1, "d": 4, "e": 3}
        inverse = {1: ["b", "c"], 3: ["a", "e"], 4: ["d"]}
        self.assertEqual(inverse, invert_dict(input))

    def test_invert_dict_edges(self):
        input = {}
        inverse = {}
        self.assertEqual(inverse, invert_dict(input))

        input = {"a": 3}
        inverse = {3: ["a"]}
        self.assertEqual(inverse, invert_dict(input))

        input = {"a": 1, "b": 1, "c": 1}
        inverse = {1: ["a", "b", "c"]}
        self.assertEqual(inverse, invert_dict(input))

    def test_sample_size(self):
        self.assertEqual(186, sample_size(6.95, 1))

    def test_map_to_binary(self):
        array = []
        # test null
        self.assertEqual([], list(map_to_binary([])))

        # test single value
        self.assertEqual(["0"],
                         list(map_to_binary(["asdfj jhasfjhgask jghasdg"])))

        # test exact powers of two
        self.assertEqual(["0", "1"], list(map_to_binary(["a", "b"])))
        self.assertEqual(["00", "01", "10", "11"],
                         list(map_to_binary(["a", "b", "c", "d"])))

        # test uneven powers of two
        self.assertEqual(["00", "01", "10"],
                         list(map_to_binary(["a", "b", "c"])))
        # test uneven powers of two
        self.assertEqual(["000", "001", "010", "011", "100"],
                         list(map_to_binary(["a", "b", "c", "d", "e"])))

    def test_histogram_similarity(self):
        expected_words = ["a", "b"]
        expected_probs = [0., 1.]
        actual_words = ["a", "b"]
        actual_probs = [0., 1.]
        self.assertEqual(
            histogram_similarity(expected_words, expected_probs, actual_words,
                                 actual_probs), 0.)

        actual_probs = list(reversed(actual_probs))
        self.assertEqual(
            histogram_similarity(expected_words, expected_probs, actual_words,
                                 actual_probs), 1.)

        # When binary words are passed directly, order shouldn't be preserved
        expected_words = ["0", "1"]
        expected_probs = [0., 1.]
        actual_words = ["1", "0"]
        actual_probs = [1., 0.]

        self.assertEqual(
            histogram_similarity(expected_words, expected_probs, actual_words,
                                 actual_probs), 0.)

        actual_probs = list(reversed(actual_probs))
        self.assertEqual(
            histogram_similarity(expected_words, expected_probs, actual_words,
                                 actual_probs), 1.)

    def test_generate_samples(self):
        words = ("apple", "banana")
        freqs = (50, 50)
        expected_distro = Distro(word_to_freq=tuple(zip(words, freqs)))

        def rand_word():
            return choice(words)

        n_samples = 10000

        # generate_samples returns Counter of keys generated from rand_word
        actual_distro = Distro(generate_samples(n_samples, rand_word))

        # the correct number of samples were generated
        self.assertEqual(sum(actual_distro.freqs), n_samples)

        # given n_samples is large, it's very likely every word appears at least
        # once
        self.assertIn("apple", actual_distro)
        self.assertIn("banana", actual_distro)

        # expected_distro and actual_distro should be nearly identical
        self.assertAlmostEqual(expected_distro.similarity(actual_distro), 0, 3)

    def test_binsearch(self):
        words = sorted(small_data.words)
        self.assertEqual(binsearch((), ""), -1)
        self.assertEqual(binsearch(words, "marmalade"), -1)
        for i in range(len(words)):
            rand_idx = randrange(i + 1)
            words_up_to_now = words[:i + 1]
            rand_word = words_up_to_now[rand_idx]

            with self.subTest(i=i,
                              words=words_up_to_now,
                              rand_index=rand_idx,
                              rand_word=rand_word):
                idx = binsearch(words_up_to_now, rand_word)
                self.assertNotEqual(idx, -1)  # was anything found?
                self.assertEqual(words_up_to_now[idx], rand_word)

    def test_rand_ints(self):

        self.assertEqual(randints(0), [])  # null case
        with self.assertRaises(ValueError):
            # variance and deviation passed together would change the mean
            randints(50, variance=4, deviation=.5)
        with self.assertRaises(ValueError):
            # at least 1 must be at every index
            randints(50, target_sum=49)

        for n_ints in range(100, 1000, 100):
            # create a series of repeat tests for n_ints random natural numbers
            # going up in increments of 10
            randsum = randint(n_ints, 10000)
            deviation = 1  #random()
            expected_mean = randsum / n_ints
            expected_variance = floor(deviation * expected_mean)

            # track results for each experiment repeat
            actual_variance_list = np.array([])

            # repeat test more times for smaller results of randints
            n_test_repeats = 1  #ceil(log(1000, 2) - log(n_ints, 2))

            ints = []
            for _ in range(n_test_repeats):
                # repeat
                ints = np.array(randints(n_ints,
                                         target_sum=randsum,
                                         variance=expected_variance),
                                dtype=int)
                np.append(actual_variance_list, np.var(ints))
                with self.subTest(expected_sum=randsum,
                                  ints=ints,
                                  repeats=n_test_repeats,
                                  variances=actual_variance_list):
                    # sum and mean should be the same every time
                    self.assertEqual(sum(ints), randsum)
                    self.assertAlmostEqual(np.mean(ints), expected_mean)

            # with self.subTest(expected_sum=randsum,
            #                   ints=ints,
            #                   repeats=n_test_repeats,
            #                   variances=actual_variance_list):
            #     # compare average results from repeat experiments to expected
            #     self.assertAlmostEqual(np.mean(actual_variance_list),
            #                            expected_variance, -1)

    def test_metaclass(self):
        logs_size = 32

        # make a dummy class for testing LogMethodCalls
        class Class(metaclass=LogMethodCalls, logs_size=logs_size):
            @classmethod
            def cmethod(cls):
                pass

            def imethod(self):
                pass

        cls_obj = Class()
        total_calls = 0

        for name in reversed(dir(cls_obj)):
            # go through all the attributes of the instance of Class in reverse
            # order to put magic methods last. stop when we reach a method
            # surrounded by __ since we'll assume none of the methods we created
            # are remaining.
            if name.strip("__") != name:
                # attr is a builtin
                break
            try:
                # assuming we can use attribute for name as a function, call
                # a random, consecutive number of times. since LogMethodCalls
                # merges consecutive method calls with a count, check that
                # count equals n_calls
                n_calls = randrange(1, 100)
                attr = getattr(cls_obj, name)

                for _ in range(n_calls):
                    attr()
                total_calls += n_calls
                with self.subTest(attr=name,
                                  number_of_calls=n_calls,
                                  logs=[repr(x) for x in cls_obj._logs_]):
                    # the last method to be called should have been attr
                    self.assertEqual(cls_obj._logs_[-1].name, name)
                    # length of Class.method_logs should only increase by 1
                    self.assertEqual(cls_obj._logs_[-1].calls, n_calls)
            except TypeError:
                pass

        # the total consecutive_calls should be equal to total_calls
        self.assertEqual(sum(log.calls for log in cls_obj._logs_), total_calls)

        # there are only two methods
        self.assertEqual(len(cls_obj._logs_), 2)

        for _ in range(50):
            # don't call each method consecutively to guarantee that _logs_
            # isn't merging them
            cls_obj.imethod()
            cls_obj.cmethod()

        # since more than logs_size items were added, the len of logs should
        # equal max_size
        self.assertEqual(len(cls_obj._logs_), logs_size)

    def test_metaclass_subclass_has_arg_in_constructor(self):
        class C(metaclass=LogMethodCalls):
            def __init__(self, x):
                self.x = x

        c = C(3)
        self.assertEqual(c.x, 3)  # check that args was passed to constructor

        # __init__ should be the only method
        self.assertEqual(len(c._logs_), 1)
        self.assertEqual(c._logs_[0].name, "__init__")
        self.assertEqual(c._logs_[0].calls, 1)

    def test_metaclass_edges(self):
        num_calls = 10

        @classmethod
        def cmethod(cls):
            pass

        def imethod(self):
            pass

        # subclass and instantiate LogMethodCalls with some test methods of default logs_size
        c = LogMethodCalls("C", (), {"cmethod": cmethod, "imethod": imethod})()

        for _ in range(num_calls):
            # call methods non-consecutively to guarantee they aren't merged
            c.imethod()
            c.cmethod()

        # check that only the last two method calls are saved
        self.assertEqual(len(c._logs_), 2)

        # subclass and instantiate LogMethodCalls with test methods. only the most recent
        # method call should be tracked
        c = LogMethodCalls("C", (), {
            "cmethod": cmethod,
            "imethod": imethod
        },
                           logs_size=1)()
        c.imethod()
        c.cmethod()

        # check that only the most recent method call is kept
        self.assertEqual(len(c._logs_), 1)

        # check that the most recent method call tracked is cmethod
        self.assertEqual(c._logs_[0].name, "cmethod")
        self.assertEqual(c._logs_[0].calls, 1)

        # check that consecutive method calls are merge by the number of calls

        for _ in range(num_calls):
            c.imethod()
        self.assertEqual(c._logs_[0].name, "imethod")
        self.assertEqual(c._logs_[0].calls, num_calls)

        # subclass and instantiate LogMethodCalls with test methods. not method
        # calls should be tracked.
        c = LogMethodCalls("C", (), {
            "cmethod": cmethod,
            "imethod": imethod
        },
                           logs_size=0)()

        c.imethod()
        c.cmethod()
        self.assertEqual(len(c._logs_), 0)

    def test_merge_dictionaries(self):
        expected = {"apple": 3, "banana": 0, "orange": 200}
        self.assertEqual(
            expected,
            dict(
                merge_nonsequentials_containing_ints({"apple": 3},
                                                     {"banana": 0},
                                                     {"orange": 200})))
        self.assertEqual(
            expected, merge_nonsequentials_containing_ints(expected, {}, {}))
        self.assertEqual(
            expected,
            merge_nonsequentials_containing_ints({"apple": 1}, {
                "apple": 2,
                "banana": 1
            }, {
                "orange": 2,
                "banana": -1
            }, {"orange": 198}))

    def test_merge_dictionaries_edges(self):
        expected = defaultdict()
        self.assertEqual(expected,
                         merge_nonsequentials_containing_ints({}, {}, {}))
        self.assertEqual(expected, merge_nonsequentials_containing_ints())

        with self.assertRaises(ValueError):
            merge_nonsequentials_containing_ints({"x": "y"})

    def test_merge_sequential_nonstring_data(self):
        expected = (("apple", 3), ("orange", 50), ("mango", 4))
        self.assertEqual(
            expected,
            merge_sequentials_containing_ints(
                (("apple", 1), ("apple", 2), ("orange", 50)),
                (("mango", 4), )))

    def test_merge_sequential_nonstring_data_edges(self):

        # test null case
        expected = ()
        self.assertEqual(expected, merge_sequentials_containing_ints())

        # test unique value case
        expected = (("apple", 3), ("orange", 50), ("mango", 4))
        self.assertEqual(
            expected,
            merge_sequentials_containing_ints(
                (("apple", 3), ), (("orange", 50), ), (("mango", 4), )))

    def test_merge_seq_or_non_seq_data(self):
        # these tests are identical to tests contained in
        # test_merge_dictionaries and test_merge_sequential_nonstring_data.
        expected = {"apple": 3, "banana": 0, "orange": 200}
        self.assertEqual(
            expected,
            dict(
                merge_data_containing_ints({"apple": 3}, {"banana": 0},
                                           {"orange": 200})))
        self.assertEqual(expected,
                         merge_data_containing_ints(expected, {}, {}))
        self.assertEqual(
            expected,
            merge_data_containing_ints({"apple": 1}, {
                "apple": 2,
                "banana": 1
            }, {
                "orange": 2,
                "banana": -1
            }, {"orange": 198}))

        expected = (("apple", 3), ("orange", 50), ("mango", 4))
        self.assertEqual(
            expected,
            merge_data_containing_ints(
                (("apple", 1), ("apple", 2), ("orange", 50)),
                (("mango", 4), )))
