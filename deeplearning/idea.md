# 深度学习在基因组学中的idea

## 使用BERT等pre-train idea实现DNA和氨基酸序列语法规则的学习

multi-language 的预训练方式在NLP中取得了一定的解释性进展

通过把不同语言的语料，利用Bert等模型训练，训练策略： bert传统的训练方式、完型填空等等得到预训练模型。
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-05-29--%E5%BC%BA%E6%8E%A8-%E6%9D%8E%E5%AE%8F%E6%AF%852021%E6%98%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20-%20055%20-%20-%E9%80%89%E4%BF%AE-To%20Learn%20More%20-%20BERT%20and%20its%20family%20-%20Introduction%20and%20Fine-tune-0001.png)

随后查看不同语言相近的词汇它们的embedding的相似性，可以发现很多会相近

**统计一个语言到另外一个语言中的 Mean Reciprocal Rank的大小 可以近似估量两个语言在模型中的语法规则的相似性**
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-05-29--%E5%BC%BA%E6%8E%A8-%E6%9D%8E%E5%AE%8F%E6%AF%852021%E6%98%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20-%20057%20-%20-%E9%80%89%E4%BF%AE-To%20Learn%20More%20-%20Multilingual%20BERT-0002.png)

可以绘制这样的图：
![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-05-29--%E5%BC%BA%E6%8E%A8-%E6%9D%8E%E5%AE%8F%E6%AF%852021%E6%98%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20-%20057%20-%20-%E9%80%89%E4%BF%AE-To%20Learn%20More%20-%20Multilingual%20BERT-0003.png)

### 基于3mer的DNA序列分词和蛋白质序列的bert模型来识别密码子和氨基酸之间的语法规则

生物学中密码子和氨基酸之间的转化关系是大家所熟知的。但是不同物种中密码子和氨基酸的对应关系略有不同，甚至偏好性也不同。

那么是否可以利用multi-language的idea去研究这个过程呢？

思路：以不同物种作为一个分界，用同一个物种中的基因组序列做3mer切分（**可以考虑3种不同的顺序作为对照**）和该物种编码的蛋白质序列作为语料
>也可以对照使用单独的编码基因作为语料。这样一个语句可以是一个基因
>也可以一个语句是随机切分出来的分词为3mer的DNA序列（倾向于这种）

有了语料库了，就可以使用bert做预训练，那么预训练的输出是什么呢？

策略：
1. 对输入的序列进行随机的mask，而输出是包含这些mask的正确序列，也即bert传统的策略
2. 采用\<cls\> 分词符，也即，在输入的序列开始加入cls分词符，希望输出的cls对应的是一个分类？也即bert 分类的训练策略![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2022-05-29--%E5%BC%BA%E6%8E%A8-%E6%9D%8E%E5%AE%8F%E6%AF%852021%E6%98%A5%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E8%AF%BE%E7%A8%8B%20-%20056%20-%20-%E9%80%89%E4%BF%AE-To%20Learn%20More%20-%20ELMo-%20BERT-%20GPT-%20XLNet-%20MASS-%20BART-%20UniLM-%20ELECTRA-%20others-0005.png)


预期结果：
 1. 模型可以很好完成预训练的任务
 2. 并且embedding中的确存在一些有趣的现象，
    1. 比如已经知道密码子-氨基酸的对它们的某种相似性的描述是很接近的；
    2. **根据一些密码子或者氨基酸找到与之相应的高相似性的另外一对，它们与现有的生物学观点相符或者相悖，能从该物种的特点中介绍**
 3. 可以用于其他任务中作为embedding的一层，并进行简单fine-tune后就可以很好的完成其他的基因组学相关的预测任务
 4. **对物种进行这样的训练进行对比实验看看结论的差异性**，对所有物种的合计进行语料库的训练（把不同物种的密码子和氨基酸作为同一种语言 或者分开处理 来对比）观察实验结果


## 基因表达预测上

### 模拟motif作用的层
对于一段启动子序列，可以将其编码成A为(seq_len, 4)的矩阵。  

假设有motif的矩阵V(motif_nums, seq_len, 4)，A与V 做点积，得到的就是该序列不同启动子的不同motif的结合概率的矩阵O（motif_nums, seq_len, 4），由于motif的长度未必是和seq_len等长的，所以我们可以在加上一个mask的W矩阵(motif_nums, seq_len ,4)，这个矩阵必须是介于0~1之间的，并且最好最好就只有0和1。W和O再做点积，得到真实的PSSM。输出需要用ReLU函数，去除为负的情况。（加不加b是个问题）
$$ReLU(A * V * sigmoid(W)) + b $$

option：最后得到的PSSM是(motif_nums, seq_len, 4)，可以考虑不同motif之间的attention。得到一个新的输出，第一个维度是motif_num，其中一个代表一个motif和其他motif之间的关系后得到的新的张量，可以近似理解为motif相互作用后的集合作为输出结果

option：motif的PSSM矩阵可以采用真实存在的矩阵作为替代。

### 基于motif的网络

第一层可以采用模拟motif的层

第二层采用？