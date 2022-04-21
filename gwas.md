# 全基因组关联分析统计学方法

目前主流的似乎是 **单基因模型**，但是polygenetic model可以衡量多基因的影响

**GWAS目前都是针对单个SNP进行回归分析**，**几乎没有用全部SNP做多元回归的**

- 连续性状
  - assoc 用的是T和F检验，可以在r中直接用`lm()`实现，实际上就是把每个SNP和表型值进行线性回归，然后计算对应的$\beta$值
  - linear 也是简单的线性回归做
- 离散型性状
  - assoc 用的是卡方检验，对SNP进行各种编码的方式
  - logistic 

**但是其实也是多元回归**

为什么这么说呢？目前最常用的GLM（线性混合模型），其实后面也加了一堆协变量。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-123356.png)

如：[yangjian2019](https://www.nature.com/articles/s41588-019-0530-8)等人发表了fastGWA
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-124935.png)
>就直接利用部分感兴趣的SNP + 协变量进行回归分析


而这里的统计学检验的目的有：
1. 检验所有参数是否全为0 ，也就是F检验
2. 检验各个参数的效应是否是真正的显著，通常是t检验完成
3. 检验各个参数之间的相互作用

而通常我们做的就是一个SNP+协变量然后做线性回归然后检验；然后换下一个SNP和这些协变量进行检验

## 实验验证plink的算法

- 选用的数据：随便选数据啦，反正是验证结果是否一致的~

## 使用**卡方检验**，`--assoc`参数进行

### 卡方检验的原理

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-085953.png)

大致上就是这样，可以自行百度 卡方检验

#### plink数据格式解释

- 在plink中，**默认A1为次等位基因，而A2为主等位基因**
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-080354.png)
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-080659.png)

- plink中，如果表型为1为control和2为case，则说明是离散型表型。其余情况为连续性表型
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-080848.png)

有了这些过后，我们才可以更好的理解plink在进行什么统计学分析

假设我们现在的数据集中表型是用1和2编码的。也就是说 可以进行卡方检验的方式。

plink中`--assoc` 会进行卡方检验
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-081115.png)

`--model`则可以指定编码的方式

##### plink可以产生的几种编码
需要注意的是，plink都是以次等位基因作为标准，我也不知道为啥……

- `--recode A` ![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-103144.png)
- `--recode AD` ![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-103048.png)
对于上面两个，产生的结果是`.raw`文件，可以看plink关于这类文件的注释
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-103317.png)

- `--recode 01`
- `--recode 12`


#### 卡方检验

##### `--assoc`
使用的似乎是下面`--model `中的allelic的方式做出来的，
也就是有次等位基因的为1，无次等位基因的为0的方式

##### `--model`
首先我们先看看plink采用几种不同的编码模型进行卡方检验的结果，要使用`--model`，输出的文件是`.model`

结果中，看起来是会执行几种模型的检验，并且结果汇总在一起。

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-083106.png)

.model文件的解释

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-081910.png)

>其中关于geno、trend、allelic、dom、rec的解释
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-083036.png)

- 
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-083407.png)
- GENO 是以次等位基因为主的加性模型的方式编码SNP，对应的`plink --recode A`可以输出这样的格式的数据，然后导入R进行chitest
- ALLELIC 则是含有次等位基因的就为1，没有为0，也就是A1 ->0 A2 -> 1 `--recode 01`
- DOM 有次等位基因的基因型为1 
- REC 只有纯合的次等位基因型为1

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-083614.png)

至于TREND则看起来是基于**Cochran-Armitage trend test**这个进行的

**总结起来就是`--model` 和`--assoc`是构建列联表然后进行卡方检验或者进行fisher检验，是对每一个SNP都进行一遍的。**

>不过似乎在r中利用对应的数据做出来的结果和plink的结果有差异~
>怎么去做呢？ 应该就是`--recode [A|01]`这样子，把数据编码成对应的类型后，读入R调用卡方检验或者fisher检验的函数去执行。我做出来有差异就很奇怪了……

##### 二者对比
见下图，可以看到`--assoc`是用的`--model`中的`allelic`的方式，二者的结果是一致的。

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-085640.png)


### 简单线性回归模型

#### 原理
我们可以认为真实的表型是$\bold{y}$，而我们的模型拟合出来的是$\bold{\hat{y}}$

通常我们的$\bold{\hat{y}}$与$\bold{y}$之间的差异是由随机误差$\epsilon$引起的，我们假定这个误差服从正态分布。

从而我们可以认为真实的表型
$y = \bold{x^T} \bold{\beta} + \epsilon$，其中$x_{m\times1}$为列向量，是一个个体的SNP型，$\beta_{m\times1}$是对应的SNP产生的效应值。$\epsilon \sim N(0, \sigma^2)$

对于所有数据可以写成：$\bold{y} = \bold{X^T} \mathbf{\beta} + \mathbb{\epsilon}$，这里$\epsilon \sim N(0, \sigma^2 I_n)$，$X_{m\times n}$
是所有个体的SNP信息组成的矩阵。

用最小二乘法可以求解出$\beta = (\bold{X^T}\bold{X})^{-1}\bold{X^T}\bold{y}$
这样我们的$\bold{\hat{y}} = \bold{X^T} \mathbf{\beta}$

>需要注意的是我们求出的$\beta$是估计值![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-IMG_AC7B4E4118BC-1.jpeg)

##### F检验
求出$\beta$下一步就是进行统计学检验。首先进行F检验

F检验的目的是为了验证求出的$\beta$是否是显著的，也就是说我们可以给出null假设为：$\beta = 0$ ；备择假设为$\beta_j \ne 0, j \in n$。也就是如果拒绝原假设则说明$\beta$里面至少有一个不为0。那么我就可以进行t检验去查看每一个SNP在其中是否是显著必须的。

F检验怎么进行呢？见下图：

这是关于笔记中的数据矩阵的一些解释
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-IMG_C0CEF19BD58C-1.jpeg)

计算过程：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-IMG_B822A5718E1A-1.jpeg)
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-IMG_6EAF528D205D-1.jpeg)
>这里的n为样本总数，$p = m + 1$，$m$是SNP的个数。计算MSR和MSE的时候，分母是对应的自由度。

##### t检验
t检验的目的就是在前面已经知道$\beta$是显著的时候，我们需要搞明白$\beta_i$是否为显著的。

而t检验，可以对单个SNP进行检验，也可以对一组SNP进行检验。

- 单个SNP进行检验的方式


$H0:\beta_i = 0$ ； $H1:\beta_i \neq 0$ 

$t_0 = \frac{\hat{\beta_i}}{Se(\beta_i)} \in t(n-p)$
>前面提到了$D(\hat{\beta}) = \sigma^2 (\bold{X^T}\bold{X})^{-1}$，所以$Se(\beta_i) = \sigma^2 (\bold{X^T}\bold{X})^{-1}_{i,i}$

>也就是计算了**协方差矩阵**

笔记：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-IMG_9F81E32ECEEA-1.jpeg)

- 对多个参数进行t检验的方式

目前还在学习~


#### plink中的操作
- `--assoc `会进行一元线性回归，`--covar` 可以添加协变量

##### `--assoc`
这里随机生成了一组表型作为数据来回归

`plink --bfile snp --assoc --pheno pheno.txt --out snp_quantitative_assoc`

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-110448.png)其结果如图

这里只有t检验的结果，是因为在单元的时候t检验和f检验的结果是等价的。

在R中复现这一过程，使用`recode A`获得加性模型的编码方式，输入r，a1基因仍然是次等位基因。

用lm去做回归针对rs3131972进行，结果如图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-110756.png)
可以看到结果是一样的。

加上`qt-means` 参数后，看起来是给出加性模型中每一个情况对应的$\beta$值的

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-111732.png)

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-111814.png)

>**不理解这里的mean和方差是什么意思以及怎么计算出来的**

- `--gxe --covar cov.txt`可以添加协变量

Quantitative trait interaction (GxE)，--gex是考虑交互作用

也就是：$y = SNP_i * beta_i + c_i * w_i$，这里的$c_i$就是刚刚添加进来的协变量。

结果就成：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-114702.png)
z和p就是衡量交互作用的

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-114838.png)

在R中进行`mod3 <- lm(fake_pheno$V3 ~ a$rs3131972_A * a$SEX)`

结果：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-115855.png)

对比：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-120118.png)

**似乎差距很大！**，不知道是啥原因，不过应该就是这样做的，可能是

##### `--linear` 

仍然跑的是一元线性回归，对每一个SNP都跑了一遍
结果：

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-10-120358.png)

>1. 但是为什么很少做全部SNP一起回归的模型，一个解释是：样本量远少于SNP量，就导致$\bold{X^T}\bold{X}$无法满秩，就不存在可逆（可以用[广义伪逆](https://zh.wikipedia.org/wiki/广义逆阵)来解决）。
>2. 但是一个想法是求局部最优解，从计算上讲似乎是可行的。深度学习的方法也是直接用全部SNP，并且计算复杂度也高于线性回归。但是深度学习的一个问题就是似乎很难做统计学检验？因为模型过于复杂，很难去检验每一个SNP效应值是否显著。**但是如果去检验偏微分呢？也就是输出对于每一个SNP的偏导数，去看它们是否显著**

和`--assoc`的结果是一样的


- **加上协方差矩阵**
  - PCA矩阵
  - [G矩阵](https://blog.sciencenet.cn/blog-2577109-1122903.html)
  - kinship，K矩阵
>更多关于G矩阵：https://www.cnblogs.com/liujiaxin2018/p/15504343.html

**有了多个变量之后就可以考虑变量之间的交互作用**，方法跟上面类似



#### G矩阵K矩阵以及PCA作为协变量

#### 混合线性模型