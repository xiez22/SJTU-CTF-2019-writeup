# Basic Web
进入网页后并没有发现什么有价值的内容，按下`F12`，在网页源代码里看到这个可疑的内容：
``` html
<!-- You may try w3lc0me_t0_CTF.php -->
```
我们继续访问 `http://111.186.57.85:10023/w3lc0me_t0_CTF.php` ，发现提示 “You are not admin.”。根据经验，考虑修改cookies让自己变成admin。

在Chrome浏览器中，可以按下`F12`之后在`Application`标签页下找到Cookies，点进去就可以修改了。把`admin = 0`修改为1之后，刷新网页，便可以看到新的提示：“Can you POST flag=0ops to me?”。

为了方便，我们使用[GetMan](https://getman.cn)工具进行POST。设置好Cookies和post内容后，点击按钮，即可得到返回的flag:
```
0ops{I_like_flag_WoW_Do_you}
```