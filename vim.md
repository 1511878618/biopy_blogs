## vimrc文件配置

首先需要知道vimrc是什么。

它是记录vim配置的文件，对于某个用户而言它的位置在`~/.vimrc` 

如果没有这个文件，就自己创建一个文件命名为`.vimrc`在home目录下就可以了

anyway 有了`.vimrc`后，在里面的写入的设置就可以在vim中起作用了
## 常用设置
在vimrc文件里面，注释采用`“”` 双引号而非常用的`#`。

如果需要进行代码编写，实现简单的代码高亮功能：`syntax on`

打开与正在写入的文件的类型相对应的缩进规则：`filetype indent on`
更多信息可以参见以下博客：
https://www.cnblogs.com/zhichaoma/articles/7820141.html
https://dougblack.io/words/a-good-vimrc.html

## 更改键位
vim默认键位如图所示，相应功能如图所示。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-20-vi-vim-cheat-sheet-sch.gif)

然后可以更改键位的映射

在文件里写入以下代码：
``` shell
noremap k i
```

