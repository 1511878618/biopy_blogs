#如何让你的终端变得更好看.jpg
### 安装Ohmyzsh
可以直接通过官网的方式：https://ohmyz.sh/#install
也可以https://github.com/ohmyzsh/ohmyzsh
但是如果提示openssl之类的报错的话
则可以采用简单粗暴的方式
在ohmyzsh的github主页可以找到tools这个文件夹，里面的install.sh就是我们需要下载下来运行的安装脚本。如果是在下不下来，就可以直接打开，复制里面的代码。然后在本地
`vim install.sh`创建一个sh脚本，然后把复制的内容写入。然后`chmod +x install.sh` 以及`sh install.sh`便装上了ohmyzsh。如果此时默认的shell是zsh便可以发现画风大变～

### 安装PowerLine
需要使用pip命令，如果没有，安装python最新版就可以了，或者安装anaconda
`pip install powerline-status --user`

### 安装PowerLine的字体库
仍然需要上GitHub，链接：https://github.com/powerline/fonts
如果下载不下来可以试着直接下载或者使用迅雷～
随后进入下载或者解压得到的目录，运行`sh install.sh`安装字体
安装好了后，

### 剩下部分可以见https://zhuanlan.zhihu.com/p/37195261

