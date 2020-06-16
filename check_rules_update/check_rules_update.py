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
    # 七天前
    # format YYYY-MM-DDTHH:MM:SSZ
    since = (datetime.datetime.now() - datetime.timedelta(days=7)
             ).strftime("%Y-%m-%dT%H:%M:%SZ")
    requests_params = {
        "sha": "master",
        "path": "/Clash/Rule.yaml",
        "since": since
    }

    github_commit_api = "https://api.github.com/repos/lhie1/Rules/commits"
    response = requests.get(url=github_commit_api, params=requests_params)
    print(response.url)
    print(response.text)

    if len(response.json()) > 0:
        print(f"{bcolors.OKGREEN}See repo commit: {response.url}{bcolors.ENDC}")
        exit(233)


if __name__ == '__main__':
    check_rules_commit()
