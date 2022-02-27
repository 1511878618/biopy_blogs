## 命令行输入的传递
可以采用`getopt`模块或者`argparse`这两个模块来实现。
前者是类似bash shell脚本的传递方式；后者是python 3.2版本新增加的模块，用于支持这一功能。

现在都使用`argparse`模块来完成命令行输入的处理
exapmle:
``` python
import argparse

#创建一个argparase
parser = argparse.ArgumentParser()

# 添加位置参数
parser.add_argument("x", type=int, help="一个普通的位置参数，类型为int")

# 添加可选参数
parser.add_argument("-f", "--flag", action="store_true", help="一个普通的可选参数，记录flag值")
## action="count"，会统计特定选项的次数。比如：-v 时，args.v 的值为1；-vv 则为2，而由于设置了default为0，所以如果没有-v的时候为被赋值为0！
parser.add_argument("-v", "--verbosity", action="count", default=0, 
                    help="increase output verbosity")

# 添加互相冲突的参数
# -v 和 -q 只能二选一，或者都不出现。
group = parser.add_mutually_exclusive_group()

## action="store_true"，当使用-v 或者-q的时候，args.v就会被赋值为True，如果不指定这个参数就是False，如果给它指定某个值就会报错。
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

# 调用argparse
# args储存了所有的参数，可以直接调用属性的方法来调用
args = parser.parse_args(description="这是一个简单的程序")
# 直接args.x 就可以调用到 x这个位置参数的值；同样args.f 调用--flag这个可选参数的值。
print(f"输入的位置参数是x，平方为：{args.x ** 2}")

# 参考：https://docs.python.org/zh-cn/3/howto/argparse.html#id1

```


大致上分为这样几个步骤：
1. `parser = argparse.ArgumentParser(description='xxxx')`首先生成`ArgumentParser`，也就是用于解析命令行的输入的一个类；其中`description`是help文档中关于该脚本的介绍文字。
   1. `prog=xxx` xxx是程序名，会在后续的文字中以这个名称来出现；`%(prog)s` 代表程序名。
   2. `description="xxxx"`会在help文档中显示的一段描述该程序功能的文字；`description="%(prog)s is a useful tool for detect RNA splice sites."`
2. **然后便是添加各种参数**，通过`parser.add_argument('--name',default='xxx',)`来添加各种各样的参数，以及参数相关的设置。需要注意的是，开头两个位置参数会决定创建的参数是什么类型：比如：1）创建一个位置参数`parser.add_argument('test')`；2）`parser.add_argument('-t', '--test')` 会创建一个可选参数
   1. `default=''`：**是没有设置值情况下的默认参数**
   2. `required=True`：**表示这个参数是否一定需要设置**；True or False
   3. `type=int`：**输入的文本会被转化成什么样的类型**；`type=int;type=str`
   4. `choices=['alexnet', 'vgg']`；**输入的参数只能位于其中**，否则会报错
   5. `help=''` **指定参数的说明信息**
   6. `dest='xxx'`**把这个参数赋值给变量 xxx**，也就是parser.parse_args()会返回包含xxx的属性的一个对象
   7. `nargs = '+'`**这个参数后面可以跟的输入的个数**；`+`表示至少1个，`*`至少0个，`?`0或者1个。；并且后续仍然可以输入其他的参数~
   8. `metavar` 仅改变 显示的名称；parse_args() 对象的属性名称仍然会由 dest 值确定。
3. 然后就是解析获得其中的参数`name=parser.parse_args().name`。其中之前添加参数时所赋予的命令行参数名，会变成这个时候的属性（会自动去掉--）
4. 然后就是你的核心代码啦~


最后包裹成`getParser()`的形式方便管理

``` python
import argparse

def getParser():
	parser = argparse.ArgumentParser(description="使用scihub的api进行文献批量下载")
	parser.add_argument('--input',default='input.txt',required=True,type=str,help='指定输入文件',nargs='+')
	parser.add_argument('--model',required=True,type=str,choices=['a','b'],help='运行的模式')
	return parser

if __name__ == '__main__':
	parser = getParser()
	args = parser.parse_args()
	inputFile = args.input
	
	print('using File: {}'.format(inputFile))

```

>推荐阅读的博客：https://vra.github.io/2017/12/02/argparse-usage/
>
>官方教程：https://docs.python.org/zh-cn/3/howto/argparse.html#id1


### 添加输入输出文件
``` python 
parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
```