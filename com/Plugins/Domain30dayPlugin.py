#! /usr/bin/python
# -*- coding:utf-8 -*-

from pandas import Series
from com.Plugins.AbstractPlugin import AbstractPlugin
import re
import time
from com.Common.HttpRequest import *


class Domain30dayPlugin(AbstractPlugin):
    def __init__(self):
        AbstractPlugin.__init__(self, "domain_30day")

    def do_extract(self, simple_data):
        features = []
        for url in simple_data:
            url_info = parse_url(url)
            domain = url_info.netloc
            while True:
                content = read_html('https://www.whois.com/whois/' + domain)
                if not content:
                    print('[%s] read_html() err, try... ' % self.feature_name)
                    continue
                try:
                    partten = '(?<=Registration Date:\<\/div\>\<div class\=\"df\-value\">)' \
                              '(\d{4}-\d{1,2}-\d{1,2})(?=\<\/div>)'
                    str_reg_date = re.search(partten, content).group()
                except Exception, e:
                    print('[%s] No Registration Data. %s' % (self.feature_name, domain))

                list_tmp = str_reg_date.split('-')
                reg_timestamp = time.mktime((int(list_tmp[0]), int(list_tmp[1]), int(list_tmp[2]), 0, 0, 0, 0, 0, 0))
                # print (reg_date.
                if (time.time()-reg_timestamp) < 30*86400:
                    # < 30day
                    features.append(1)
                else:
                    features.append(0)
                break

        return Series(features)
