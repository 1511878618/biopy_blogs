# LDSC

- **The genomic inflation factor** was defined as the median of the observed chi-squared test statistics divided by the expected median of the corresponding chi-squared distribution and was computed for each chromosome separately and for the whole genome for the different densities.

- polygentic因素会与LD共同发挥作用进而影响GWAS的结果？

## 为什么要做LD？

- 个体之间的潜在关系是指：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-13-090147.png)

- A **meta-analysis** is a
statistical analysis
that combines **the
results** of multiple
scientific studies on
the same question.
>While no-one has access to all original genotype-phenotype
data, everyone can access the meta-analyzed GWAS results
as they are (often) publicly available.

## LD, linkage disequilibrium

- 连锁平衡 就是**独立不相关**，也就是单倍型中的几个基因是随机分配的
- 连锁不平衡，就是**独立相关**，也就是单倍型中的几个基因不是**随机分配的**

>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-12-061729.png)

上面这张图说的是：我们假定基因组上有两个位点：*1位点中的一个等位基因A*，*2位点中的一个等位基因B*

对应的频率为：$P_A和P_B$

同一个单倍型中出现AB的情况：$P_{AB}$
>[单倍型](https://zh.wikipedia.org/wiki/单倍群)讲的是，同一条染色体上，不同位点之中不同等位基因的一个组合。比如：我们有1,2,3三个基因座，对应的各存在三组等位基因情况，分别是$A_1,A_2,B_1,B_2,C_1,C_2$。理论上就有$2^3$个组合的情况，其中一个组合：$A_1,B_1,C_1$就叫做一个单倍型。

假定$D_{AB} = P_{AB} - P_AP_B$，如果**连锁平衡**就意味着$D_{AB}$几乎为0；**连锁不平衡**就意味着$D_{AB}$不等于0，也就是说A和B不**相关**

这样我们就可以去寻找基因组中的LD区域。**目前关于LD最常用的一个定义是利用皮尔森相关系数$r^2$，公式如下。**

$r^2 = \frac{D_{AB}^2}{p_A(1-P_A)p_B(1-p_B)}$

>$P_A$可以是样本中的频率作为总体频率的估计
>**是否也可以用bootstrap之类的抽样方式来获取对应的A基因的频率的估计？**

简单介绍可以参考[GWASLab](https://zhuanlan.zhihu.com/p/362250519)。

计算LD的时候也需要注意：
1. **样本中的来自不同群体的样本会影响我们研究LD**，其他小群体中的等位基因的频率可能会与另外一个小群体的该等位基因的频率有差异，而如果混合在一起，我们计算出来的$r^2$或者$D_{AB}$就会趋近于两个小群体的加权平均。
2. 此外**群体的大小也会影响我们计算的结果，因为$P_A$会受到抽样的影响，样本越大越接近期望概率**。是否**可以用bootstrap等抽样的方式来近似总体的该基因型的频率？**

### GWAS中为什么需要考虑LD的因素

LD区域往往会在亲缘关系较近的人群中是相似的，而association分析的结果往往会出现如下图所示的 **peak**![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-12-065229.png)

这些peak可能是因为这些位点是高度连锁的，因此出现的分布是相似的。

那么如果我们的样本来自同一个近源群体中，**这样的peak就可能是该群体中常见的LD，并且与目标性状高度关联**

**但是如果我们的样本来自多样化的群体，比如亚欧非人群的混合样本呢**？LD的存在就可能会影响关联分析的显著性。

>另外一个观点：**In a GWAS, test statistic distribution can be inflated by both
polygenicity - meaning that many small genetic effects together affect the phenotype -
and confounding bias such as cryptic relatedness and population stratification.**

>Both polygenicity (many small genetic effects) and confounding biases, such as cryptic relatedness and population stratification, can yield an inflated distribution of test statistics in genome-wide association studies (GWAS).

**因此我们做GWAS的时候往往需要考虑群体分层的情况**




### 遗传力

遗传力是想要描述在给定的样本中，与**遗传相关的方差占表型的总方差的百分比。**
>这里的遗传因素包括SNP但不仅局限于此。

- 广义遗传力：$H^2 = \frac{\sigma_G^2}{\sigma_P^2}$，其中$\sigma_G$是遗传因素的方差，而$\sigma_P$是表型的方差。其中，认为：$\sigma_P^2 = \sigma_G^2 + \sigma_E^2 + \sigma_{E\times G}^2$是成立的，也就是**表型的方差由遗传因素贡献的方差和环境贡献的方差以及遗传因素和环境因素的方差组成**。而这里的$\sigma_G^2 = \sigma_A^2 + \sigma_D^2 + \sigma_I^2$，A是加性模型的情况下的方差，D是dominant或者passsive模型下的方差，而I这是**上位基因**？的方差。也就是把遗传效应的方差分解成多个部分产生

>其假设模型可以想象成$P = \bold{W}*G + \bold{\beta}E + \bold{W_1}*E*G$的模型，这样$var(P)$就可以分解成上述三部分

- 狭义遗传力：$h^2_{SNP} = \frac{\sigma_{SNP \in S}^2}{\sigma_P^2}$，也就是$y = xw+b + \epsilon$的一元回归模型中$var(y)$和$var(w)$之间的百分比。表型的变异中可以被回归模型解释的部分变异的占比。$var(y) = var(xw+b) + var(\epsilon)$。这里的$S$表示全部SNP的集合。

这样的狭义遗传力也被叫做这样一个芯片上的SNP。由于这样的遗传力只包括SNP的，以及样本数量会影响该值的大小，因此这个值会小于广义遗传力。**因此之前的许多研究就发现这样做出来的遗传力远小于以前通过双胞胎等实验方式算出来的遗传力**。造成了一段时间的困惑，😂。

LDscore regression，可以帮助计算出比较准确的芯片集上的遗传力。


### LDscore regression

- LD score 是用来描述在所有的SNP与某一个特定的$SNP_i$之间的$r^2$的和，也就是皮尔森相关系数。即：$l_{i,:} = \sum_{k=1}^Mr_{i,k}^2$。其中$:$表示所有的SNP，$r^2_{i,k}$表示第i个SNP（也就是当前计算的这个SNP）与另外一个$SNP_k$的$r^2$值

>这里是否需要考虑这个SNP与自己的$r^2$？似乎没提及，我个人认为是不需要考虑的，应为恒定为1。

- category specific LD Score。 在LD score的基础上，我们需要考虑的这些其他SNP，不再是所有的SNP了。而是**属于特定的某一类别C的SNP**。这样公式可以改写为$l_{i,\bold{C}} = \sum_{k\in\bold{C}}r_{i,k}^2$

因为LDscore取决于$r_{i,k}^2$，因此需要估计$r_{i,k}^2$。我们直接计算得到的是样本中的$\hat{r}_{i,k}^2$。

但是**这个估计不是无偏的**，所以[Bulik-Sullivan et al., 2015][1]提出了一个矫正过的$r_{adj}^2 = \hat{r}^2 - \frac{1-\hat{r}^2}{N-2}$作为近似的无偏估计
>更多详细的推到与论证见这篇论文嗷

**有了这个就可以计算近似的LDscore**。

$OR = \frac{odds1}{odds2}$


### jackknife的方法

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-04-13-030956.png)





<!-- 引用 -->

[1]: https://www.nature.com/articles/ng.3211