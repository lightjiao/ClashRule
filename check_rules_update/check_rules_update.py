# -*- coding: utf-8 -*-

import requests
import datetime


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_rules_commit():
    """
    检查 lhie1 的rules 是否有最近的commit，如果有，则 exit(-1)
    利用 exit(233) 白嫖 github 的notification
    :return:
    """
    # 一天前
    # format YYYY-MM-DDTHH:MM:SSZ
    since = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
    commit_url = "https://api.github.com/repos/lhie1/Rules/commits?path=/Clash/Rule.yaml&since={}".format(since)
    print(commit_url)
    r = requests.get(commit_url)
    print(r.text)

    if len(r.json()) > 0:
        print(f"{bcolors.OKGREEN}See repo commit: https://github.com/lhie1/Rules/commits/master/Clash/Rule.yaml{bcolors.ENDC}")
        exit(233)


if __name__ == '__main__':
    check_rules_commit()
