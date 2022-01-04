# ssh简单介绍以及免密登录的原理与过程
SSH全名Secure Socket Shell，安全外壳传输协议。专为远程登录会话和其他网络服务提供安全性的协议。
关于SSH起源以及中间人攻击等知识可以参见：
https://www.cnblogs.com/lisenlin/p/10541363.html
https://www.cnblogs.com/machangwei-8/p/10352725.html
等文章

这里主要是介绍似乎是目前最常用的一种方式
首先需要理清楚，用户(client)和服务器(server)这两个东西。顾名思义，用户就是咱们自己的电脑，而服务器是远程的电脑，虽然二者可以反过来，单在这里暂且作为抽象概念固定住。我们是通过自己的电脑（用户）去连接远程的服务器。

通常我们是通过http等协议进行，有时也会采用ssh进行连接。但是无论用哪一种方式我们都绕不开一个过程————输入密码。

对于SSH的传输方式。首先是这样的一个过程

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-124608.png)
>此图来源于https://www.jianshu.com/p/33461b619d53

也就是client 首先输入 server中一个用户的用户名和密码这样一对值

然后通过一个秘钥A（其实就是一个词典进行加密的操作）生成一组加密后的对应的一对值

随手这样的被加密的值又传入到server中，然后server用秘钥A进行解密获得这个用户的用户名和密码，如果正确就登录上去啦。

这是最简单的一个方式，考虑到中间人攻击等安全问题，因此单独一个秘钥A不安全！

那么怎么办呢，有人就采用这样的方式

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-125253.png)
>来源同上

其实就是server生成一对公钥和私钥，在每一次client请求登录的时候就会把公钥发给client，client就通过这个公钥对数据进行加密然后发送到server中，server通过私钥进行解密然后登录就好了。**这也被叫做非对称加密登录**

>这里就可以解释所谓的中间人攻击是什么，就是client发出请求登录的时候被hack1（一个模拟server的终端）拦截下来了，然后发送一个hack1的公钥给client进行加密，client这边也不知道这个公钥是对还是不对（这个时候目前的解决就是会提示如下图的一个东西，需要client去确认是否接受这个公钥，但是由于没有类似HTTP认真的这种公钥，因为SSH的公钥和私钥都是自己随意生成的……，所以这个地方似乎是存在安全性问题的），如果憨憨的按照这个去加密然后传到hack1这里，hack1就可以使用私钥进行解密获得server的一个账号密码，导致server可能会被攻击！
>
>这个是受到公钥后会有的一个提示：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-125810.png)
>中间人攻击的一个示意图
>![中间人攻击原理](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-125750.png)

SSH的一个基本原理就如上了
不过关于这个安全性现在怎么解决的问题，我并没有太多了解。

然后呢下一个重点就是如何跳过密码验证直接登录，因为每一次我们要登录到一个用户就需要输入密码，这对于我们想远程让服务器执行某个脚本的时候就显得略微麻烦。

#### 基于公钥的认定
这个时候其实和之前的流程有所区别，之前是server生成了一对公私钥，然后公钥丢给client进行加密，然后server进行解密来登录

这个基于公钥的认定的方式呢，则有所区别。client生成公私钥然后存放在本地。

然后client手动把公钥上传到server中用以后续登录的时候使用

然后正经的登录流程就开始了

首先client发出**登录请求**，当server收到后，就生成一个**随机数R**,然后用公钥加密，发给client（是不是和正常的SSH有点像？client按照公钥加密登录信息，然后发给server。这里就反过来了server用公钥加密一个随机数R，发给client）

client收到后呢就用自己的私钥**解密得到R**，然后使用MD5来对R和SessionKey（这个应该是代表这一次登录请求所产生的一个数字）生成一个Digest1。（简单说就是用R再加密一次，为什么不直接发过去呢，应该是出于安全性的考虑吧……，不清楚具体的原因）

server收到这个Digest1后呢，就用自己的随机数R和这个SessionKey，进行同样的一个MD5算法进行Digest2的生成，然后比较两个是否相同，相同则说明没问题。（client不直接返回R和server的R进行比较的一个原因应该是保证信息的安全吧……）

整个流程如下图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-131609.png)
>来源同上

所以整个流程就是这样如果实际操作就是这样

client上生成一对公钥和秘钥（有多种算法 RSA, DSA, ECDSA, or EdDSA 可以生成，这里选择使用RSA，因为是`ssh-keygen`的默认方式。）然后上传到server。
`ssh-keygen`生成公钥和秘钥，一般直接enter，就可以了不需要设置其他的东西（设置其他东西是为了更加的安全！），然后输出结果会显示你的结果存放的位置，通常是在`~/.ssh/`下面，会有
    1. `id_rsa`这个是私钥
    2. `id_rsa.pub`这个是公钥

>如果之前生成过的话，就可以不用再走这一步了！！因为github等可能用的就是这个公钥，如果再生成一次的话github上留着的公钥就不能用了~~~~
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-28-132805.png)


然后上传公钥到服务器上，`ssh-copy-id userName@ip`可以把rsa的公钥上传上去。

到这里应该就可以通过`ssh userName@ip`直接登录上去了！


本文主要参考该文章：
https://www.jianshu.com/p/33461b619d53


讲完了这里其实可以随便简单讲一讲github的配置方式

## 配置github，合理的使用git工具 {3}
这里配置github其实也就是配置git使得你的电脑(client)可以和github（client）进行正常的友好的交流~~~~

github的通讯其实也是SSH，也是基于公钥的认定的方式。

github里面你的用户设置里，找到`SSH and GPG keys`然后在里面的`SSHkeys`创建一个新的key，然后把你电脑(client)里的id_rsa.pub里面的东西也就是公钥复制粘贴过去，然后随便给个title保存好就行了。

然后在命令行 `ssh -T git@github.com`一下，其实就是连接一次github（server）看看可以吗，如果提示
`Hi xxx ! You've successfully authenticated, but GitHub does not provide shell access.`则说明成功了

这个时候去试试`git clone xxx` 一下看看是否work了。

关于git的配置可以见菜鸟教程的Git配置部分（**在这个连接的文章的下半部分**）：https://www.runoob.com/git/git-install-setup.html 

#### git初始化操作
初始化一个Git仓库，使用`git init`命令。

添加文件到Git仓库，分两步：

使用命令`git add <file>`，注意，可反复多次使用，添加多个文件；
使用命令`git commit -m <message>`。

这样就完成了创建一个仓库，并且添加文件以及commit的操作

下一次你修改了其中的文件后 只需要`git add`一下就好了，然后便可以 `git commit -m "备注信息"`这样你的git分布式仓库里面就会储存好这一次的修改了。

如果某天你的朋友帮助修改了你的某个文件，那么你就需要知道你朋友修改了那些地方。

`git status` 就可以显示那些文件被修改过。

知道被修改过还不够呀，还需要知道那些文件被修改了什么内容

这个时候可以用`git diff xxx`就可以显示本地尚未上传的文件 与仓库里面的该文件的差异

再过了一段时间，你不小心删除掉了你的一个文件，哎呀！这糟糕了。怎么办呢？

git既然储存了你每一次的修改，那么自然就可以**回溯**。

`git log`可以查看你过去的**提交信息**，`git log --pretty=oneline` 可以**只显示每一次的提交的信息**

你大概知道你之前提交过的内容之后便可以开始 回溯到哪一个版本啦。

`git reset --hard HEAD` 表示回溯到上次提交的版本，`HEAD^`上上个版本，`HEAD~100`表示之前的第100个版本

此外偶尔的还想修改一下已经add的文件，可能会有这样几个场景。

场景1：当你改乱了工作区某个文件的内容，想直接丢弃工作区的修改时，用命令git checkout -- file。

场景2：当你不但改乱了工作区某个文件的内容，还添加到了暂存区时，想丢弃修改，分两步，第一步用命令git reset HEAD <file>，就回到了场景1，第二步按场景1操作。

场景3：已经提交了不合适的修改到版本库时，想要撤销本次提交，参考版本回退一节，不过前提是没有推送到远程库。

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-09-20-081902.png)

