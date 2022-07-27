

[TOC]

# Linux
1.高效利用文本搜索相关的命令
https://mp.weixin.qq.com/s?__biz=MzAxMDkxODM1Ng==&mid=2247485539&idx=1&sn=cbb02d48ea5bb90ee5bdf35d501ee428&chksm=9b4848d8ac3fc1ce58b14128a138c100d305cb70c61180b523c21ad4859fdcc2cd7e96a75c99&scene=21#wechat_redirect
2.掌握re的语法





## linux 命令
`&` 表示挂在后头运行
### 常用基本命令

`w `显示所有的用户
`top`查看所有运行的程序
`sleep`
`which`
`ps` `ps -ef` 查看任务运行列表
`ls` `ls -al` 
`ifconfig` 
##### `cd `
`cd ../`回到上一层目录

#### 显示目录内容
`ls`
`ls -al` 
`ls /*`
#### 排序命令
`sort`对结果排序，一般是当作字符串按照第一个字符进行排序
当指定参数则可以更改排序的规则：
1. `-n`**按照数字进行排序**
2. `-M`指定月份排序
3. `-r`降序排列
4. `sort -nr`按数字同时降序排列

### 磁盘管理
1. `df` 可以显示当前设备上所有挂载的磁盘的使用情况
> `df -h` 用M 和G表示使用空间来显示使用情况

2. `du` 可以显示当前目录下的所有文件、目录和子目录的磁盘使用情况。
  >1. `-c` 显示所有文件的总大小，也就是在末尾加上一个 total
  >2. `-s` 只显示当前目录下所有文件的总大小，也就是`-c`的total
  >3. `-h` 用K、M和G来显示大小
  >4. `du -sh *`可以显示当前目录下的所有文件的大小
### 进程管理
进程查看的方法如下：
1. `ps` 默认情况下，**只会显示在当前控制台下的属于当前用户的进程**
   >这个可选参数很多很复杂，当需要的时候在查需要的指令。
2. `top` 可以实时检测进程情况

如何结束进程呢？

linux中，进程之间通过**信号**来通信。进程的信号就是预定义好的一个消息，进程能识别它并决定忽略还是作出反应。进程如何处理信号是由开发人员通过编程来决定的。大多数编写完善的程序
都能接收和处理标准Unix进程信号。这些信号都列在下表中
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-062757.jpg)
在Linux上有两个命令可以向运行中的进程发出进程信号
1. `kill 进程PID` 可以终止某个进程
   1. `kill -s HUP PID` **-s可以指定其他的信号，用信号名或者信号值**
2. `killall`

### 搜索命令
#### `grep`
grep其实是正则表达式的搜索方法
最简单的使用就是直接`grep pattern file` 直接搜索pattern在file文件中
想要进行反向搜索，也就是不包括该搜索目标的其他结果则是`-v`
要显示搜索的结果所位于的行数`-n`
**要只输出**匹配的个数则`-c`
**当想要指定多个搜索的条件，并且多个条件之间的关系是 “或”** 则可以用`-e pattern1 -e pattern2 ...`来指定多个条件
>pattern的写法，也就是正则表达式的语法可以见：https://github.com/ziishaned/learn-regex/blob/master/translations/README-cn.md
>**但是需要注意的是grep是使用的unix风格正则表达式来匹配模式**

### 压缩数据与归档
压缩与归档虽然不是一个概念，但是两者往往一起用
#### 压缩
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-062759.jpg)
gzip包括以下的工具：
1. gzip：用来压缩文件
2. gzcat：用来查看压缩过的文本文件的内容
3. gunzip：用来解压文件
`gzip xxx`可以压缩某个文件，`gzip *.xxx` 可以批量压缩文件。此外`-1..9`表示压缩的质量，其中9压缩效果最好但是速度最慢。
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-070501.png) 
>压缩效果如图所示，所以选择最快的一般就好了

#### 归档
虽然zip命令 够很好地将数据压缩和归档 单个文件 但它不是Unix和Linux中的标准归档工具。目前 Unix和Linux上最广泛使用的归档工具是tar命令
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-073953.png)
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-074129.png)
基本归档命令
`tar -cvf test.tar test/ test2/` 可以归档 test/ 和test2/ 两个目录到test.tar中
`tar -tf test.tar` 则可以列出tar文件中的内容
`tar -xvf test.tar`可以从tar文件中提取文件
>`-c` 表示 归档 而`-x`表示提取
>加上`-z`则可以使用gzip进行压缩。
`tar -zcvf xxx.tar.gz file1 file2` 可以压缩文件
`tar -zxvf xxx.tar.gz `可以解压文件




## Shell的基本介绍
系统启动的时候会启一个可以交互的shell程序，这个程序取决于你的设置。设置在`/etc/passwd`文件中，其中第七个字段记录的便是默认的shell。 而所有的可以使用的shell位于`/bin/`目录下

可以直接运行`/bin/zsh`启动一个ZSH的shell，但是此时启动产生的是一个子shell，什么是子shell呢，就有点类似，我们打开了一个目录再打开一个目录的感觉。子shell里面也可以进行命令的运行，但是与主shell存在很多东西是不相通的。`exit`可以退出该子shell。此外`ps -f`也可以查看。PID和PPID相似的就是一对父子shell，PID的是父而PPID是子。
>运行某个命令后，会返回$这个符号，这个符号叫做CLI提示符，表示在等待命令输入。

>关于父shell和子shell之间的差异以及创建子shell会增加的运行损耗等等，对于生物er其实并不需要太过关心（也关心不过来哈哈哈哈哈）

>`exit`可以直接退出正在运行的shell或者子shell

下面就介绍一系列可以创建子shell或者挂在后头运行命令的方法。

首先是`;`可以用于命令行中，发挥的作用是依次运行一系列的命令
如：`pwd ; ls ;cd /etc ; pwd ;cd ; pwd ;ls`
这样的写法是在当前的主shell下运行会占用你的界面，你就必须得等待代码运行完才可以跑下一个代码，这就比较的头大与不爽，当然也可以写shell脚本去运行。

**那解决方法是什么呢？**
#### 进程列表
进程列表 写法`(command1 ; command2;...;command5)`会创建一个子shell去执行小括号中的命令。但是和上一种写法似乎没太大的差异。

这里又介绍一个符号：

`&` 可以把命令挂在后台运行。

**多个命令的同时运行一般采用这样的写法`(command1 ; command2;...;command5)&`可以把进程列表挂在后台**

这个时候要查看该命令可以`ps`也可以用`jobs`

>`jobs -l` 可以显示更多信息



#### 协程`coproc`

`coproc 进程列表`  实现的效果跟`&`类似


**总结**：
1. 多个命令按顺序执行`(command1;command2;...;commandn)`
2. 要让当前的shell创建一个子shell执行当前的进程列表`(command1...) &`
3. `coproc (command1...)` 效果类似与 **2**
4. 查看当前的任务用：`jobs -l`

#### `history`

可以显示过去使用命令（会保存最近的1000条记录）
`!!`可以快速执行上次的命令
通常终端运行的命令历史也会写入在`~/.zsh_history`这样类似的文件中，`history -a`可以强制写入

>但是对于子shell的命令存储好像有所差异，暂时不清楚具体的机制~~~~

`!20`可以恢复history中的第20个命令

下面再介绍一个比较好玩的命令

### `alias`给命令赋予别名

设置别名是什么其实算是一种缩写或者变量替换，普通的变量替换只能生成字符格式，使用`alias`的话就可以把**类似变量的一个命令**链接到**指定的某个命令上**

- `alias`不加任何参数可以显示当前的别名设置

- `alias 别名='command'`可以把该command和这个别名联系在一起。如：`alias envList='conda env list'`
- 但是需要注意的是不会在子shell中生效


### 环境变量
环境变量可以分为：**全局变量和局部变量**

那么什么是局部变量和全局变量呢？

局部变量和全局变量：

全局变量是第一个shell，也就是开机就启动的shell所生成的变量，可以通过`env`等命令去查看，此外全局变量还可以被后续启动的可交互shell以及子shell等调用到。

而shell启动后（无论是bash还是zsh等）均可以设置一系列局部变量，这样的局部变量可以通过`test=Hello`来设置，这样就可以设置一个名叫test的局部变量了。但是如果关闭这个shell则test这个命令会被删除，此外如果在子shell里面也无法调用。

那么如何把一个局部变量变成全局变量呢？ 可以通过`export test=Hello`就可以在创建的子shell里面调用。但是仍然，当重新启动系统后，test这个变量还是会被删除。
>更多关于[export](https://www.runoob.com/linux/linux-comm-export.html)

>**所有的bash shell的环境变量均使用大写字母。因此如果是你自己创建的局部变量或者shell脚本，应当使用小写字母。**
变量名是会区分大小写的。在涉及用户定义的局部变量时使用小写字母可以避免覆盖原有的系统环境变量
**要想解决这个问题就得先了解shell启动的过程**

#### shell启动的过程

登录shell的启动方式。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-042354.png)
其中这样的5个文件中，最为重要的是
`~/.bashrc`，因为这个文件始终会被运行一次，**里面可以写入各种用户自定义的变量与函数！**
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-042410.png)

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-042538.png)


![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-042602.png)


**对于一个用户每一次所启动的shell会读取`$HOME/.zshrc`，并运行其中的所有命令。因此如果需要设置一些变量或者别名，可以直接把命令添加到这里面进行配置。** 这样里面的变量就会在每一次启动shell的时候就生成。

而用户如果在登录shell中运行另外一个shell，这个shell叫做交互式shell。
##### 最后：总结

而如果实在分不清谁是谁的时候，只需要记住
**需要用到的全局变量和别名（alias）全部写入到你所使用的shell对应的.xxxrc文件中就好了。**
而其他的过程大可以不必完全了解原理
#### 查看所有变量的方式
那么如何查看交互式shell所定义的全局变量，以及用户定义的局部变量呢？
可以用这样的三个命令

1. `printenv`
2. `env`
3. `set`


 >命令env、printenv和set之 的差异很细微。set命令会显示出全局变量、局部变量以
及用户定义变量。它会按照字母顺序对结果进行排序。env和printenv命令同set命
令的区别在于前两个命令不会对变量排序 也不会输出局部变量和用户定义变量。在 
种情况下，env和printenv的输出是重复的。不过env命令有一个printenv没有的功能，可能会比较好用一些

##### 如何删除某个变量

- `unset test`就可以删除名为test的变量


>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-040630.png)
另外如果是在子shell中删除全局变量并不会影响到父shell中去。

##### PATH变量

当用户在命令行界面输入了一个外部命令（Linux无法在已经定义的PATH变量所指定的目录下找到或者系统本身的目录下找到）。PATH环境变量定义了用于进行命令和程序查找的目录。
PATH变量可以包含多个目录，每个目录之间用`:`分割，如下图
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-041504.png)
因此如果要添加一个目录到PATH变量中可以通过这样的方式

- `PATH=$PATH:~/xxx/bin` `~/xxx/bin`是一个目录。但是如前说提到的 这样无法永久保存。 

- 如果要永久保存可以写入到`.zshrc`中

## 编写shell脚本

`chmod +x xx.sh` 改变脚本的权限，这样便可以直接`sh ./xx.sh`了

### 生成一系列变量的方式

1. `{1..10}` 可以生成1~10的数字

### 变量定义

#### 字符串类型

字符串类型的变量定义
`a='xxxx'`而不能写成`a = 'dddd'`

``` shell
my_name="Xu Tingfeng"  #变量定义的时候不要打空格不要打空格不要打空格！！！ 写法和python有区别！！
echo "i am ${my_name}" #如果含有一个变量则要用双引号
#or 
my_name=Xutingfeng #此时不能有空格
```

> 单引号：`''` 和双引号：`""`的区别：
> 首先单引号字符串的限制：
> 1. 单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；
> 2. 单引号字串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可成对出现，作为字符串拼接使用。
>
>双引号的好处则是：
>1. 双引号里可以有变量 
>2. 双引号里可以出现转义字符
>**也可以不写双引号，这样会出现的一种情况是什么呢，当有空格存在就会报错**

字符串类型的数据也可以相加，也就是**拼接**

**`${变量}` 可以调用某个变量，但需要注意，如果变量对应的字符串存在空格，则需要写成`"${变量}"`来避免出现如下的错误：**

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-05-115939.png)

`${#变量名}`则可以显示变量的长度,但是仍然是字符串的类型

`${变量名:a:b}`表示索引，从a到b。
#### 数组
bash只支持**一维数组**
定义的方法：
``` shell
array=(value1 value2 str1 str2)
array=(
  value1
  value2
  value3
  value4
)
#可以单独定义或者修改其中的数据
array[0]=value0_new
array[1]=value1_new
```
读取数组中的元素的方法：
`${array[0]}`
而读取数组中的所有元素则用`@`符号
`echo ${array[@]}`

获取数组长度的方法仍然是在变量调用的括号中加上#号
也就是
``` shell 
test=(10 20 30 40 "hi" "hello")

echo "length is ${#test[@]}"
#or 
echo "length is ${#test[*]}"
#这里@和*号似乎都可以表示索引全部

```

### Shell脚本参数的传递
shell中的预定义的变量有0,1....,n。
这些变量就是，执行脚本的时候向脚本传递的参数。
```shell
echo "执行的文件名: ${0}"
echo "第一个参数: ${1}"
echo "第二个参数: ${2}"
```
然后执行`./test.sh hi hello`
便可以得到输出
```shell
(base) xutingfeng@xutingfengdeMacBook-Pro ~ % ./test.sh hi hello
执行的文件名: ./test.sh
第一个参数: hi
第二个参数: hello
```
>另外一些特殊的字符来处理参数
>``` shell
>echo "执行的文件名: ${0}"
>echo "第一个参数: ${1}"
>echo "第二个参数: ${2}"
>echo "传递到脚本的参数个数：$#"
>echo "当前传递的所有参数：$*"
>echo "当前传递的所有参数：$@"
>echo "脚本运行的当前进程ID号：$$"
>echo "显示Shell使用的当前选项：$-"
>```

关于`$*`与 `$@`的区别：
用for循环来显示它们
``` shell
echo "--- \$* 演示 ---"
for i in "$*"; do 
    echo $i
done

echo "--- \$@ 演示 ---"
for i in "$@"; do 
    echo $i
done
```
输出如下：
```shell
--- $* 演示 ---
hi hello
--- $@ 演示 ---
hi
hello
```
### shell的基本运算符
``与''和”“不同
>``是可以执行command line命令，类似的还有这样的写法`$(expr 4 + 4)`

`expr `是用于表达式计算的工具

``` shell
echo `expr 2 + 2`#用``框住的部分会被shell当做命令行代码去运行
a=10 #a='10'似乎也可以
b=20
echo `expr ${a} + ${b}`
```

>注意：如果是条件表达式要放在方括号之间，并且要有空格，例如: [$a==$b] 是错误的，必须写成 [ $a == $b ]

在bash shell 中可用[]更加方便，如`val3=$5[${a} * ${b} ]` 但是在bash shell中数学运算符只支持整数运算，**不推荐过度依赖shell进行数学计算！**
也可以这样写
```shell
a=5
b=6
result=$[a+b]
echo "the sum of a plus b is equal to ${result}"
```

### 重定向

简单来说就是把某个命令的输出不仅仅显示在显示器上而是**把命令的输出重定向到另一个位置如文件，某个命令输入等**

1. `command > outputfile`  输出重定向`>`
2. ` | ` 管道符号，上一个命令的输出作为下一个命令的输入
3. `command < inputfile` 输入重定向`<`
   >`conda list | sort | more`
4. `>>` **可以追加数据**，而`>` 是覆盖写入
一个`>>`的使用案例

``` shell
for i in {1..10};do
    sleep 1 
    date >> date.log
done
```

不过要认真梳理重定向相关的知识的话，还是挺复杂的。上面的部分会记录一些常用的简单用法，**下面的内容则会记录详细的东西**

首先需要搞清楚这两个符号，这两个符号是重定向中最重要的两个符号
输入重定向`<`，也就是把右边的文件的内容当做左边的输入

输出重定向`>`，就是把左边的输出作为右边文件的输入

到了这里就得提一提linux如何处理命令产生的输出的。
通常我们运行一个命令会有这样的几个东西：

1. 命令的输入 STDIN ，

>对于终端来说，**一般就是我们键盘输入的东西，比如`echo 'xxxxx'`**，这里的`xxxxx`就是一个STDIN或者`cat`运行后，终端会提示输入东西，这个时候键入的几个字符也是一个标准输入，当然你按下回车键，他就会显示在屏幕上。；而输入重定向做的事就是把这样的输入重新定向到其他地方，比如某个文件等。

2. 命令的输出 STDOUT

>命令的输出，通常命令的输出是会根据STDOUT定位到屏幕上的。**如果采用输出重定向符号`>`**则可以定位到某个文件或者变量上。需要注意，命令的报错是不会跟着走的。

3. 命令的报错 STDERR
这三个部分都是会显示在我们的屏幕上，但是他们却有一个对应的描述符来描述
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-14-081853.png)

这三个描述符：`0`,`1`,`2` 都会对应这一个位置，**如果不加以修改的状态就是屏幕**。

那么这个描述符起的作用是什么呢，其实重定向符号还可以这么写
- `1>` 1也就是重定向STDOUT的输出到一个位置
- `2>` 2也就是重定向STDERR的输出到一个位置

这么写大家就明白了吧。也就是 一个命令的输出有两部分，**标准输出和标准错误**。这两部分是分开的，如果要重定向他们的话就需要在重定向输出符号上指定这个数字，来告诉系统你需要处理的是那部分输出。

那么在这个地方就把输出的重定向是说明白了。但是关于输入的重定向还有一些东西没说，此外还有如何修改描述符定向的位置。

**不过让我们直接快进到如何在脚本中使用这些吧**

在脚本中重定向需要使用`exec`命令
`exec 1> test.file`就可以永久的更改 脚本中后续的输出的位置
然后如果要把其中一个命令的输出重定向到某个地方可以使用`>&2`，就可以重定向到STDERR，比如：
`echo "这是一个报错信息" >&2` 就可以把`echo`的结果放到STDERR中去。

如果运行下面这个脚本：
``` shell
exec 2> test.error
echo "这个应该显示在屏幕上方"
exec 1> test.out
echo "这个应该在输出重定向到其他的文件了"
echo "这是一个报错信息" >&2
```
结果如图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-14-085712.png)
可以看到的确重新定向输出了。

**接下来就是如何在脚本中重定向输入了**
也就是告诉脚本，某个命令不从STDIN这里读取而是从其他的描述符或者文件读取
如果只是临时的读取，可以用`cat < test.file`实现
**而在脚本中永久的更改**，则是类似与上面更改重定向输出一样的操作`exec 0< test.sh`，这样后续的命令就可以不再指定输入的文件名了~。
也就是这个时候`read line xx.file`就可以直接写成`read line`~
```shell
exec 0< test.sh
count=0
while read line
do 
    echo "${count}\t${line}"
    count=$[ ${count} + 1]
done 
```

那么问题就继续来了，如何定义一个新的描述符，使得我可以在脚本中让一些文件的输出放到指定的log文件中去呢？
创建输出重定向的描述符可以如下
`exec 3>test.test`便可以创建一个输出重定向的符号：3，并且重定向到test.test
然后`echo 'xxx' >&3`便可以重定向到3这个地方，**需要注意写法`>&3`！**
```shell
exec 3>test.test
echo "这是一个测试信息" >&3
```

此外也可以做类似与之前提到的IFS的替换的方式的写法
``` shell
exec 3>&1 #把1这个描述符的信息赋值给描述符3
echo "这是一个测试信息，并且应该出现在屏幕中。" >&3

exec 1>test.test  #重新修改1的描述符
echo "这个应该是出现在一个文件中而非屏幕上"

exec 1>&3 #还原1描述符的信息
echo "这个信息现在应该还是出现在屏幕上的而非文件中。"
```
运行结果如下
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-14-134120.png)

输入重定向也是一样的操作
``` shell
exec 3<&0 #把STDIN 赋给3
exec 0<test.sh #把0输入重定向到test.sh
exec 4>test.test
count=0
while read line
do 
    echo "${count}\t${line}"
    count=$[ count+1 ]
done >&4
# cat test.test
```

最后怎么关闭一个描述符：`exec 3>&-`

#### 有趣的应用
在linux系统中有个文件叫做null，这个文件的特性就是，里面不会储存任何数据，**也就是我们可以把所有不需要的输出全部重定向到这个文件里面**

比如说：我们不想让我们的脚本显示一系列的报错或者一系列的通知，想让它**安静**的运行

那么就可以把`exec 1> /dev/null` `exec 2> /dev/null`
``` shell
exec 1> /dev/null
exec 2> /dev/null

echo "hi" #这个应该出现在屏幕上
cat xxx.test # 这个地方应该会出现报错信息

echo "这个应该在文件里面" > log.log # 这个应该会出现在文件里面
```


此外呢，还有的时候需要创建一个临时文件来保存一些临时的东西。linux中的/tmp目录下便是这样的一些东西。可以把文件丢到这下面，这样在下次开机的时候，这些文件就会被删除掉。

但是有的时候就不想把东西丢到哪里去，太远了，诶嘿嘿。

那么`mktemp`命令就有用武之地啦。`mktemp log.XXXXX`便可以生成一个名叫`log.几个X就会有几个的随机字符`的文件~
比如![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-14-140606.png)

这个时候，就可以把临时产生的一些输出丢到这里面去了，这样可以临时的使用，之后就会被删除~
如下面：
``` shell
tempFile=$(mktemp log.XX)

exec 3>${tempFile}
echo "${tempFile}"
echo "这个信息应该在文件中出现嗷" >&3

exec 3>&-

cat ${tempFile}

rm -f ${tempFile} 2> /dev/null

``` 
此外 `mktemp -d test.XXX`可以创建一个临时目录~
``` shell
tempDir=$(mktemp -d log.XXXXXX)

tempLog1=$(mktemp ${tempDir}/test.XXXX)

exec 3>tempLog1

echo "这个应在文件中哟" >&3
```

#### `tee`
有的时候不仅仅想让信息显示在屏幕，也想让它记录到文件中

`tee`就可以重定向STDOUT，不能重定向STDERR 

可以直接简单的使用`who | tee log.log`;`tee -a fileName`采用追加模式而不是覆盖模式~

#### 挂在后台运行的程序需要注意~ `&`
之前提到过，如果要把程序放在后台运行需要在后面加上`&`

但是标准输出仍然是在屏幕上，这就很麻烦了
>如果不知道这是个什么情况的话可以试试运行下面的代码
``` shell
echo "Start the scripts now"
count=1
while [ ${count} -le 5 ]
do 
    echo "loop ${count}"
    sleep 5
    count=$[ ${count}+1 ]
done 
echo "Script is done!"
```


这个时候用刚刚讲到的`exec`去**修改标准输出的位置**便可以解决这样一个问题拉~
``` shell
exec 3>&1
tmpFile=$(mktemp test.XXXX)
exec 1>${tmpFile}
echo "Start the scripts now"
count=1
while [ ${count} -le 5 ]
do 
    echo "loop ${count}"
    sleep 5
    count=$[ ${count}+1 ]
done 

echo "Script is done!"

```


### 挂在后台运行程序

<!-- shell也把运行中的进程叫做 **作业** -->

挂在后台运行程序，是我们使用服务器的一个核心要求，**因为我们生信er使用服务器的唯一目的就是跑程序**，通常我们的程序耗时一般都会很长很长，而这个过程我们也不能坐在这里等待程序运行，我们可能会进行其他的操作，甚至退出终端进行 **严肃认真的摸鱼活动**。 这个时候我们该怎么办呢？

之前我们熟悉的`&`的命令可以创建一个子shell去执行我们的程序，但是我们如果退出了终端，自然地这个子shell也会**收到相应的退出信号**然后它也会退出🤡。这就很尴尬了，不过在不需要退出的时候就可以这样挂着。

那么如果我们需要退出终端的时候怎么呢？

加上`nohup` 就好了，但是这个时候又要注意一个问题，之前说`&`这个后运行的程序的标准输出和标准错误仍然会输出在屏幕上，因此我们使用了`exec`修改它们两个到了一个临时文件，而加上`nohup`它会把后面的程序的标准输出和错误重定位到`nohup.out`，**这个时候如果我们之前在脚本里修改了定位，那么`nohup.out`里面就会没有任何东西，也就是说这个时候可以删除我们之前的重定向。**

另外一个点是：运行位于同一个目录的多个命令，它们的输出结果都会放到该目录下的`nohup.out`，因此需要避免这样的问题。也可以`(nohup ./test.sh &) > test.out`


#### 定时运行脚本~
使用`crontab`进行
>[更多关于`crontab`](https://www.cnblogs.com/intval/p/5763929.html)



### 结构化命令
#### if-then 
也就是if条件
```shell
if command
then
  command1
  command2
fi 

#or 
if command;then
  command1
  command2
fi

```
这里的`command`如果运行成功回返回statue code 为0，如果报错则会返回其他，而if只有在收到状态码0的时候才会继续运行下去。
而then下面如果有命令的退出状态码是非0则会停止。
>退出状态码，任何一个命令结束后就会生成一个状态码，从0～255，通过$$?$可以获取当前最新的一个命令的状态码。
>`exit number`可以在自定义的Shell脚本或者其他地方返回一个状态码，这样便可以调用。

另外一种写法 `if-then-else`的写法
```shell
if command
then 
  commands
else
  commands
fi

#回车可以用;代替

```

以及if-elif语句
```shell
if command1;then
  commands_1
elif command2;then
  commands_2
fi

```

这里的`command` 一般是用 `test` 或者`[]`，后面会有更多关于这个的写法

##### case语句来实现不同条件输出不同结果
`case`命令可以较好的实现，对于不同的输入给予相应的输出的要求。
比如：下面这个例子
``` shell
case ${1} in
xutingfeng | nick)
    echo "hi, administrator .";;
boss | ana)
    echo "hi, visitor";;
*)
    echo "warrning!"
esac
```
首先，需要解释一下`case`的写法，见下面

```shell
case 变量 in
pattern1 | pattern2 ) #pattern1或者pattern2 会执行com1和com2
    commands1
    commands2;;
pattern3);; # pattern3会执行com3
    commands3;;
*) # * 表示任何 非前面写到的pattern的情况。会执行commands4
    commands4;;
esac
```
这样再回头看第一个例子是不是就比较清晰了呢？

#### test
test可以测试某个命令或者某个条件，如果成立则返回状态码0，这样。test命令便可以用于if语句中作为判断条件，test可以用于数值、字符和文件三个方面的测试
>可以用`[]`代替test
>需要注意的是`[ ${value1} -eq ${value2} ]` 而不是`[${value1} -eq ${value2}]` 

下为test的参数
##### 数值比较
**需要注意的是，只支持比较整数！！！，浮点数在bashshell中可以`echo`但是不能计算~**
1. `-eq`等于则返回真 `=`也可以代替 eq:equal
2. `-ne`不等于则为真 `!=`也可以代替 ne:negative equal
3. `-gt`大于则为真 gt:greater than
4. `-ge`大于等于则为真 ge:greater equal
5. `-lt`小于则为真 lt:lower than
6. `-le`小于等于则为真 le:lower equal
```shell
num1=100
num2=200
if test $[num1] -eq ${num2};then
  echo "两个数相等"
else
  echo "两个数不相等"
fi

#or 

value1=10
value2=20

if [ ${value1} -gt 5 ]
then 
    echo "The test value ${value1} is greater than 5"
fi 

if [ ${value1} -eq ${value2} ]
then 
    echo "The values are equal"
else
    echo "The values:${value1} and ${value2} are different"
fi
```
##### 字符串的比较
1. `=`等于则为真
2. `!=`不等则为真
3. `-z 字符串`字符串的长度为0则为真
4. `-n 字符串`字符串长度不为0则为真
5. 虽然可以支持使用 `>`等参数，但容易出现奇怪的bug，需要进行的操作会比较麻烦，不推荐使用过于复杂的比较。
```shell
name1='Xutingfeng'
name2='Nicktf'
if test ${name1} = ${name2};then
	echo "${name1} = ${name2}"
else
	echo "${name1} != ${name2}"
fi

#or 使用[]

logUser=xutingfeng

if [ ${USER} = ${logUser} ];then
    echo "Welcome ${USER}"
fi


```
##### 文件比较
1. `-e 文件名` 文件存在则为真
2. `-f 文件名` 文件存在且可读则为真
3. `-w 文件名` 文件存在且可写则为真
4. `-x 文件名` 文件存在且可执行则为真
5. `-s 文件名` 文件存在且不为空

更详细的看一看这个表格：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-03-064807.png)

当需要对文件进行操作的时候最好是先采用这样的命令判断文件是否允许用户进行相应的操作。

不过最多用的应该是判断文件是否存在，是否为目录或者文件也就是：
`-d` `-f`
以及`-e`
**example1：**
```shell
# echo "Now we are at the is directory `pwd`"
targetFile=$HOME/test/test.py

if [ -e ${targetFile} ];then
    echo "There is ${targetFile}"
    if [ -f ${targetFile} ];then
        echo "It is a file "
    elif [ -d ${targetFile} ];then
        echo "It is a dirctory"
    fi 
else
    echo "There is no such file :${targetFile}"
fi

```
**example2：**

``` shell
targetDirectory=$HOME

if [ -d $targetDirectory ]
then 
    echo "The ${targetDirectory} exists"
    cd $targetDirectory
    ls
else
    echo "The ${targetDirectory} does not exist"
fi

```
##### 复合条件测试

也就是多个条件的判断，如：想要判断某个文件是否是文件，并且可读。就要用到`&&`和`||`，前者是and，后者是或。
可以这样写
``` shell
targetFile=$HOME/test/test.py

if [ -f ${targetFile} ] && [ -r ${targetFile} ];then
    echo "OK, this file: ${targetFile}  can be read"
else
    echo "Sorry, this file have some problems to be accessed "
fi 

#or

targetFile=$HOME/test/test.py

if [ -f ${targetFile} ] || [ -d ${targetFile} ];then
    echo "OK, this file: ${targetFile} is available "
else
    echo "Sorry, this file is unavailable "
fi 
```
`&&`和`||`这两个符号在刚刚的例子中用到了。

`&&`是and的意思，表示左右均返回TRUE，则可以
`||`是or的意思，表示左右任意一个为真就好。



##### 双括号与双方括号
###### 双括号`(( expression ))`
**用于数字比较**

在if-then的用法中可以使用双括号：`(( expression ))`
>双括号也可以用于数学计算，但是也不支持浮点运算。
>**在双括号中的符号也不用进行转义。** **因此数字计算推荐用双括号**
```shell
val=12
if (( ${val} ** 2 > 30 ))
then
    (( val1=${val} ** 2))
    echo "The square of ${val} is equal to ${val1}"
fi  
```
###### 双方括号 `[[ expression ]]`
**用于字符串比较** 可以使用**正则表达式**

``` shell 
if [[ ${USER} == xu* ]]
then
    echo "Hi, ${USER}."
else
    echo "Sorry, you are not authorized."
fi
```


#### for循环
标准模板：
```shell
for var in list
do 
  command1
done

or 

for val in list;do
  command1
  command2
  ...
  commandn
done
```
**此外也可以把循环的输出重定向到一个文件中**
``` shell
for i in `ls`
do
    echo "${i}"
done > test.log
```

结合后面会提到的修改IFS以及多个嵌套的循环的写法可以实现各种有趣的功能。比如：我们知道`PATH`变量中存有系统可以执行的各类文件的目录，因此如果写循环去读取这些目录下的文件然后存到`bin.log`文件中，也是可以简单实现的。

``` shell
IFSold=${IFS}#保存之前的IFS
IFS=$":" #更改新的IFS
for folder in ${PATH}
do
    for file in ${folder}/*
    do
        if [ -x ${file} ];then #检查该文件是否为可以执行的文件
            echo "${file}"
        fi
    done
done > bin.log
```



##### IFS
在for循环中，读取的变量如果不是列表的话，则会按照**一些分隔符进行切分**。

这样的分隔符（linux中用一个变量叫IFS）在linux中的默认情况是：空格、制表符和换行符。

然而在实际使用上往往需要更改这样的分隔符。

可以直接使用`IFS=$':'` ，其中`$''`**是一个语法结构！**

如果要指定多个分割符则可以采用如这样的写法`IFS=$':;!\n'`，这样将会指定`:`、`;`、`!`以及换行符作为分隔符。

如果想要临时的修改IFS的话则可以
``` shell
IFS.old=IFS #把原来的IFS存为IFS.old
IFS=$':'
command

IFS=IFS.old #还原为原来的IFS
```
>如果要把linux命令输出赋值给变量的话，这样进行out=`pwd`


##### 使用通配符获取某个目录下的所有文件名
一个简单的示例可以如下
``` shell

for file in ./*
do
    if [ -f ${file} ]
    then
        echo "${file} is a file."
    elif [ -d ${file} ]
    then
        echo "${file} is a directory."
    fi
done
```
但是如果想要获取多个目录下的文件名怎么办呢，可以采取下面的写法
```shell

for file in ./* ~/Music/* #只需要在这里添加上目录就好
do
    if [ -f "${file}" ] #为什么要写成"${file}"，是因为，如果文件名中存在空格，则会报错，因此可以考虑添加""
    then
        echo "${file} is a file."
    elif [ -d "${file}" ]
    then
        echo "${file} is a directory."
    fi
done
```
#### while循环
``` shell
while testCondition
do
    command1
    ...
done

```
上面就是一个标准的模板，其中`testCondition`指的是判断条件，写法和if中的是一样的，可以用`test`也可以用`[]`
一个简单例子如下：
``` shell
var=10
while [ ${var} -gt 0 ]
do
    echo "${var}"
    var=$[ ${var} - 1 ]
done 

```
`var = $[ ${var} -1 ]`这里的`[]`是进行数学计算，

此外 `while` 后面还可以跟上多个命令
``` shell
var=10
while echo 'running while'
echo 'hi'
[ ${var} -gt 0 ] #只有最后一个命令才是作为真正发挥作用的判断条件
do
    echo "${var}"
    var=$[ ${var} - 1 ]
done 
```

#### until命令
与 `while`命令相反 `until`命令是到什么为止，也就是后面跟的判断条件返回的状态码是0的时候（也就是TRUE）就会停止运行后面的代码。

简单来说就是一直运行后面的命令，**直到**判断条件成立。

``` shell
var=10
until echo 'running while'
# echo 'hi'
[ ${var} -eq 3 ]
do
    echo "${var}"
    var=$[ ${var} - 1 ]
done 
echo "until command finishes"
``` 


#### 多次嵌套循环
其实就是循环之中在加入循环~

一个简单的示例如下：
``` shell
IFS.old=IFS
IFS=$'\n'
for i in `cat /etc/passwd`
do
    IFS=$':'
    for j in ${i}
    do 
        echo "${j}"
    done 
done 

```
本案例也就是使用了两次`for循环`，并且每一次循环开始前更改`IFS`使得可以正确的迭代出`/etc/passwd`文件的内容。

#### 如何打破循环
`break`和`continue`命令可以实现打破循环的一个效果。一般与if语句结合使用
- `break` 表示打破**这个循环**，直接停止现在**进行的这个循环**直接进入后续的命令运行
- `continue`表示打破**这次循环**，**停止当前这一次循环的迭代，进入下一轮迭代**


### shell脚本怎么优雅的处理用户输入
在bash shell中，自带的一些命令可以实现读入用户的输入

`./test.sh var1 var2 ... varN` 在执行脚本的时候后面跟上多个值，这些值也可以在shell脚本中调用到。

那么怎么调用呢？

bash shell中**会预定义好一些以数字命名的变量**。如：`${0}` `${1}` `${2}` ... `${N}`

- `${0}` **是这个脚本的名称**
- 而`${1}` ... `${N}`**则是对应的执行脚本时写入的**`var1`...`varN`

因此可以通过这样的方式进行调用。

此外还有这样一些预定义的变量
- `$*` 会把命令行中的所有输入**当做一个字符串处理**
- `$@` **会把命令行中的每一个输入当做一个字符串处理，可以通过for循环来迭代**
- `$#` **会显示输入的参数的个数**

但是，我们经常看到各类命令可以指定`-h`等参数来传入输入，那么又要怎么去编写脚本实现这样的功能呢？

**这里要用的一个新的命令`shift`**。

代码如下
``` shell
while [ -n "${1}" ] #记得加”“，这样才是字符串
do
    case "${1}" in
        -a) echo "Found the -a option";;
        -b) echo "Found the -b option";;
        -c) echo "Found the -c option";;
        *) echo "not found the ${1} option";;
    esac
    shift #把所有其他的参数往左移动一个，并且会删除第一个参数
done
``` 
首先`while`确保`shift`完所有参数后传入的参数不是空字符串，也就是`shift`移动完所有参数后，while循环会终止。

然后`case`判断位于第一位的参数是什么，根据后面的4个判断条件进行相应的输出。

>`shift`命令的作用很简单。用户的输入会被shell赋予`${1}`等变量名，`shift`运行一次，就会把所有的参数的变量名 往左移，也就是：`${2}`的变量会变成`${1}`，而`${1}`则会删除而非变成`${0}`。**需要注意的是`${0}`是不会受到影响的**

这样我们输入`./test.sh -a -b `就会work了

通常我们使用的命令行工具带上参数是这样的形式 `./test.sh -i inputFile -m -h`
那么怎么实现这样的过程呢？

只需要对上面的代码进行一点点的修改

``` shell
while [ -n "${1}" ] #记得加”“，这样才是字符串
do
    case "${1}" in
        -i) echo "Found the -i option"
            filePath=${2} #参数位于当前的第二位，赋值给一个变量给后面使用
            echo "使用的输入文件为${filePath}"
            shift;;# shift一次，这样循环结束的时候还会shift一次 就可以把该次的-i 和参数一起消除掉
        -m) echo "Found the -m option";;
        -f) echo "Found the -f option";;
        *) echo "not found the ${1} option";;
    esac
    shift #把所有其他的参数往左移动一个，并且会删除第一个参数
done
```

但是，如果`./test.sh -fm`就会报错了。因为这样的写法不支持这样的功能。
#### getopts来处理用户的参数~
**目前使用最多的是使用`getopts`命令**
`getopts`命令的用法是：`getopts optstring variable`。

- `optstring`是指，设置的参数，如`iom`，表示使用参数`i`,`o`和`m`。可以在单个参数后加`:`，如：`i:o:m`，这样的效果是，`i`和`o`后面会有参数，这样的参数会被对应的赋予给`OPTARG`这个变量。
- `variable`会把当前处理的参数保存到其中。

通常会和while循环一起使用
一个example：
``` shell
while getopts :i:o:m opt 
do  
    case "${opt}" in
        i) echo "input File:${OPTARG}";;
        o) echo "output File:${OPTARG}";;
        m) echo "using max model~";;
        *) echo "Unknown Option ${opt}";;
    esac 
done 
```

**使用的时候可以参照这个进行修改**
>设置参数的时候，一些大家共同认可的参数设置
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-12-110107.png)

#### 手动输入的情况
有的时候，我们需要让使用者手动输入一系列信息，比如：是否同意进行操作(y/n)等情况

使用`read` 命令实现
``` shell
read -p "输入你的年龄" age
echo "your age is $[ ${age} * 10 ]"
```
也可以使用多个输入；什么是多个输入？

其实就是在输入的地方，采用分割符号（空格）来分割产生多个变量，这些变量会依次赋予给`name1` ...`name3`，**其中最后一个变量会接受所有剩下的输入**
``` shell 
read -p "输入你的兄弟的名字：" name1 name2 name3
echo " your brothers : ${name1} ${name2} ${name3}"
```
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-12-111745.png)

此外，可以通过`-t`设置一个时间，如果用户反应的时间超过这个时间则返回非0的状态码，也就是退出~
也就可以和 `if`命令联用~
``` shell
if read -t 5 -p "输入你的年龄" age
then
    echo "your age is $[ ${age} * 10 ]"
else
    echo '\n Waitting for to long time and sys exit!'
fi
```
`-n` 可以设置接受到多少个字符后就退出，如`-n1`表示接收到1个字符就退出，而不需要按回车
>`-p` 表示显示后面的字符~

```shell
read -n1 -p "是否同意(y/n)：" answer 
case ${answer} in 
    Y | y) echo "\n Fine, continue on ...";;
    N | n) echo "\no Ok, sys exit"
           exit;;
esac 

echo "Finished"
```
此外 `-s` 可以隐藏输入的字符，也就是输入密码时使用的情况~
``` shell
read -s -p "please enter your password:" password 

echo "Make sure your password is correct~"
```

##### read的其他用法
###### 读取文件
可以从文件中读取数据。如下例
``` shell
ls
read -p "enter the file you want read:" fileName
count=1 #用以显示行号
cat ${fileName} | while read line
do 
    echo "${count}\t${line}"
    count=$[ $count + 1 ]
done 
``` 
其中该文件的名字`test.sh`。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-12-113902.png)




### 函数定义
如何在shell脚本中定义一个函数呢？
```shell
function func1 {
    echo 'Hi, this is ur first function'
}
func1
```


## 用户管理
在linux上，可以对不同得用户(user)和群组(group)进行管理，这样不同的用户或者群组可以访问其权限内的文件，而不至于出现用户A删除用户B的文件等情况，这样做的好处便是可以对服务器进行有效地管理，比如：**生信分析工具是大家都会使用到的，那么这一部分工具就应该对于所有用户是可用的。而每一个用户自己的数据则由应该只可以由自己或者同一个课题组的成员所访问而不应该可以被其他人员读取或者覆写等操作。**

因此进行这样的用户管理可以十分方便的对服务器（特别是大型的公共服务器进行管理）

**但是这一部分对于非管理员而言则没有太多的用处！**

不过有用的一部分是，对于文件的权限管理却是我们需要了解的部分。
这里就不得不提及`ls`命令。 该命令可以显示目录下的文件的详细信息

常用的是`ls -al`
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-30-064819.png)
其输出结果如下
**其中第一列便是代表文件的权限只读**，**这里的一列也叫字段**
以`drwxr-xr-x@`为例子说明：

其中第一个字符表示该文件是 **文件还是目录**，d表示directory 
> - `-`代表文件
> - `d`代表目录
>-  `l`代表链接
>-  `c`代表字符型设备
>- `b`代表块设备
>-  `n`代表网络设备

**而之后的每3个字符为一组，分别代表该对象的拥有者、拥有者所属的组以及其他用户的权限**
这三个字符代表分别依次又是`rwx`，如果没有对应的某个权限，比如：没有w权限则写成`r-x`。
>`rwx`分别是什么意思呢？
>`r`表示read，读取权限
>`w`表示write，写入权限
>`x`表示执行权限
>需要注意的是尽管你是对象的拥有者也不一定同时具备这三个权限。比如：有的文件不可以被执行，那么就是`rw-`

权限机制了解，下一步就应该是学习如何修改某个文件的权限啦！
### 如何修改某个文件的权限
这里首先先引入关于二进制的部分的一些知识！

在linux中对于`rwx` 是用二进制来表示比如：`rwx`对应的是`111`，而其转化为8进制的结果为$2^2+2^1+2^0=4+2+1=7$；`r--`对应`100`，转化为8进制的结果是：$2^2+0^1+0^1=4$

这样任意给出一个权限，只要是`rwx`的写法，均可以得到其对应的二进制结果（有这个权限的位置就是1，没有就是0），然后也可以转化为8进制的数字。 **这样我们就得到了该权限对于的8进制的数字**。

这个数字有什么用呢？ 其实就是更改某个文件的权限的时候使用的啦

这里引入`chmod`命令，最简单的更改某个文件的权限的方式是`chmod 八进制的数字 文件名`就给某个文件赋予这个8进制的数字所对应的权限啦。

一个详细的对应表格可以见下图
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-30-072502.png)

**简单来说r:4,w:2,x:1**

>1. 这里的进制转换不一定正确，8进制涉及到更多位数的时候这样转换就是错误的！
>2. 只需要理解这样的一个过程，实际上使用的时候可以粗暴的这样更改也可以使用其他的方式去指定修改某个特定的权限。要进行这样的操作的话可以更进一步的了解chmod命令（不过这会比较麻烦）
>3. `chmod 777 xxx` 表示赋予某个文件所有的权限，三个7的对应关系同三类用户是相对应的
`
### 如何修改系统新建文件的默认权限

这里就需要引入 `umask`

`umask`在命令行输入后会得到如图这样的一个结果：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-30-073049.png)
可以看到是022。

那么022是什么意思呢，嘿嘿其实就是刚刚提到的东西————一个八进制的代表权限的数字。只不过呢，这个022是用于 **屏蔽**的。

什么个意思呢。

首先得搞清楚一个东西，对于文件和目录它两兄弟的全权限是不一样的（虽然文件也可以赋予执行的权限o(￣▽￣)ｄ）。linux认为文件的全权限就是 `rw-` ，而目录的全权限就是 `rwx` 。**这两个对于的数字就是 6 和 7**

这样对于文件和目录而言，所有群组赋予全权限的话便是 `666` 和`777`。 

到这里，umask的作用就发挥了，你创建一个新的文件，其权限就是：`666 - 022 = 644`，**这里进行的不是减法，而是对应位相减！**；对应的，新创建一个文件夹，其权限是`777 - 022= 755`

现在！ 创建一个一个文件和文件夹试试！ 结果如图！
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-30-073754.png)
可以看到左边的权限结果。

可以对照表格看看是不是`644` = `rw-r--r--`；`755` = `rwxr-xr-x`！

到这里理解了umask后，就是如何修改umask 的值了

**很简单**

只需要`umask 新的8进制数字` 就好了。 比如`umask 000`🥲


### 如何设置共享文件夹

目前还未学习！！！



## 包管理
包管理系统（package management system,PMS）是linux上用来进行软件安装、管理和删除的命令行工具。

对于常用的linux的两类：Debian和Red Hat分别使用的是不同的PMS，Red Hat的PMS是`rpm` 而 Debian则是用`dpkq`。两者使用上略微有所差异。但是主要的功能是类似的。
>PMS是帮助系统与储存有软件包的服务器进行检索、下载所需要的软件的工具。其中这样的服务器称为 仓库（reposity）
>使用PMS也会安装目标软件相关的各类依赖

主流的linux系统的发行版是centos和ubuntu，前者是基于redhat而后者是基于Debian。

需要注意的一点是，这两个命令并非全PMS，现在很多发行版使用的很多都是基于这两个命令的工具。
如ubuntu使用的是`aptitud`和`apt-get`等；而centos使用的是`yum`

由于我的服务器是centos，我只记录了`yum`的一系列常用命令，而不对其中的东西过多记录。

### `yum`常用命令

#### 查询功能
`yum list installed` 列出已经安装的所有包，可以配合`more` 使用`yum list installed | more`
>`yum list updates` 可以查询可以更新的一系列包，如果要更新他们，则采用`yum update` or `yum update packageName`

`yum list packageName` 可以查询某个特定包的功能

`yum provides fileName` **可以查询某个文件是从哪个软件提供的，仅限于3个repo：base，updates和installed三个仓库中有的软件！**

#### 安装软件
`yum`也可以从本地安装某个rpm文件，使用`yum localinstall packageName.rpm` 就好了

当然，从repo中安装只需要使用`yum install packageName`就好了。

#### 卸载软件
`yum remove packageName`直接删除某个软件，不删除配置文件和数据文件等
`yum erase packageName` 删除某个软件和它的所有文件（完整的删除！）

#### 其他功能

1. 查看某个软件使用的依赖关系：`yum deplist packageName` 
2. 查看当前的repo信息：`yum repolist`
>repo的设置储存在`/etc/yum.repos.d/`这个目录下，**可以到某些提供repo的站点去获取url以及秘钥，然后添加进去！** 通常这些站点会给出详细步骤，如：rmpfusion.org


### 从源码安装软件

一般软件开发者会在github上放上自己的源码，可以通过github下载。

下载的方式有很多，比如：电脑下载后通过ssh等传输的方式传给服务器；wget、curl等直接下载等等。

不管如何下载，**第一步便是获取得到归档后的安装包**，随后便通过`tar` 进行解压。
>如果是tar.gz `tar -zxvf fileName.tar.gz`
>如果没有用gz压缩而只是归档后的`tar -xvf fileName.tar`

完成解压后会得到一个**目录**，`cd`到这个目录后会看到许多的文件，其中重要的有：`README`、`configure`以及`make`这三个文件
>`README`**记录了开发者，关于如何安装这个软件的一系列介绍，也就是用户必须知道的一些信息**。
>不过一个标准的流程仍然是下面提到的，**通常README中还会有其他的要求安装的东西**，一般这些是该软件的依赖包，**因此从源码安装需要注意该软件的依赖**

首先执行`./configure` ，也就是运行目录下的`configure`文件，这个命令的作用是：
1. 检查系统是否有其**需要的编译器**
2. **检查系统是否已经具备其需要的各种依赖包**
3. **如果报错**，请仔细阅读报错文件，**一般会告诉你缺少什么编译器或者缺失什么依赖包！**

然后下一步就是执行`make`，这一步就是进行编译
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-31-073752.png)
`make`命令结束后，软件其实就已经安装好了，只不过呢，并没有配置到系统的环境变量中。如果需要使用你还得在命令行中指定该软件的位置来调用。

因此最后一步的`make install`就是配置该软件到环境变量以及其他的一些东西。



## 文本文件处理

### sed编辑器
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-105459.png)
sed处理数据的一个过程：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-105610.png)
`sed` 的使用很简单：`sed options scripts file`

options 指定你使用的是手写的scripts还是一个文件。 这是什么意思呢

scripts其实就是刚刚写到的 **预先提供的一组规则**。 这个规则 可以使用`'s/big/big test'`或者`'s/big/big test/;s/blue/green/'`这样的规则  也可以是写入到文件中，如下图
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-110036.png)。

关于这样的 **规则** 是怎么样的，在后面会介绍。

options:
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-110217.png)

也就是 可以这样写 `cat test.txt | sed -f script.sed` 或者`sed -e 's/brown/green/; s/dog/cat/' data1.txt`

>注意：建议是把sed编辑器的脚本 文件用.sed 结尾，避免和其他文件搞混淆~

### gawk编辑器

和sed编辑器相比，gawk的规则更为丰富，可以实现 变量定义 和判断逻辑等 更利于编程实现。
>使用gawk可以做的这样一些事情：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-115733.png)

基本命令`gawk options program file`
options:
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-115814.png)

不过一般会把相应的 规则 写入到文件中（类似sed的做法一样）。 除非 很简单的规则 🤣

操作上和sed是一样的。 只不过规则上有所差异

先说 直接在命令行上的写法
`gawk -F :'{print $1}' /etc/passwd` 

这样便会从`/etc/passwd`这个文件中读取数据，这里就涉及到 下面的一些内容![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-15-120131.png)

其实读完这些文字，就知道 **怎么把一行分成数据字段** 是最重要的。gawk采用 字段分隔符，默认是空白或者制表符。
>如果要修改，可以直接在命令行 指定参数 `-F :` 以`:`为分隔符;
>也可以在脚本中 添加`IF=":"` 这个下面会说

这里的`{}`定义了一个程序，程序也就是每一次对一行会执行的任务。 `print`的意思就不解释了~
在`{}`可以写多个命令，比如：`gawk -F : '{print $1 ;print " \t" ;print $7 }' /etc/passwd`
>`;`也就是换行的意思~

自然，当程序较为复杂的时候在命令行中写入就比较麻烦。

这个时候就可以写入到文本中，如下图：
``` shell
BEGIN{
print "The latest list of Users and shells"
print "UserID \t Shell"
print "----- \t -----"
FS=":"
}
{
print $1 " \t " $7
}
END {
print "This concludes ths listing"
}
```
>`BEGIN {}` 表示在整个文本开头的时候才会执行的程序；`END {}` 同理

下面将会细讲语法~

## 链接
- `ln`命令

- 软连接
`ln -s /pubdata/NGS ~/`
- 硬连接
`ln source target`