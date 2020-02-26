# -*- coding: utf-8 -*-

import requests
import base64
import json
import yaml


def get_vmess(url):
    """
    获取vmess订阅
    :param url:
    :return:
    """
    r = requests.get(url)
    vmess_list = base64.b64decode(r.text).decode().split("vmess://")
    vmess_list = map(lambda x: base64.b64decode(x + "==").decode(), vmess_list)
    vmess_list = filter(len, vmess_list)
    vmess_list = map(json.loads, vmess_list)
    vmess_list = map(vmess_sub_to_clash, vmess_list)
    return remove_vmess_node(vmess_list, "特殊")


def vmess_sub_to_clash(d):
    """
    将vmess订阅结果转换成clash的proxy格式
    :param d:
    :return:
    """
    new_d = {
        "name": d["ps"],
        "type": "vmess",
        "server": d["add"],
        "port": d["port"],
        "uuid": d["id"],
        "alterId": 2,
        "cipher": "auto",
        "tls": True
    }
    return new_d


def remove_vmess_node(vmess_list, keyword):
    """
    将指定的关键字节点从节点列表中移除
    :param vmess_list:
    :param keyword:
    :return:
    """
    new_vmess_list = []
    for n in vmess_list:
        if keyword in n["name"]:
            continue
        new_vmess_list.append(n)
    return new_vmess_list


def get_rule():
    """
    get remote rule, and set it to global variable
    :return:
    """
    global config
    global rule
    with open("./clash_my_rule.yml") as f:
        my_rule = yaml.safe_load(f)
    r = requests.get(config.rule_url)
    rule = yaml.safe_load(r.text)
    rule = my_rule + rule

    return rule


class Config:
    def __init__(self, rule_url):
        self.rule_url = rule_url


config = Config(rule_url="https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Rule.yml")
rule = []
proxy_group = []

if __name__ == '__main__':
    # 将vmess订阅链接当作参数传递进来
    vmess_url = ""

    # 解析订阅成proxy group（排除掉一些自己不喜欢的节点）
    proxies = get_vmess(vmess_url)
    for proxy in proxies:
        print(proxy)

    # 读取lhie1规则，加上自己的规则

    # 接口返回完整的clash文件

    # rule = get_rule()
