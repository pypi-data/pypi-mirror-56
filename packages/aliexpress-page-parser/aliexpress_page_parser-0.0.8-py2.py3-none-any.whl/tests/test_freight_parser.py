# -*- coding: utf-8 -*-

# Copyright :copyright: 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from aliexpress_page_parser.freight_parser import FreightParser

import pytest

def test_parse(freight_result, target_freight):
    parser = FreightParser(freight_result)
    assert parser.parse() == target_freight
