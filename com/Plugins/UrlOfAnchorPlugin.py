#! /usr/bin/python
# -*- coding:utf-8 -*-

from pandas import Series
import tldextract
from com.Plugins.AbstractPlugin import AbstractPlugin
from com.Common.HttpRequest import *

class UrlOfAnchorPlugin(AbstractPlugin):
    def __init__(self):
        AbstractPlugin.__init__(self, "url_of_anchor")

    def do_extract(self, simple_data):
        features = []
        for values in simple_data.values:
            total_href = 0.0
            suspicious_href = 0.0
            soup = self.get_soup(values[0])
            if soup is None:
                features.append(0)
                continue

            split_url = tldextract.extract(parse_url(values[1]).netloc)
            domin_main = split_url.domain + "." + split_url.suffix

            for tag_a in soup.findAll("a"):
                if not tag_a.has_attr("href"):
                    continue
                total_href = total_href + 1
                href_attr = tag_a["href"]
                if href_attr.startswith("#"):
                    suspicious_href = suspicious_href + 1
                elif href_attr.startswith("javascript"):
                    suspicious_href = suspicious_href + 1
                elif href_attr.startswith("http"):
                    if domin_main not in href_attr:
                        suspicious_href = suspicious_href + 1

            if total_href == 0:
                features.append(0)
            elif (suspicious_href/total_href) <= 0.31:
                features.append(0)
            elif (suspicious_href/total_href) >= 0.31 and (suspicious_href/total_href) < 0.67:
                features.append(1)
                print "[Suspicious]score :%s %s" %(suspicious_href/total_href, domin_main)
            else:
                features.append(2)
                print "[Phishing]score :%s %s" %(suspicious_href/total_href, domin_main)

        return Series(features)