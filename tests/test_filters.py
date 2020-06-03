import pytest

from processing.filters import LabelFilter

from tests.mock_objects import tass_info  # info needed it
from tests.mock_objects import covid_filter, not_covid_disease_filter, economic_filter
from tests.mock_objects import covid_info_in_subjects_only, vaccination_rabies_info, achs_virus_info, economic_info


def test_filter(covid_filter, economic_info, covid_info_in_subjects_only):
    assert covid_filter(economic_info) is False
    assert covid_filter(covid_info_in_subjects_only) is True


def test_filter_conjunction(covid_filter, not_covid_disease_filter,
                            achs_virus_info, covid_info_in_subjects_only):
    filter = covid_filter & not_covid_disease_filter
    assert filter(achs_virus_info) is True
    assert filter(covid_info_in_subjects_only) is False


def test_filter_disjunction(covid_filter, economic_filter, economic_info, covid_info_in_subjects_only, achs_virus_info):
    filter = covid_filter | economic_filter
    assert filter(covid_info_in_subjects_only) is True
    assert filter(economic_info) is True
    assert filter(achs_virus_info) is True


def test_filter_negation(covid_filter, economic_info, covid_info_in_subjects_only):
    filter = ~covid_filter
    assert filter(economic_info) is True
    assert filter(covid_info_in_subjects_only) is False


def test_filter_representation():
    empty_filter = LabelFilter(labels=[])
    one_word_filter = LabelFilter(labels=['word'])
    two_word_filter = LabelFilter(labels=['apple', 'orange'])
    a_lot_of_word_filter = LabelFilter(labels=['one', 'two', 'three'])
    aliased_filter = LabelFilter(labels=['COVID', 'coronavirus'], alias='CovidFilter')

    assert repr(empty_filter) == 'LabelFilter()'
    assert repr(one_word_filter) == 'LabelFilter(word)'
    assert repr(two_word_filter) == 'LabelFilter(apple, orange)'
    assert repr(a_lot_of_word_filter) == 'LabelFilter(one, two...)'
    assert repr(aliased_filter) == 'CovidFilter'


if __name__ == '__main__':
    pytest.main(['test_filters.py'])