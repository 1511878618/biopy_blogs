# awk
对于一个文件，采用awk打开，会把**每一行当做一个记录**，而对于每一行也就是每一个**记录**中的字段又会根据一个字段分隔符（变量是`FS`）把字段分割成多个域(fields)。

每一次会对一个记录进行操作，进行的操作取决于你输入的命令。

而在每一个记录里面，每一个fields，也会有一个变量名（从0到n，`$n`）可以来调用。

其中，默认的记录分隔符是 **换行符**；而域的分割符是**空格**。要修改这二者在`awk 'BEGIN{FS="新的域分隔符",RS="新的记录分隔符"}'`。其中`BEGIN{}`表示在一开始会进行的操作。

awk的命令的写法呢 `'{程序1} {程序2}'`，这样的一个完整的awk语句可以是放在文本（也就是脚本）中的也可以是命令行输入。`{}`包裹的部分会在每一个记录执行。

而在其中还有一类特殊的`{}`，可以再开头和结尾使用：`BEGIN{}`和`END{}`。

此外在`{}`之中可以调用多个函数每一个函数之间的分割用`;`，比如`{print $1;print $2}`。

那么最大的问题就是怎么写这样的**程序或者说脚本**。在awk中可以实现的功能还是较为丰富的，可以实现 定义变量、数字计算以及逻辑判断等。

当然最为重要的是能够找到数据中符合某一个pattern的记录，然后进行一系列的操作。这一点在生信中才是最为重要的操作。 一个简单的例子：`awk '$2 ~ /(GTG)+/ {print $1}' test.txt`。第一个域是DNA序列的名称，第二个域是序列。[更多的awk在NGS中的使用例子](http://userweb.eng.gla.ac.uk/umer.ijaz/bioinformatics/linux.html)
>[onelineAwk](http://www.pement.org/awk/awk1line.txt)

## 自有变量

- 数字变量`$n`，n表示每一行的第几个field，field的区分使用 分隔符 定义的。
- `NF` **NF表示浏览的这个记录的域的个数**，是个数字。通常使用是`$NF`，也就是相当于取这个这个数字对应的变量
- `NR`**已经处理的输入的记录数**
- `FNR`**当前文件中已经处理的输入的记录数**

二者的区别在只读取单个文件的时候区别不显著，而在读入多个文件的时候就显著差异了。

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-070809.png)


![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-065223.png)
### 域分隔符的修改
- `FIELDWIDTHS` 变量允许你不依靠字段分割符来读取记录 `awk 'BEGIN{FIELDWIDTHS="3 3 3 3"}{print $1 ,$NF}' test.tsv`
- `FS` 输入字段的分隔符
- `OFS` 输出字段的分隔符

### 记录分隔符
通常awk会把换行符当做一个新纪录的分隔符。

- `RS` 输入数据的一个记录的分隔符
- `ORS` 输出数据的一个记录的分隔符
  - `{print $1,$2}`中的`,`会被自动解释成`ORS`

>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-063503.png)比如这样的一个文本，实际上的 记录与记录之间的分隔符是一个**空白行**，fields之间的分割则是**换行符**。
>`awk 'BEGIN{FS="\n";RS=""}{print $1,$4}' test.txt` 这样便可以比较好的format输出。![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-063654.png)

### 引用系统变量
也可以在awk中引用系统的全局变量
>查看系统的全局变量可以用`printenv` 或者查阅 <<linux笔记>> 中关于全局变量的部分

直接输出 HOME变量`awk 'BEGIN{print ENVIRON["HOME"]}'`
或者赋值给一个 新的变量 `awk 'BEGIN{a=ENVIRON["HOME"]}'`

## 变量
定义变量和shell没有区别，都是`name=''`或者`id=3`这样的方式。只是`=`左右可以有空格。

### 关联数组

这个是一个比较特殊的数组，在python中的list，shell中的数组的定义其实都是手动输入，然后索引是按照一个从0 开始的数字去索引，内部是有一定顺序的。

但是awk中的关联数组就比较奇特。它的定义是你手动给它其中的每一个元素一个索引，这个索引不具有任何顺序，仅仅是索引。与其说它是数组，倒不如说它有点类似的py中的 **字典**。

```
var[1]=5
var[2]=4
var[10]=2
var["hi"]=3
```

如果用[for循环](#循环语句)去迭代它的话，似乎是从最后添加的元素往前面迭代，并且迭代出来的是**它的索引**

如果要删除其中的一个变量，则可以用`delete var[2]`就可以了。

## BEGIN和END

`awk 'BEGIN{print "This is the beginning"} {print NF} END {print "This is the End"}' fileName` 其中，BEGIN后跟的命令会在一开头显示，END则是在结尾处显示

这样的代码：
`awk 'BEGIN{print "This is the beginning"}{print $1 "," $2} END{print "-----------"}' test.tsv`

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-20-140253.png)

可以看到BEGIN后跟的命令会在一开头显示，END则是在结尾处显示。


## 结构化语句

### 循环语句

在这里面也可以使用for循环。不过在这awk中for循环仅仅限与**关联数组**。

``` 
'BEGIN{
var[1]=3
var[4]=4
var[5]=8
for (i in var)
{
print "index is ",i,"--values:",var[i]
}
}'
```

**迭代出来的是它的索引而非具体的值**

### 判断

#### if判断
条件判断简略化的写法：

- `awk '{print (Condition) ? 为是时输出的内容 : 为否时输出的内容}'`
- `awk '{print (pattern) ? 为是时输出的内容 : 为否时输出的内容}'`

>其中的`()`可以省略

如：`awk '{print (length($2) > 14) ? $0">14" : $0"<=14"}' test.tsv`
>条件判断部分会用到各种内置函数，对于我们生信er而言最多的可能就是判断序列的长度之类的字符串的函数，如这里的`length`。[内置函数的介绍](https://www.runoob.com/w3cnote/awk-built-in-functions.html)

> `print`和`printf`的区别，`print`会在后面自动添加一个换行符；而`printf`则不会。

这样的写法其实只是if的一个简化版本，虽然这样的写法用的时候会更多。

**if判断的的完整写法：** `awk '{if (condition/pattern) {func}}'`

- `if (condition) {功能}` 当condition成立的时候执行功能
- `awk 'if (condition/pattern) {func} else {func}'`

一个例子，如何把fasta文件转化成这样一个文件：第一个域是序列name，第二个域是序列。域分隔符是 制表符(`\t`)
`awk '{if (/^>/) {gsub(">","",$0);printf $0"\t"} else {printf $0 "\n"}}' test.fa`

结果：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-131406.png)

>gsub()是一个内置函数，其作用![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-21-131801.png)

当然这个写法还可以再精简一点：`awk '{if (/^>/) {gsub(">","",$0);printf $0 "\t";getline;print $0 } }' test.fa`

>这里就引入了另外一个内置函数：`getline`。其功能很简单就是读取下一行的数据。在getline之前，awk处理的是当前行的数据，而getline之后的就变成了下一行的数据，会相应的更新内置变量；此外`getline < "filename"` 可以一个文件中读取，并且重置相应的变量。因此该函数最好在`BEGIN`使用，否则会影响当前的读取。[更多关于getline的知识](http://www.west999.com/info/html/caozuoxitong/Linux/20191123/4663019.html)

#### while循环
`{while(condition) {动作}}`

一个比较好的例子
`'BEGIN{while((getline k <"IDs.txt")>0){i[k]=1}}'`

getline 函数默认是会返回一个状态码，对linux有一定了解的应该就清楚是什么。不知道的话就当做getline成功读取的时候就会返回一个状态码1，然后呢while循环只要收到状态码就会继续下去，这个时候`i[k]=1`就会运行。

这里的`while( (getline k<"IDs.txt">))` 表示的就是从IDs.txt文件中不停的读取文件，如果没有数据了getline就会返回一个非正数的状态码，while就会停止。 而while运行的时候其实就是不停的在给 关联数组i进行一个赋值，把IDs.txt中的每一行作为索引，而value就是1。为什么这么做？ 很简单，因为后面不管是读取还是for循环 读取到的都是idx，而不是value，要取到value就得`i[idx]`。这个地方的思路和py之类的处理是不同的。
一个复杂的例子如下：
`awk '{if (/^>/) {gsub(">","",$0);printf $0 "\t";getline;print $0 } }' test.fa | awk 'BEGIN{while ( (getline k< "IDs.txt")>0) {i[k]=1};FS="\t" } {if (i[$1]) {print $0} }'`

这行代码干的事情是就比较复杂了。

## 数值计算

- 可以进行简单的数学运算。`awk 'BEGIN{x=3; y=x**2;z=x/2;t=x/22;print "y="y,"z="z,"t="t }'`

- 支持浮点运算？

## 搜索模式

除了之前提到的进行逻辑结构判断等操作，更为重要的是寻找一个记录中符合某个 pattern的域或者记录本身，然后进行各种操作。这才是生信er需要搞懂的。

`awk '$2 ~ /pattern/ {function}' test.txt` 表示在每一个记录的**第二个域**中查找符合**某个pattern**的数据，然后进行**function**所定义的操作。`~`表示**匹配操作** `!~` 则是**取反匹配**





