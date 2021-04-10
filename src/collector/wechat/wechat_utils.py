#!/usr/bin/env python
"""
    Created by howie.hu at 2021/4/9.
    Description：微信相关通用函数
    Changelog: all notable changes to this file will be documented
"""

from ruia import Request

from src.config import Config
from src.databases import MongodbManager


async def get_wf_url():
    """
    获取 wechat-feeds 资源链接
    Github: https://github.com/hellodword/wechat-feeds
    :return:
    """
    url = "https://wechat.privacyhide.com/VERSION?"
    resp = await Request(url=url).fetch()
    version = str(await resp.text()).strip()
    return f"https://cdn.jsdelivr.net/gh/hellodword/wechat-feeds@{version}/details.json"


def wechat2url(name_list: list):
    """
    将微信名称转为 wechat-feeds 对应的url
    :param name_list:
    :return:
    """
    mongo_base = MongodbManager.get_mongo_base(mongodb_config=Config.MONGODB_CONFIG)
    coll = mongo_base.get_collection(coll_name="2c_wechat_name")
    _rss_tem = "https://gitee.com/BlogZ/wechat-feeds/raw/feeds/{0}.xml"
    res_dict = {}
    for each in coll.find({"name": {"$in": name_list}}):
        rss_url = _rss_tem.format(each["bizid"])
        res_dict[each["name"]] = rss_url
    return res_dict


if __name__ == "__main__":
    wechat2url(Config.WECHAT_LIST)