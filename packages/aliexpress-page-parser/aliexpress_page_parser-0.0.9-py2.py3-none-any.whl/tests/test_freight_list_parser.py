# -*- coding: utf-8 -*-

# Copyright :copyright: 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

from aliexpress_page_parser.freight_list_parser import FreightListParser

import pytest

def test_parse(freight_list_result, target_freight_list):
    parser = FreightListParser(freight_list_result)
    freights = parser.parse()
    for freight in freights:
        assert freight in target_freight_list
