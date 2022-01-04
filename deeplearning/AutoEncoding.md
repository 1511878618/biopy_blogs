
# 自编码器
[TOC]
自编码器的输入和输出均是自己，也就是 输入：是一张图片；输出也是这张图片。

自编码器也可以说是self-supervise 的一种方式
也就是这样的一个图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-060637.png)

而我们期望的效果就是这样的一个vector能够包含左边输入的图片中的某些讯息。这些讯息通过Encoder提取出来，并且可以通过Decoder给还原回去。就好像是一种**降维操作（dimension reduction）**。

>更多关于降维的操作；PCA 和t-sne 是传统的机器学习方法来进行降维
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08--%E5%BC%BA%E6%8E%A8-%E6%9D%8E%E5%AE%8F%E6%AF%852021%E6%98%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20-%20053%20-%20%E8%87%AA%E7%BC%96%E7%A0%81%E5%99%A8%20-Auto-encoder-%20-%E4%B8%8A-%20%E2%80%93%20%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5-0001.png)

因此这样的自编码器训练得到的**vector**就可以用来下游的分析。比方说用于另外的模型输入，因为我们已经把一个很大很大的图片，给降维到一个**vector**，几百或者几千的大小。
## Feature Disentangle
Feature disentangle做的事情呢其实就是去解释，这样的Vector的功能。
比方说我们train了这样一个自编码器：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-061239.png)
输入是一段语言，输出也是这段语音。那么这个vector我们就可以认为它蕴含了原语音中的某些信息：内容、说话人之类的。那么如果可以解释这样的vector的话，就可以更好的利用它。
图片中的三篇文章介绍了怎么去做这样的事情

>更多关于vector可能包含的内容的一些猜想或者想法
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-061529.png)

在生物学中，也会有比较好的用处。

### 应用
可以实现的一个应用：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-061927.png)

vector可以分为：1）：文字内容；2）：说话人的声音
这样如果交换两个不同人说的话对应的vec，就可以实现A的内容用B的声音说出来。也就是柯南的变声器的功效啦

#### 生物学中可能的用处
1. 通过这样的Auto-encoder 去学习序列数据与一些调控信息；比方说：输入某个1000bp序列对应的TF结合的peak数据，输出也是这个。那么中间的vec可以试图让它是代表了：1）物种或者序列位于那一条染色体的信息；2）：代表了这个序列位于的基因的信息等。

## Discrete Representation
可以让vector变得特殊一些：比方说 是二进制的；比方说是one-hot的；比方说可以是(20,10)
的一个时间序列
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-062639.png)


一个比较有趣的想法（VQVAE做的事情）是：如果我把encoder得到的vector和一个包含了许多vector的字典（这个vector 字典里面的东西都是有意义，可以解释的东西），然后计算这个vector和字典中每一个vector之间的相似性（可以用类似self-attention的机制去做）。拿相似性最高的$vector_N$ 在丢到decoder中去。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-063129.png)
>那么反向梯度传播的过程该怎么去实现呢？

另外一个有趣的想法是用来做摘要（summary）。输入一个文章，输出也是这个文章，我们希望这个**vector**是一个特殊的矩阵，这个矩阵呢就是编码后的一段句子，也就是摘要。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-063654.png)

但是正常情况下这样训练出来的word sequence，很大概率是我们看不懂的东西（即使我们有一个embedding词典，这里面的向量也往往找不到词典中对应的解释）那么怎么做呢？
添加一个Discriminator，去判别产生的sequence是不是人写的。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-064033.png)
这样其实就成了一个cycle GAN网络了。
>关于更多GAN的东西。

更有趣的：拿tree 作为**vector**
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-064342.png)
>**那可以用基因的同源序列作为输入和输出；中间的vector是一个树；再接上一个判别器（用真实的树的训练出来的可以判别是不是树的一个模型）来做一个cycle gan的工作呢？**


## decoder =? generator

![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-064720.png)

## 1 class模型？

有的时候我们想做二分类问题，但是实际上我们很容易收集到的数据均是分类某一类的，而另外一类的数据可能会很少。
这样一个例子：你有一堆你老婆的照片？？（lol），你可以train这样一个Auto-encoder模型
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-065526.png)
训练集中全是你老婆的照片，还原的也是你老婆的照片。这个时候我们就可以别管vector的信息了~。

那么下一次给你一张新的照片，如果仍然是你老婆的照片，那么还原出来的结果应该说和输入的照片的**差异会比较小**；而如果不是你老婆的照片，差异可能会很大。这样就可以实现一个判别器了~。可能结果就会像这样：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-065939.png)


## 训练自编码器的一些小技巧？
1. 输入的数据可以进行一些处理，比方说：在**输入的图片中加上一些随机的噪声**，而输出采用并没有加上噪声的原图片。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-12-08-061017.png)

