# BypassAv - Logs404

## 仅用于技术交流，请勿用于非法用途。


本仓库为木末君学习过程中积累的一些小脚本,不保证免杀效果

## 使用方法

终端输入

```shell
python3 v1.0.py
```

按照提示输入payload.c的路径即可

脚本会自动读取shellcode并生成代码

配置好gcc环境变量可以全自动编译为exe

推荐使用[tcc](https://www.bellard.org/tcc/)替代gcc作为编译器，免杀效果更佳

下图为tcc编译的查杀率，查杀率有点高，但是实测能过火绒、360、windows defender

![image-20221111163227761](https://s.imgkb.xyz/abcdocker/2022/11/11/35cf4697d9218/35cf4697d9218.png)
