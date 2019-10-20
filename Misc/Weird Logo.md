# Weird Logo
这道题给了一张图片。对于图片，首先打开隐写查看神器`StegSolver`，通过不断的按动下面的左右按钮，可以看到图片里面隐藏了一些残缺的二维码图片。我们使用该工具自带的Image Combiner功能，将不同的二维码图片叠加在一起，使用手机扫码得到了一个字符串，提交上去发现是Wrong Flag。说明此题还有其它的内容。

之后用16进制编辑器打开，发现在PNG文件尾后面有一些多出来的内容，使用编辑器把它们提取出来。发现里面有一个十分显眼的字符串：`txt.galf`，是倒过来写的`flag.txt`。联想到开始的那个倒着写的0ops的logo，我们使用Python将这些二进制内容倒过来。
``` python
f = open('flag','rb')
a = bytearray(f.read())
a.reverse()
fo = open('output','wb')
fo.write(a)
f.close()
fo.close()
```

翻转完成后发现output的图标变成了一个压缩包，打开提取发现需要密码，于是用二维码中的内容作为密码，解压得到flag。