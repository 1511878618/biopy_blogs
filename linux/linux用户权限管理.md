## 用户管理
`usermod`

- `usermod -aG groupname username` 给username追加groupname这个组别；`-a, --append`添加组。必须和`-G groupnams`一起使用  
  - `usermod -a xtf -G A -G B` `-a`指定用户，`-G`指定组名
  - 修改组名后，要重新登录才生效？
  - [更多关于usermod](https://www.howtoing.com/usermod-command-examples/)

##添加组、用户
- `groupadd 组名`
- `useradd 用户名`
  -  `useradd -g test phpq `新建用户同时增加工作组

## 改变拥有者
- `chgrp`改变文件所属群组
  - `chgrp -hR A projectA/` 
- `chown`改变文件拥有者
  - 


- `chmod`改变文件的权限
  - `chmod 750 -R` , `-R`递归进行；其中：r:4,w:2,x:1
  - `chmod a+r -R` ,`a+r`中第一个字符表示对应的类型，有：u（用户）,g（同组）,o（其他）,a （全部）;第二个字符可以是`+`或者`-` 表示添加或者删除某个权限；第三个是字符是权限：rwx，三者之一。


