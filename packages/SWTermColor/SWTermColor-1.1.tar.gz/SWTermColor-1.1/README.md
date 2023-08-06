# SWTermColor

封装了 [termcolor库](https://pypi.org/project/termcolor/)，更方便使用了；

同时，也借鉴了 [termcolor2库](https://pypi.org/project/termcolor2/)的一些思想;

支持 python2 + python3;

注意：不同的终端软件、不同Shell，的输出效果会有些许的不同。

## Install

```

pip install SWTermColor

```

## Example Modules:

文本颜色，都是以 **"c_"** 开头的方法；  
背景色，都是以 **"b_"** 开头的方法；  
文字特性(加粗等)，都是以 **"a_"** 开头的方法；    

```python

from swtermcolor import SWTermColor
from swtermcolor import ColorPrint
from swtermcolor import PrintColor

# 注意：
# SWTermColor == ColorPrint == PrintColor, 三者都是等价的类名，根据喜好选用
SWTermColor("hello, SWTermColor").p()  # p 即 print的缩写
PrintColor("hello, PrintColor").p()
ColorPrint("hello, ColorPrint").p()


# 常用的几种打印方法：
print(SWTermColor("hello, sw red").c_red())
SWTermColor("hello, sw red").c_red().p()  # 先设置文本，再设置效果
SWTermColor().c_red().p("hello, sw red")  # 先设置效果，再设置文本
# 默认以", "为分隔符，打印所有文本
SWTermColor().c_red().p("hello", "sw", "red")
# 以" * "为分隔符，打印所有文本
SWTermColor().c_red().p("hello", "sw", "red", sep=" * ")


print(SWTermColor("hello, sw red").c_blue().c_red())
print(SWTermColor("hello, sw red bg_grey").c_red().b_grey())
SWTermColor("hello, sw red bg_blue").c_red().b_blue().p()
# 背景色：蓝色 覆盖了 白色，同时会打印一行覆盖警告
print(SWTermColor("hello, sw red bg_blue").c_red().b_white().b_blue())
print(SWTermColor("hello, sw red bg_blue bold").c_red().b_blue().a_bold())
print(SWTermColor("hello, sw red bg_blue bold dark").c_red().b_blue().a_bold().a_dark())
print(SWTermColor("hello, sw red blue bold reverse(反转)").c_red().b_blue().a_bold().a_reverse())


# 文本 与 样式 分离
text = "hello, sw red bg_blue bold 文本 与 样式 分离"  # 文本
effect = SWTermColor(prefix_text="提示文案前缀：").c_red().b_blue().a_bold()  # 特效
print(effect)  # 输出空行，因为没有文本信息
effect.p("看打印效果")
print(effect(text))  # 正常使用方法
print(effect(text, "color临时改为grey", color="grey"))  # 临时改变文本颜色
print(effect(text, "bg_color临时改为grey", bg_color="grey"))  # 临时改变文本背景色
print(effect(text, "attrs临时改为reverse", attrs=["reverse"]))  # 临时改变文本效果

# 输出彩色的：1 + 2 = 3
effect._prefix_text = None  # 删除 提示文案
print(effect("彩色文本") + " + 普通文本")  # 与普通str 相加
print("普通文本 + " + effect("彩色文本"))  # 与普通str 相加
print(effect(" 1") + effect(" + ", bg_color="cyan") + effect("2") + effect(" = ", bg_color="cyan") + effect("3 "))

```

## 截图（ScreenShot）

![image1](https://raw.githubusercontent.com/shede333/SWTermColor/master/screenshot/termnial.png)


## 致谢

* "swtermcolor/termcolor.py"文件，来自于[termcolor 1.1.0](https://pypi.org/project/termcolor/)  
* 设计思想借鉴了：[termcolor2](https://pypi.org/project/termcolor2/)

## 待完成的功能

1. 内置一些彩色打印模板，类似警告、错误等；  