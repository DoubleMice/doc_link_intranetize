#-*- coding:utf-8 –*-
# /usr/local/bin/python
import re
import os
import requests

fix_dir = "auto_fix_dir"
FIX_DIR = "auto_fix_dir" 
ROOT_DIR = os.getcwd()

text = '''
[cc[cc]ccc](http://auto_f(ix_d(ir/cccc)cc)c.html)，[bbbbbbb](http://auto_fix_dir/(bbb)bbbb.html)

* Added `toc` config to front-matter for `[TOC]` and sidebar TOC [#606](https://github.com/shd101wyy/markdown-preview-enhanced/issues/606)....(xxxxx).

[xxxx](http://asodfjaosdjf.c)
'''
# rule = "(?:c|cpp|pdf|py|asm|txt)"

rule = "(?<!!)\[[^\]]*?\]\((?:[a-zA-z]+://[^\s]*?|www\.[^\s]*?)\.(?:c|cpp|pdf|py|asm|txt)\)"
# rule = "[^!]\[.*\]\([a-zA-z]+://[^\s]*\)"
# rule = "(?<!!)\[[^\[\]]*(((?'open'\[)[^\[\]\]]*)+((?'-open'\])[^\[\]]*)+)*(?(open)(?!))\]\((?:[a-zA-z]+://[^\s]*?|www\.[^\s]*?)\)"
# rule = "\([^\(\)]*(((?'open'\()[^\(\)]*)+((?'-open'\))[^\(\)]*)+)*(?(open)(?!))\)"

# rule = "\[[^\[\]]*(((?'open'\[)[^\[\]\]]*)+((?'-open'\])[^\[\]]*)+)*(?(open)(?!))\]"

# rule = "\[[^\[\]]*(((?'Open'\[)[^\[\]\]]*)+((?'-Open'\])[^\[\]]*)+)*(?(Open)(?!))\]"

# print re.findall(re.compile(rule),text)
print "aa bb".replace(" ","_")

# rule = "[^!]"

#### 识别图片
# rule = "!\[.*\]\([a-zA-Z]+://[^\s]*\.\w+[png|jpg|jpeg]\)|!\[.*\]\(www\.[^\s]*\.\w+[png|jpg|jpeg]\)"

# def site_link_2_text(content):
#     def repl_site_link(matchobj):
#         sub_rule = "\[(.*)\]\((.*)\)"
#         sub_pattern = re.compile(sub_rule)
#         print "外网链接："+re.findall(sub_pattern,matchobj.group(0))[0][1]+"("+re.findall(sub_pattern,matchobj.group(0))[0][0]+")"
#     re.sub(rule,repl_site_link,content)
# site_link_2_text(text)



# def repl_pic_link(matchobj):
    # if os.path.exists(fix_dir)==False:
    #     os.mkdir(fix_dir)
    # sub_rule = "!\[(.*)\]\((.*)\.(png|jpg|jpeg)\)"
    # sub_pattern = re.compile(sub_rule)
    # postfix = re.findall(sub_pattern,matchobj.group(0))[0][2]
    # pic_name = re.findall(sub_pattern,matchobj.group(0))[0][0]
    # pic_link = re.findall(sub_pattern,matchobj.group(0))[0][1]+"."+postfix
    # url = re.findall(sub_pattern,matchobj.group(0))[0][1]+"."+postfix
    # try:
    #     r = requests.get(url)
    # except:
    #     new_pic = "图片外部链接失效：![" + pic_name + "](" + pic_link + ")" 
    # else:
    #     pic_out = fix_dir + "/" + re.escape(pic_name) + "." + postfix
    #     with open(pic_out,"w") as pic:
    #         pic.write(r.content)
    #     new_pic = "![" + pic_name + "](./" + pic_out + ")" 
    # print re.findall(sub_pattern,matchobj.group(0))[0]
    # print matchobj.group(0)
# re.sub(rule,repl_pic_link,text)


# pattern = re.compile(rule)
# match = re.findall(pattern,text)
# for member in match:
#     print member



##### 遍历测试
# def traversal_to_fix(ROOT_DIR):
#     list_root_dir = os.listdir(ROOT_DIR)
#     for i in range(0,len(list_root_dir)):
#         path = os.path.join(ROOT_DIR,list_root_dir[i])
#         if os.path.isfile(path):
#             print path
#             # with open(path,'r+') as f:
#             #     f.seek(0)
#             #     buffer = f.read()
#                 # log(FIX_SUCCESS,path)
#                 # file_localed = file_locale(buffer)
#                 # pic_localed = pic_locale(file_localed)
#                 # site_link_2_texted = site_link_2_text(pic_localed)
#                 # f.write(site_link_2_text(site_link_2_texted))
#         else:
#             traversal_to_fix(path)

# traversal_to_fix(ROOT_DIR)


##### 文档类型识别
# def recognize_bug_file(filename):
# bug_rule = "[^\s]*\.(md)"
# pattern =re.compile(bug_rule)
# print re.findall(pattern,"/aaa/vvv/bbb/ddd/test.md")[0]