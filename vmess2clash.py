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
    vmess_content = r.text
    if not vmess_content.endswith("=="):
        vmess_content += "=="

    vmess_list = base64.b64decode(vmess_content).decode().split("vmess://")
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


def generate_proxy_groups(proxy_groups: list, proxies: list) -> list:
    """
  - 🇭🇰 香港节点
  - 🇨🇳 台湾节点
  - 🇸🇬 新加坡节点
  - 🇯🇵 日本节点
  - 🇺🇲 美国节点
  - 🚀 手动切换
    :param proxy_groups:
    :param proxies:
    :return:
    """
    um = []
    jp = []
    sg = []
    cn = []
    hk = []
    for n in proxies:
        if "美国" in n["name"]:
            um.append(n["name"])
        elif "日本" in n["name"]:
            jp.append(n["name"])
        elif "新加坡" in n["name"]:
            sg.append(n["name"])
        elif "台湾" in n["name"]:
            cn.append(n["name"])
        elif "香港" in n["name"]:
            hk.append(n["name"])

    for idx, value in enumerate(proxy_groups):
        if value["name"] == "🇭🇰 香港节点":
            proxy_groups[idx]["proxies"] = hk
        if value["name"] == "🇨🇳 台湾节点":
            proxy_groups[idx]["proxies"] = cn
        if value["name"] == "🇸🇬 新加坡节点":
            proxy_groups[idx]["proxies"] = sg
        if value["name"] == "🇯🇵 日本节点":
            proxy_groups[idx]["proxies"] = jp
        if value["name"] == "🇺🇲 美国节点":
            proxy_groups[idx]["proxies"] = um
        if value["name"] == "🚀 手动切换":
            proxy_groups[idx]["proxies"] = [n["name"] for n in proxies]

    return proxy_groups


def get_rule():
    """
    get remote rule, and set it to global variable
    :return:
    """
    global config
    with open("config/clash-my-rule.yml") as f:
        my_rule = yaml.safe_load(f)
    r = requests.get(config.rule_url)
    rule = yaml.safe_load(r.text)
    rule = my_rule + rule

    return rule


def get_clash_sub(vmess_url):
    """
    :param vmess_url:
    :return:
    """
    # 解析订阅成proxy group（排除掉一些自己不喜欢的节点）
    proxies = get_vmess(vmess_url)
    with open("config/clash-proxy-group.yml", encoding='UTF-8') as f:
        proxy_groups = yaml.safe_load(f)
    proxy_groups = generate_proxy_groups(proxy_groups, proxies)

    # 读取lhie1规则，加上自己的规则
    rule = get_rule()

    with open("config/clash-config-template.yml", encoding="utf-8") as f:
        template = yaml.safe_load(f)

    # 接口返回完整的clash文件
    template["Proxy"] = proxies
    template["Proxy Group"] = proxy_groups
    template["Rule"] = rule

    return yaml.dump(template, sort_keys=False)


class Config:
    def __init__(self, rule_url):
        self.rule_url = rule_url


config = Config(rule_url="https://raw.githubusercontent.com/lhie1/Rules/master/Clash/Rule.yml")

if __name__ == '__main__':
    # 将vmess订阅链接当作参数传递进来
    vmess_url = ""
    get_clash_sub(vmess_url)
