#!/usr/bin/python3
import argparse
import json
import os
import sys
import time
import requests

from jinja2 import Template

CURRENT_VERSION = "0.0.2-20230912"
GITHUB_NAMESPACE = "yifengyou"
REPOS = None
TOKEN_FILE = "/etc/yifengyou"

CONTENT = """

<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
</head>
<div align="center">
    <div style="width: fit-content; margin-left: auto; margin-right: auto;">
    <img src="https://github-readme-stats.vercel.app/api?username=yifengyou&theme=default&hide_border=true&show_icons=true&hide_title=true" width="49%" />
    <img src="https://github-readme-streak-stats.herokuapp.com/?user=yifengyou&theme=default&hide_border=true" alt="Streak Stats" width="49%" />
    </div>
    <img src="https://user-images.githubusercontent.com/19882390/203891125-3d50010e-dc87-45a9-a53c-d53ff21c3e4b.png" width="25%"  alt="微信" title="微信"/>
    <img src="https://user-images.githubusercontent.com/19882390/203893616-72e4b570-2628-4067-980b-a73aab253c7b.png" width="25%"  alt="钉钉" title="钉钉"/>
    <br><br>
    <strong>技术方向：操作系统、内核、虚拟化、云原生 :blush: 欢迎交流~ :blush: </strong>
    <br><br>
    <a href="https://github.com/yifengyou">
      <img src="https://badges.strrl.dev/visits/yifengyou/yifengyou?style=flat-square&color=black&logo=github">
    </a>
    <a href="https://github.com/yifengyou">
      <img src="https://badges.strrl.dev/years/yifengyou?style=flat-square&color=black&logo=github">
    </a>
    <a href="https://github.com/yifengyou?tab=repositories">
      <img src="https://badges.strrl.dev/repos/yifengyou?style=flat-square&color=black&logo=github">
    </a>
    <a href="https://github.com/yifengyou">
      <img src="https://badges.strrl.dev/commits/monthly/yifengyou?style=flat-square&color=black&logo=github">
    </a>
</div>

**环境/工具**

<div align="center">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/linux/linux.png" alt="Linux" title="Linux">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/docker/docker.png" alt="Docker" title="Docker">
<img height="50" src="https://raw.githubusercontent.com/github/explore/01ea2a586e5da744792d0ccfce2f68b861f29301/topics/kubernetes/kubernetes.png" alt="Kubernetes" title="Kubernetes">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/android/android.png" alt="Android" title="Android">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/vim/vim.png" alt="Vim" title="Vim">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/atom/atom.png" alt="Atom" title="Atom">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/git/git.png" alt="Git" title="Git">
<img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/markdown/markdown.png" alt="Markdown" title="Markdown">
</div>


"""


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"All done! {func.__name__} took {elapsed} seconds")
        return result

    return wrapper


def check_python_version():
    current_python = sys.version_info[0]
    if current_python == 3:
        return
    else:
        raise Exception('Invalid python version requested: %d' % current_python)


def get_repos_data(filepath="repos.json"):
    global REPOS
    with open(filepath, "r") as repos_file:
        REPOS = json.loads(repos_file.read())


def get_github_repo_info(repo, namespace=GITHUB_NAMESPACE):
    """
    {
        "message":"API rate limit exceeded for 147.182.238.250. (But here's the good news:
            Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
        "documentation_url":"https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
    }
    """
    url = "https://api.github.com/repos/%s/%s" % (namespace, repo)
    print(f"call api {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json"
    }
    if os.path.exists(TOKEN_FILE) and os.path.isfile(TOKEN_FILE):
        # with open(TOKEN_FILE, 'r') as f:
        #     headers["Authorization"] = "yifengyou %s" % f.read().strip()
        print(f"get token from {TOKEN_FILE}")
    print("")
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        description = data.get("description")
        return description
    else:
        print("请求失败，状态码为：" + str(response.status_code))
        return ""


def scrapy_repo_info(REPOS):
    for reponame, repoinfo in REPOS.items():
        repoinfo["description"] = get_github_repo_info(reponame)
        print(f"{reponame} description:{repoinfo['description']}")


@timer
def handle_scrapy_githubinfo(args):
    try:
        get_repos_data(args.filepath)
    except Exception as e:
        print("load repos.json failed!", str(e))
        exit(1)

    scrapy_repo_info(REPOS)

    with open(args.output, 'w') as output_file:
        json.dump(REPOS, output_file, ensure_ascii=False, indent=4)

    for repo_name, repo_info in REPOS.items():
        print(f"# {repo_name}")
        for key, value in repo_info.items():
            print(f"    '{key}' : '{value}'")


@timer
def handle_generate_profile(args):
    with open(args.filepath, "r") as repos_file:
        repo_data = json.loads(repos_file.read())

    data = {
        "eBPF": {},
        "kernel": {},
        "userspace": {},
        "virtualization": {},
        "cloudnative": {},
        "programmer": {},
        "diy": [],
        "code": [],
        "book": [],
        "all": [],
    }
    """
        data = {
        "eBPF": {
            "构建": [PERINFO],
            "配置": [PERINFO],
            "扩展": [PERINFO],
            "书籍": [PERINFO],
            ...
        },
        "kernel": {
            "构建": [PERINFO],
            "配置": [PERINFO],
            "扩展": [PERINFO],
            "书籍": [PERINFO],
            ...
        },
        "userspace": {
            "构建": [PERINFO],
            "配置": [PERINFO],
            "扩展": [PERINFO],
            "书籍": [PERINFO],
            ...
        },
        "all": [PERINFO]
    }
    """

    for key, value in repo_data.items():
        dir = value["direction"]
        type = value["type"]
        value["prj"] = key

        if 'diy' in value and value['diy'] == 1:
            value["label"] = "自研"
        elif 'code' in value and value['code'] == 1:
            value["label"] = "应用、解析"
        elif 'type' in value and value['type'] == "书籍":
            value["label"] = "书籍"
        elif 'type' in value and value['type'] == "笔记":
            value["label"] = "笔记"

        if dir == "eBPF":
            if type not in data["eBPF"]:
                data["eBPF"][type] = []
            data["eBPF"][type].append(value)
        elif dir == "内核态":
            if type not in data["kernel"]:
                data["kernel"][type] = []
            data["kernel"][type].append(value)
        elif dir == "用户态":
            if type not in data["userspace"]:
                data["userspace"][type] = []
            data["userspace"][type].append(value)
        elif dir == "虚拟化":
            if type not in data["virtualization"]:
                data["virtualization"][type] = []
            data["virtualization"][type].append(value)
        elif dir == "云原生":
            if type not in data["cloudnative"]:
                data["cloudnative"][type] = []
            data["cloudnative"][type].append(value)
        elif dir == "编程语言":
            if type not in data["programmer"]:
                data["programmer"][type] = []
            data["programmer"][type].append(value)

        data["all"].append(value)

    template = """
**eBPF**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["eBPF"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> {{type_name}} </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
            <img alt="Progressing" src="https://img.shields.io/badge/{{info["label"]}}-d00000"/>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>

**内核态**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["kernel"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> {{type_name}} </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
            <img alt="Progressing" src="https://img.shields.io/badge/{{info["label"]}}-d00000"/>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>

**用户态**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["userspace"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> {{type_name}} </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
            <img alt="Progressing" src="https://img.shields.io/badge/{{info["label"]}}-d00000"/>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>

**虚拟化**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["virtualization"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> {{type_name}} </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
            <img alt="Progressing" src="https://img.shields.io/badge/{{info["label"]}}-d00000"/>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>

**云原生**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["cloudnative"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> {{type_name}} </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
            <img alt="Progressing" src="https://img.shields.io/badge/{{info["label"]}}-d00000"/>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>

**编程语言**

<table class="table table-striped table-bordered table-vcenter" align="center">
  <tbody>
    <tr>
      <th> 类别<br/>Type </th>
      <th> 项目名<br/>ProjName </th>
      <th> 描述<br/>Description </th>
      <th> 赞<br/>Stars </th>
      <th> 进度<br/>Progressing </th>
    </tr>
    {%- for type_name,typeinfo_list in data["programmer"].items() %}
    {%- for info  in typeinfo_list %}
    <tr>
        <td> 
            <img height="50" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/{{info["prj"]}}/{{info["prj"]}}.png" alt="{{info["prj"]}}" title="{{info["prj"]}}"> 
        </td>
        <td align="center">
            <a href="https://github.com/yifengyou/{{info["prj"]}}" target="_blank"> {{info["prj"]}} </a>
        </td>
        <td> {{info["description"]}} </td>
        <td><img alt="Stars" src="https://img.shields.io/github/stars/yifengyou/{{info["prj"]}}?style=flat"/></td>
        <td><img alt="Progressing" src="https://img.shields.io/badge/{{info["progress"]}}%25-green&logo=github"/></td>
    </tr>
    {%- endfor %}
    {%- endfor %}
  </tbody>
</table>



"""

    template = Template(template)
    table_code = template.render(data=data)

    with open(args.output, 'w') as f:
        f.write(CONTENT + table_code)
    print(f" write to {args.output} done!")


def main():
    check_python_version()

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-v", "--version", action="store_true",
                        help="show program's version number and exit")
    parser.add_argument("-h", "--help", action="store_true",
                        help="show this help message and exit")

    subparsers = parser.add_subparsers()

    # 全局命令
    parent_parser = argparse.ArgumentParser(add_help=False, description="generate github profile")
    parent_parser.add_argument("-V", "--verbose", default=None, action="store_true", help="show verbose output")

    # 添加子命令 scrapy
    parser_scrapy = subparsers.add_parser('scrapy', parents=[parent_parser])
    parser_scrapy.add_argument('-f', '--filepath', default="repos.json", help="repos json to load")
    parser_scrapy.add_argument('-o', '--output', default="format.json", help="output json filepath")
    parser_scrapy.set_defaults(func=handle_scrapy_githubinfo)

    # 添加子命令 generate
    parser_generate = subparsers.add_parser('generate', parents=[parent_parser])
    parser_generate.add_argument('-f', '--filepath', default="format.json", help="repos json to load")
    parser_generate.add_argument('-o', '--output', default="yifengyou.html", help="output json filepath")
    parser_generate.set_defaults(func=handle_generate_profile)

    args = parser.parse_args()
    if args.version:
        print("GitHub profile generation %s" % CURRENT_VERSION)
        sys.exit(0)
    elif args.help or len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    else:
        args.func(args)


if __name__ == "__main__":
    main()
