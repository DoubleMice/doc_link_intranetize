# -*- coding: UTF-8 -*-
# /usr/local/bin/python

import re
import os
import time
import requests
import logging

#CONFIG####################################################################################CONFIG
## 工作目录
ROOT_DIR = os.getcwd()
## 文件本地化存储目录
FIX_DIR = "auto_fix_dir" 
## GIT API
GIT_REPO_BASE = "*********/api/v4/projects"
HEADERS = {"PRIVATE-TOKEN":"************"}
## 获取所有仓库信息
# REPO_POOL = requests.get(GIT_REPO_BASE,headers=HEADERS).json()
REPO_POOL = []    
REPO_IGNORE = []
GIT_CLONE = "git clone "
GIT_COMMIT = "git commit -am "
GIT_PULL = "git pull"
COMMIT_MSG = "外链修复"
GIT_PUSH = "git push"
GIT_ADD = "git add ."
GIT_FETCH = "git fetch"
ID_START = 20
ID_END = 100

def get_repo_info():
    logger.info("-------------获取仓库列表-----------")
    for id in range(ID_START,ID_END):
        git_url = GIT_REPO_BASE + "/" +str(id)
        r = requests.get(git_url,headers=HEADERS)
        if (r.status_code == 200) and (r.json()["default_branch"]!= None) and (r.json()["name"] not in REPO_IGNORE):
            REPO_POOL.append(r.json())
            logger.info("get repo " + r.json()["name"] + " git addr")
        else:
            logger.warn("invalid or skip repo id:" + str(id))
    logger.info("-------------获取仓库列表完成-----------")
## 日志文件
LOG_FILE = ROOT_DIR + "/" + time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))  + ".log" 
## 需修复的文件类型
FILE_TYPE_POOL = ["c","cpp","pdf","py","asm","txt"]
PIC_TYPE_POOL = ["png","jpg","jpeg"]
## 指定文档类型
BUG_TYPE_POOL = ["md"]
## 日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
logfile = LOG_FILE
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
ch.setFormatter(formatter)
logger.addHandler(ch)
## 匹配规则
file_type = ""  #外链文件后缀
pic_type = ""   #外链图片后缀
bug_type = ""   #需修复的文档后缀
for postfix in FILE_TYPE_POOL:
    file_type += postfix
    if postfix!=FILE_TYPE_POOL[-1]:
        file_type += "|"
for postfix in PIC_TYPE_POOL:
    pic_type += postfix
    if postfix!=PIC_TYPE_POOL[-1]:
        pic_type += "|"
for postfix in BUG_TYPE_POOL:
    bug_type += postfix
    if postfix!=BUG_TYPE_POOL[-1]:
        bug_type += "|"
## markdown中引用文件的正则匹配
file_rule = "(?<!!)\[[^\]]*?\]\((?:[a-zA-z]+://[^\s]*?|www\.[^\s]*?)\.(?:" + file_type + ")\)" 
print file_rule
sub_file_rule = "\[(.*)\]\((.*)\.(" + file_type + ")\)"
sub_file_pattern = re.compile(sub_file_rule)

## markdown中网址的正则匹配
site_rule = "(?<!!)\[[^\]]*?\]\((?:[a-zA-z]+://[^\s]*?|www\.[^\s]*?)\)"
sub_site_rule = "\[(.*)\]\((.*)\)"
sub_site_pattern = re.compile(sub_site_rule)

## markdown中图片引用的正则匹配
pic_rule = "!\[.*\]\([a-zA-Z]+://[^\s]*\w+[" + pic_type + "]\)|!\[.*\]\(www\.[^\s]*\w+[" + pic_type + "]\)"
sub_pic_rule = "!\[(.*)\]\((.*)\.(" + pic_type + ")\)"
sub_pic_pattern = re.compile(sub_pic_rule)

## 需要修复的文档正则匹配
bug_rule = "[^\s]*\.(" + bug_type + ")"


#CONFIG####################################################################################CONFIG


file_flag,pic_flag,site_flag = False,False,False


def file_parent_dir_miss_handle(file_path):
    parent_dir,file_name = os.path.split(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

def name_escape(filename):
    return filename.replace(" ","_")

# 识别文件后缀是否在指定修复后缀中
def recognize_bug_file(filename):
    pattern =re.compile(bug_rule)
    bug_result = re.findall(pattern,filename)
    for postfix in bug_result:
        for candidate in BUG_TYPE_POOL:
            if postfix == candidate:
                return True
    return False


# 文件外链=>下载到本地并修复链接
def file_locale(path,content):
    global file_flag
    file_flag = False
    def repl_file_link(matchobj):
        global file_flag
        file_flag = True
        location = os.path.dirname(path)
        fix_dir_name = os.path.join(location,FIX_DIR)
        if os.path.exists(fix_dir_name)==False:
            os.mkdir(fix_dir_name)
        file_result = re.findall(sub_file_pattern,matchobj.group(0))
        postfix = file_result[0][2]
        file_name = file_result[0][0]
        file_link = file_result[0][1]+"."+postfix
        url = file_result[0][1]+"."+postfix
        try:
            r = requests.get(url)
        except:
            old_content = "[" + file_name + "](" + file_link + ")"
            new_content = old_content
            msg = "文件外部链接失效，" + path + "\n\t\t\t\t\t\t失效链接为：" + url
            logger.error(msg)
        else:
            old_file_name = file_name
            file_name = name_escape(old_file_name) + str(int(time.time()))
            old_content = "[" + file_name + "](" + file_link + ")" 
            file_out = os.path.join(fix_dir_name,file_name + "." + postfix)
            file_parent_dir_miss_handle(file_out)
            with open(file_out,"w") as file:
                file.write(r.content)
            new_content = "[" + old_file_name + "](./" + os.path.join(FIX_DIR,file_name + "." + postfix) + ")" 
            logger.info("文件链接修复成功。" + path + "\n\t\t\t\t\t\t原内容为：" + old_content + "    \n\t\t\t\t\t\t新内容为：  " + new_content)
        return new_content
    return re.sub(file_rule,repl_file_link,content)


# 网址外链=>文本
def site_link_2_text(path,content):
    global site_flag
    site_flag = False
    def repl_site_link(matchobj):
        global site_flag
        site_flag = True
        site_result = re.findall(sub_site_pattern,matchobj.group(0))
        old_content = "[" + site_result[0][0] + "](" + site_result[0][1] + ")"
        # new_content =  "外网链接：" + site_result[0][1] + "(" + site_result[0][0] + ")"
        new_content = " " + site_result[0][0] + " ( 外网链接："+site_result[0][1] + " )"
        logger.info("网址外链转换成功。" + path + "\n\t\t\t\t\t\t原内容为：" + old_content + "    \n\t\t\t\t\t\t新内容为：  " + new_content)
        return new_content
    return re.sub(site_rule,repl_site_link,content)

# 图片外链=>下载到本地并修复链接
def pic_locale(path,content):
    global pic_flag
    pic_flag = False
    def repl_pic_link(matchobj):
        global pic_flag
        pic_flag = True
        location = os.path.dirname(path)
        fix_dir_name = os.path.join(location,FIX_DIR)
        if os.path.exists(fix_dir_name)==False:
            os.mkdir(fix_dir_name)
        pic_result = re.findall(sub_pic_pattern,matchobj.group(0))
        postfix = pic_result[0][2]
        pic_name = pic_result[0][0]
        pic_link = pic_result[0][1]+"."+postfix
        url = pic_result[0][1]+"."+postfix
        try:
            r = requests.get(url)
        except:
            old_content = "![" + pic_name + "](" + pic_link + ")" 
            new_content = old_content
            msg = "图片外部链接失效，" + path + "\n\t\t\t\t\t\t失效链接为：" + url
            logger.error(msg)
        else:
            old_content = "![" + pic_name + "](" + pic_link + ")" 
            old_pic_name = pic_name
            pic_name = name_escape(old_pic_name) + str(int(time.time()))
            pic_out = os.path.join(fix_dir_name,pic_name + "." + postfix)
            file_parent_dir_miss_handle(pic_out)
            with open(pic_out,"w") as pic:
                pic.write(r.content)
            new_content = "![" + old_pic_name + "](./" + os.path.join(FIX_DIR,pic_name + "." + postfix) + ")" 
            logger.info("图片链接转换成功。" + path + "\n\t\t\t\t\t\t原内容为：" + old_content + "    \n\t\t\t\t\t\t新内容为：  " + new_content)
        return new_content
    return re.sub(pic_rule,repl_pic_link,content)


def traversal_to_fix(ROOT_DIR):
    list_root_dir = os.listdir(ROOT_DIR)
    for i in range(0,len(list_root_dir)):
        path = os.path.join(ROOT_DIR,list_root_dir[i])
        if os.path.isfile(path):
            if recognize_bug_file(path) == True:
                try:
                    f = open(path,"r")
                except:
                    logger.error("文件打开失败：" + path)
                else:
                    buffer = f.read()
                    f.close()
                    file_localed = file_locale(path,buffer)
                    pic_localed= pic_locale(path,file_localed)
                    site_link_2_texted = site_link_2_text(path,pic_localed)
                    finished = site_link_2_texted
                    if (file_flag or pic_flag or site_flag):
                        new_file = open(path + "_new","w")
                        new_file.write(site_link_2_text(path,site_link_2_texted))
                        new_file.close()
                        os.remove(path)
                        os.rename(path + "_new",path)
                    logger.info("Finish " + path)
                    # print "file,pic,site"
                    # print file_flag,pic_flag,site_flag
        else:
            traversal_to_fix(path)


def loop_to_fix(ROOT_DIR):
    list_root_dir = os.listdir(ROOT_DIR)
    



def fetch():
    for repo in REPO_POOL:
        repo_name = repo["name"]
        os.chdir(os.path.join(ROOT_DIR,repo_name))
        fetch = GIT_FETCH
        logger.info("repo fetch " + repo_name)
        os.system(fetch)

def pull():
    for repo in REPO_POOL:
        repo_name = repo["name"]
        os.chdir(os.path.join(ROOT_DIR,repo_name))
        pull = GIT_PULL
        logger.info("repo update " + repo_name)
        os.system(pull)

def clone():
    for repo in REPO_POOL:
        repo_name = repo["name"]
        repo_url = repo["ssh_url_to_repo"]
        # print repo_name,repo_url
        # usage of gitpython
        # git.Git(LOCAL_PATH).clone(repo_url)
        clone = GIT_CLONE + repo_url
        logger.info(clone)
        os.system(clone)

def commit():
    for repo in REPO_POOL:
        repo_name = repo["name"]
        commit = GIT_COMMIT + COMMIT_MSG
        os.chdir(os.path.join(ROOT_DIR,repo_name))
        os.system(GIT_ADD)
        logger.info(commit)
        os.system(commit)
        print repo_name

def push():
    for repo in REPO_POOL:
        repo_name = repo["name"]
        push = GIT_PUSH
        os.chdir(os.path.join(ROOT_DIR,repo_name))
        logger.info(GIT_PUSH + " " + repo_name)
        os.system(push)


if __name__ == '__main__':
    get_repo_info()
    clone()
    # pull()
    traversal_to_fix(ROOT_DIR)
    commit()
    push()