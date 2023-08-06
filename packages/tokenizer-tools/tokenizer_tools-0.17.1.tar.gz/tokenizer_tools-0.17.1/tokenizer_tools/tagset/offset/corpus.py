from typing import Union, List, Tuple

import numpy as np
from sklearn.model_selection import train_test_split

from tokenizer_tools.conllz.reader import read_conllx
from tokenizer_tools.conllz.writer import write_conllx
from tokenizer_tools.converter.conllz_to_offset import conllz_to_offset
from tokenizer_tools.converter.offset_to_sentence import offset_to_sentence
from tokenizer_tools.tagset.offset.corpus_statistics import CorpusStatistics
from tokenizer_tools.tagset.offset.document import Document


class Corpus(List[Document]):
    """
    This Corpus means a single corpus object.
     single corpus file can stored in single file (implemented already)
      or multiple files (not implemented yet).

    a single corpus object contains any number of example. example is the basic unit for model training/evaluate/test.

    The corpus object is a list-like object. it has all the methods and attributes a list should have.
     the only constraint is that the basic element/item in this list container is example.

    TODO: also it should have same behavior (see https://docs.python.org/3.6/library/stdtypes.html#set) with set type:
        isdisjoint, issubset, issuperset, union, intersection, difference, symmetric_difference
    """

    @classmethod
    def read_from_file(cls, data_file):
        with open(data_file, "rt") as fd:
            sentence_list = read_conllx(fd)

        offset_data_list = []
        for sentence in sentence_list:
            offset_data, result = conllz_to_offset(sentence)

            offset_data_list.append(offset_data)

        return Corpus(offset_data_list)

    def write_to_file(self, output_file):
        sentence_list = [offset_to_sentence(offset) for offset in self]

        with open(output_file, "wt") as fd:
            write_conllx(sentence_list, fd)

    def train_test_split(self, **kwargs) -> Tuple["Corpus", "Corpus"]:
        """
        split corpus into train set and test set
        :param kwargs: kwargs passed directly to sklearn.model_selection.train_test_split
        :return: train_corpus, test_corpus
        """
        train_set, test_set = train_test_split(self, **kwargs)

        return Corpus(train_set), Corpus(test_set)

    def __hash__(self):
        return hash(frozenset(self))

    def __eq__(self, other):
        return frozenset(self) == frozenset(other)

    def __getitem__(self, item) -> Union[Document, "Corpus"]:
        if isinstance(item, (np.ndarray, list)):
            subset = []
            for i in item:
                subset.append(self[i])

            return self.__class__(subset)
        else:
            return super().__getitem__(item)

    def isdisjoint(self, other):
        pass

    def issubset(self, other):
        pass

    def issuperset(self, other):
        pass

    def union(self, *others):
        pass

    def intersection(self, *others):
        pass

    def difference(self, *others):
        pass

    def symmetric_difference(self, other):
        pass

    def remove_duplicate(self) -> "Corpus":
        set_corpus = set(self)
        duplicate_free_corpus = self.__class__(set_corpus)
        return duplicate_free_corpus

    def generate_statistics(self) -> CorpusStatistics:
        return CorpusStatistics.create_from_corpus(self)
