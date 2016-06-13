#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Alfred WorkFlow - SubHD.com Hot Films
# author:JeffMa
# url: http://devework.com/

import os
import urllib2
import sys
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

reload(sys)
sys.setdefaultencoding('utf-8')


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key in ('arg',):
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)


def get_film_info():
    items = []
    target_url = 'http://www.dy2018.com/'
    content = urllib2.urlopen(target_url).read()
    content = unicode(content,'GBK').encode('utf-8')
    only_hotl_tags = SoupStrainer(class_='co_content222')
    soup = BeautifulSoup(content, "html.parser", parse_only=only_hotl_tags)
    i = 0
    for link in soup.find_all('li', limit=15):

        link_url = target_url + link.findChildren('a')[0].get('href')

        link_title = link.findChildren('a')[0].get('title')[5:]
        # link_title = link.findChildren('a')[0].get('title')[5:]

        link_time = link.findChildren('span')[0].string

        json_item = dict(title=link_title, subtitle='日期: '+link_time, arg=link_url, icon='icon.png')
        items.append(json_item)
        i = i + 1

    return generate_xml(items)

# print get_film_info()
