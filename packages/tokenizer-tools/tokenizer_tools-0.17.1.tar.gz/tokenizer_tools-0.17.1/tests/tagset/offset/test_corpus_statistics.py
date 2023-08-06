from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.corpus_statistics import CorpusStatistics
import pytest


@pytest.mark.skip(reason="not implemented yet")
def test_create_from_corpus(datadir):
    corpus = Corpus.read_from_file(datadir / "data.conllx")

    corpus_statistics = CorpusStatistics.create_from_corpus(corpus)

    expected = CorpusStatistics(
        domain=None,
        function=None,
        sub_function=None,
        intent=None,
        entity_types=None,
        entity_values=None,
    )

    assert corpus_statistics == expected
