#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
test_onemillion
----------------------------------

Tests for `onemillion` module.
"""

import pytest

import onemillion


@pytest.fixture
def onemillion_instance():
    onemillion_instance = onemillion.OneMillion()
    return onemillion_instance


def test_get_current_etag(onemillion_instance):
    """See if we have access to the datasets."""
    for dataset in onemillion_instance.CONFIG['domain_lists']:
        etag = onemillion_instance.get_current_etag(dataset['url'])
        assert(etag is not None)


def test_onemillion_object(onemillion_instance):
    """Test an instance of the onemillion class."""
    onemillion_instance.update_lists()

    # test the rank of 'google.com'
    rank = onemillion_instance.domain_in_million('google.com')
    assert(isinstance(rank, int))
    assert(rank <= 5)

    # test the rank of 'gaagle.com'
    rank = onemillion_instance.domain_in_million('gaagle.com')
    assert(rank is None)
