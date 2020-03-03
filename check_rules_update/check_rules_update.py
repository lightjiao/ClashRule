# -*- coding: utf-8 -*-

import requests
import datetime


def check_rules_commit():
    """
    检查 lhie1 的rules 是否有最近的commit，如果有，则 exit(-1)
    利用 exit(233) 白嫖 github 的notification
    :return:
    """
    # 一天前
    # format YYYY-MM-DDTHH:MM:SSZ
    since = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    commit_url = "https://api.github.com/repos/lhie1/Rules/commits?path=/Clash/Rule.yml&since={}".format(since)
    print(commit_url)
    r = requests.get(commit_url)
    print(r.json())
    if len(r.json()) > 0:
        exit(233)


if __name__ == '__main__':
    check_rules_commit()
