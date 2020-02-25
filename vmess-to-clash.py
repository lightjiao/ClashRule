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
    l = base64.b64decode(r.text).decode().split("vmess://")
    l = map(lambda x: base64.b64decode(x + "==").decode(), l)
    l = filter(len, l)
    l = map(json.loads, l)
    l = map(vmess_sub_to_clash, l)
    for n in l:
        print(n)


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


def read_rule_from_file(file_name):
    blockRuleDict = {}
    with open(file_name) as f:
        for line in f:
            line = line.replace(" ", "")
            line = line.strip('\n')
            line = line.strip('-')
            line = line.strip(',')
            d = line.split(',')
            if len(d) < 2:
                continue
            if d[0] not in blockRuleDict:
                blockRuleDict[d[0]] = []
            blockRuleDict[d[0]].append(d[1])
    return blockRuleDict


def merge_rules(*rules):
    result_rule_dict = {}
    for rule in rules:
        for k, l in rule.items():
            if k not in result_rule_dict:
                result_rule_dict[k] = []
            result_rule_dict[k] += l

            # unique and sort result
            result_rule_dict[k] = list(set(result_rule_dict[k]))
            result_rule_dict[k] = sorted(result_rule_dict[k])

    return result_rule_dict


def merge_block_rule():
    defaultProxyGroup = "🛑 Block"

    rule_1 = read_rule_from_file("./miaopasi_block_rule.yml")
    rule_2 = read_rule_from_file("./dlercloud_block.yml")

    rule = merge_rules(rule_1, rule_2)
    for k, l in rule.items():
        for n in l:
            one_rule = " - " + k + "," + n + "," + defaultProxyGroup
            if k == "IP-CIDR":
                one_rule += "," + "no-resolve"
            print(one_rule)


def merge_white_list_rule():
    defaultProxyGroup = "🦄 WhiteList"

    rule_1 = read_rule_from_file("./whitelist_rule.yml")
    # rule_2 = read_rule_from_file("./dlercloud_block.yml")

    rule = merge_rules(rule_1)
    for k, l in rule.items():
        for n in l:
            one_rule = " - " + k + "," + n + "," + defaultProxyGroup
            if k == "IP-CIDR":
                one_rule += "," + "no-resolve"
            print(one_rule)


def generate_config_file():
    whitelist_rule = []
    with open("./whitelist_rule.yml") as f:
        whitelist_rule = yaml.safe_load(f)

    block_rule = []
    with open("./block_rule.yml") as f:
        block_rule = yaml.safe_load(f)

    last_rule = ["GEOIP,CN,DIRECT", "MATCH,🌐 默认代理"]

    config_content = {}
    with open(".scripts/clashConfig.yml") as f:
        config_content = yaml.safe_load(f)
        config_content["Rule"] = whitelist_rule + block_rule

    # 生成写入文件
    with open("./resul.yml", "w") as f:
        yaml.dump(config_content, f, default_flow_style=False, allow_unicode=True)


if __name__ == '__main__':
    # 下载lhie1的规则文件与仓库中存储的文件对比差异，没有差异直接结束流水线
    # 对比差异超过50% 则发出邮件告警，并且直接结束流水线
    # 在本地仓库提交下载好的lhie1规则
    # 合并我的规则与lhie1规则（我的规则在前，lhie1的规则在后）

    # 获取vmess订阅并对比，订阅没有变化直接结束流水线 todo: 如何对比, 规则或者订阅有一个有变化就需要更新订阅
    # 解析vmess订阅并分策略组
    # 生成策略组

    # 合并模板、订阅、策略组、规则，生成clash的订阅文件
    # 提交生成的文件到私有仓库目录
    # 发邮件提醒，说订阅有变化
