# 深度学习在调控基因组学中的应用
Ref:[Computational Systems Biology
Deep Learning in the Life Sciences](https://mit6874.github.io)第6，7课
[TOC]

## 调控基因组学

### DNApacking-染色体的结构
DNA序列在染色体上，是以核小体为最基本的单元。每一个核小体上覆盖的DNA序列大约200bp。而核小体与核小体之间的DNA序列，则处于开放状态；
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-065732.png)

在DNA序列上，存在的甲基化修饰等、转录因子的结合、是否是DNase的结合位点等的情况
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-065859.png)

因此可以采用免疫共沉淀之类的方法去抓取符合某些条件的DNA序列（比如：与某写转录因子结合的DNA序列；被DNaes结合的序列等）也就是各式各样的测序技术（Chip-seq，DNase-seq，ATAC-seq等）。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-070002.png)

此外还有捕获DNA序列之间的相互作用的Hi-C技术。

### 蛋白质与DNA的相互作用
转录因子都是蛋白质，作用于一些功能性DNA序列从而发挥各种各样的调控作用。TF和DNA的作用位点所对应的DNA序列虽然有所差异但是均具有比较保守的区域（可以通过local align 比对同一转录因子的结合序列找出共有的序列也就是**motif**）。这样的motif从相互作用上来讲可能是与对应的TF的某些氨基酸残基具有**高亲和性（affinity）**。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-070558.png)

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-070616.png)

### Technologies for probing gene regulation

#### chip-seq
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-070711.png)

#### DNase-seq
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071023.png)
DNase-seq与CHiP-seq的结果可以发现共同的信息：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071143.png)

#### Assay for Transposase-Accessible Chromatin (ATAC-seq)
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071052.png)

ATAC-seq的结果不一定会和DNase-seq的结果完全一致。

## Classical regulatory genomics
传统的发现motif的方法大多使用了PWM这样的矩阵进行各种诸如：odds-ratio等方法来判别

PWM：position weighted matrix 
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071858.png)

PSSM：相比于PWM，可以允许矩阵中存在负数，换言之负数代表了基因组背景的一个偏好性。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071914.png)

完整的一个表格，归纳了所有使用算法来预测motif和实验寻找motif。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071441.png)

## 深度学习在调控基因组学中的应用

最常用的是CNN的结构。
输入的数据通常是：一段序列（长度根据任务确定）;Chip-seq的结果
target的数据是：CHiP-seq的结果、ATAC-Seq的结果、Hi-C的结果。也可以是binary的
>binary 也就是一段序列是否是结合的或者非结合某个TF的。
### CNN for motif finding

#### DNA序列的编码方式
采用one-hot的编码方式对序列进行编码。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071637.png)

#### how CNN work for regulatory genomics

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-071720.png)

对于输入的序列，使用的1D卷积核会按照步长从左到右的滑过序列，并且进行卷积运算，并得到一个结果。这样的操作就是传统的motif finding的方法在做的事情。

卷积核其实就是一个PSSM矩阵（可以用softmax，换算成代表概率的结果），多个filter的卷积操作其实就等价于用多个PSSM矩阵在序列上进行扫描并得到一个**最大匹配结果分数**
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072148.png)。

结论：使用多个卷积核对序列进行扫描，实质上就是用多个PSSM矩阵对序列进行扫描。那么训练模型得到的filter也就对应了一个**motif**，这些motif可能是已经存在与数据库中的，也可能是未存在与数据库中的。

然后使用Max pooling对这样的最大匹配结果分数进行取最大的操作（或者平均），并使用ReLU来确保分数是大于0的（可能是为了保持和传统的motif finding的算法的思路一致。）

一段序列上，用多个filter进行扫描的生物学解释是：一段序列可以有多个motif区域
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072425.png)
#### CNN 在调控基因组学上的解释

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072548.png)

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072610.png)

**stride推荐设置为1！**


### 调控基因组学使用CNN网络的研究

#### DeepBind
整个流程图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072918.png)

最后解释第一层卷积的filter的结果：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-072950.png)


#### DeepSEA
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-073201.png)

#### Basset
**David R.Kelley 等人做的，这个组做这个方向做的挺好的。**
[scholar](https://scholar.google.com/citations?hl=en&user=NYzqnv0AAAAJ&view_op=list_works&sortby=pubdate)
github:https://github.com/orgs/kundajelab/repositories

basset的后续：https://github.com/calico/basenji

结构图：![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-073538.png)

这里预测的目标是164个cell type中的DNase sites（应该是(1,164)），输入的数据是对应的序列信息。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-073637.png)

#### chromputer
使用多个数据来预测输出。


![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-073821.png)

训练结果：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-09-073857.png)

#### DeepLift
