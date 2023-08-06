# SWTermColor

封装了 [termcolor库](https://pypi.org/project/termcolor/)，更方便使用了；

同时，也借鉴了 [termcolor2库](https://pypi.org/project/termcolor2/)的一些思想;

支持 python2 + python3;

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

print(PrintColor("hello, PrintColor sw"))
print(ColorPrint("hello, ColorPrint sw"))
print(SWTermColor("hello, SWTermColor sw"))
print(SWTermColor("hello, sw red").c_red())
print(SWTermColor("hello, sw red").c_blue().c_red())
print(SWTermColor().text("hello, sw red replace").c_red())
print(SWTermColor("hello, sw red bg_grey").c_red().b_grey())
print(SWTermColor("hello, sw red bg_blue").c_red().b_blue())
print(SWTermColor("hello, sw red bg_blue").c_red().b_white().b_blue())  # 背景色，蓝色 覆盖了 白色
print(SWTermColor("hello, sw red bg_blue bold").c_red().b_blue().a_bold())
print(SWTermColor("hello, sw red bg_blue bold dark").c_red().b_blue().a_bold().a_dark())
print(SWTermColor("hello, sw red blue bold reverse(反转)").c_red().b_blue().a_bold().a_reverse())


text = "hello, sw red bg_blue bold 文本 与 样式 分离"  # 文本
effect = SWTermColor().c_red().b_blue().a_bold()  # 特效 
print(effect)  # 输出空行
print(effect(text))  # 正常使用方法
print(effect(text, "color临时改为grey", color="grey"))  # 临时改变文本颜色
print(effect(text, "bg_color临时改为grey", bg_color="grey"))  # 临时改变文本背景色
print(effect(text, "attrs临时改为reverse", attrs=["reverse"]))  # 临时改变文本效果
print(effect.text("提示文案:"))  # 增加 提示文案
print(effect(text, sep=" *#sep#* "))  # 输出：提示文案 + text，以sep做分隔符
effect.text(None)  # 删除默认的提示文案
# 输出彩色的：1 + 2 = 3
print(effect(" 1") + effect(" + ", bg_color="cyan") + effect("2") + effect(" = ", bg_color="cyan") + effect("3 "))
```

## 截图（ScreenShot）

![image1](https://raw.githubusercontent.com/shede333/SWTermColor/master/screenshot/termnial.png)


## 致谢

* "swtermcolor/termcolor.py"文件，来自于[termcolor 1.1.0](https://pypi.org/project/termcolor/)  
* 设计思想借鉴了：[termcolor2](https://pypi.org/project/termcolor2/)  