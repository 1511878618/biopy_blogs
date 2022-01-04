
# pandoc

是一个格式转化工具
安装请前往[pandoc](https://pandoc.org)安装。

pandoc并不是一个图形化界面的软件，所以要使用它请打开命令行界面。

在目标目录下使用`pandoc xxxxx`的命令才可以进行格式转化。
[支持的格式](https://pandoc.org/MANUAL.html)

一个简单的使用
`pandoc test1.md -f markdown -t latex -s -o test1.tex`
- `-f `指定输入文件的格式
- `-t` 指定输出文件的格式
- `-o` 指定输出文件的名称
- `-s` pandoc生成一个文档片段。要生成独立文档（例如，包含<head>和<body>的有效HTML文件），请用-s或--standalone标志：