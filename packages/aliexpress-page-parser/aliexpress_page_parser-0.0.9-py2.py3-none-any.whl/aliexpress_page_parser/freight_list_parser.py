# -*- coding: utf-8 -*-

# Copyright :copyright: 2019 by IBPort. All rights reserved.
# @Author: Neal Wong
# @Email: ibprnd@gmail.com

import json


class FreightListParser(object):
    def __init__(self, text):
        self.text = text

    def parse(self):
        freights = []
        d = dict()
        info = json.loads(self.text)

        freight_result = info.get('body', d).get('freightResult', d)
        if not isinstance(freight_result, list):
            freight_result = [freight_result]

        for freight_info in freight_result:
            try:
                commit_day = int(freight_info.get('commitDay', '0'))
            except:
                commit_day = 0
            shipping_fee = freight_info.get('freightAmount', d).get('value', 0)

            freights.append({
                'company': freight_info.get('company', ''),
                'service_name': freight_info.get('serviceName', ''),
                'amount': shipping_fee,
                'currency': freight_info.get('currency', 'USD'),
                'tracking': freight_info.get('tracking', False),
                'commit_day': commit_day,
                'time': freight_info.get('time', ''),
                'send_goods_country': freight_info.get('sendGoodsCountry', '')
            })

        return freights
