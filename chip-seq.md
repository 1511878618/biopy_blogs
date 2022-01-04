#
要使用的是SRR3208779 和 SRR3208780两个数据采用的是双端测序，质控体系是33phred（查阅NCBI似乎不知道，不过是2000年的，应该是33）
原始数据是以及处理过了的raw数据，已经是fq格式，解压就好了

### 质控用fastqc进行
`fastqc _1.fa _2.fa -o f xxPATH -t 16`

查看质量结果

### 然后进行下一步bowtie2的比对

解压genome_index也就是bowtie2的索引文件
>这个东西其实可以通过全基因组序列进行生成，`bowtie2-build`就好

会生成一系列后缀名为.bt2的文件
然后输入
`bowtie2 -q -p 10 -x mm10_main/mm10_main -1 SRR3208780_1.fq -2 SRR3208780_2.fq -S SRR3208780.sam`其中mm10_main是存放idx的位置，而mm10_main则是生成的所有idx的名字
并把输出保存为sam格式
>bowtie2的使用参考：https://zhuanlan.zhihu.com/p/91317299
然后把输出转化成bam格式（也就是sam->二进制文件）
使用samtools，其中染色体的信息使用mm10_main.chrom.sizes
`samtools view -bt mm10_main/mm10_main.chrom.sizes SRR3208780.sam -o SRR3208780.bam`

>`bowtie2 -q -p 10 -x mm10_main/mm10_main -1 SRR3208780_1.fq -2 SRR3208780_2.fq | samtools view -bt mm10_main/mm10_main.chrom.sizes SRR3208780.sam -o SRR3208780.bam`


## 然后就是peak calling 
>https://www.jianshu.com/p/21e8c51fca23 参考这篇博文

其中寻找组蛋白修饰`macs2 callpeak -g hs -p 1e-5 --keep-dup 1 --nomodel --extsize 73 -t SRR3208779.bam -n SRR3208779.test.macs2`
>这里使用的是macs2 而不是很久以前的版本macs14，以前的--shiftsize 参数变成了--extsize 这个参数，并且这里没有使用对照组（control）。

寻找tf结合位点的`macs2 callpeak -g hs -p 1e-5 --keep-dup 1 -t SRR3208780.bam -n SRR3208780.TF.macs2`

>其中似乎80这个sample跟着tf结合位点发现的代码走提示没有匹配的peaks，报错如下：Too few paired peaks (0) so I can not build the model! Broader your MFOLD range parameter may erase this error. If it still can't build the model, we suggest to use --nomodel and --extsize 147 or other fixed number instead. 

#### 使用bed作为输入
师兄上传了bed文件，查阅到bed的确可以作为输入，并且这些bed似乎是由完整的sam文件生成的（不知道怎么生成的）。anyway，师兄说可以跑macs2，那就跑
代码如下：
寻找组蛋白修饰:
`macs2 callpeak -g mm -f BED -p 1e-5 --keep-dup 1 --nomodel --extsize 73 -t ICM_rep1.fragment.bed -n ICM_rep1.macs2 --outdir histoneModiftication/`
寻找tf结合位点:
`macs2 callpeak -g mm -f BED -p 1e-5 --keep-dup 1 -t ICM_rep1.fragment.bed  -n ICM_rep1.macs2 --outdir transcriptionFactor/`
但是似乎对于rep1和re2均会报错： Too few paired peaks (0) so I can not build the model! Broader your MFOLD range parameter may erase this error. If it still can't build the model, we suggest to use --nomodel and --extsize 147 or other fixed number instead. 
WARNING @ Fri, 13 Aug 2021 18:28:22: Process for pairing-model is terminated! 
很奇怪！。
不奇怪了！
这里做的事H3K4me3的数据，自然找不到tf结合位点类似的数据。

### 生成bigwig文件
` macs2 callpeak -g hs -B -q 0.05 --keep-dup 0.05 --keep-dup 1 --nomodel --extsize 147 -t SRR3208779.bam -n SRR3208779 --outdir SRR3208779`
然后需要使用`ucsc-bedclip`和`ucsc-bedgraphtobigwig`来处理
首先安装
`conda install -c bioconda -c conda-forge ucsc-bedclip `
`conda install -c bioconda -c conda-forge ucsc-bedgraphtobigwig `
然后运行代码如下：
`bedClip SRR3208779/SRR3208779_treat_pileup.bdg mm10_main/mm10_main.chrom.sizes SRR3208779/SRR3208779.tmp.bdg`
`grep -v _ SRR3208779/SRR3208779.tmp.bdg > SRR3208779/SRR3208779.bdg`


这里鉴于师兄考虑之前做mapping的时候如果把完整的数据给出来，可能电脑跑不动。于是只给了一部分，所以Peakcalling结果会比较少只有几十个。

而后续师兄给了Peakcalling后的bed文件。
>什么是bed文件呢？
>![](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-063222.jpg)
>这个就是一个简单的bed文件示例。每一行记录的是一个区域，对于peakcalling后的数据来说就是一个峰的区域，chr就是chrome的缩写。
>而bed文件还可以有许多格式，大多都是在增加每一个区域的一些信息，如：增加一些列来补充信息。
>**bed文件并不是chip-seq数据分析特有的**。更多关于bed的介绍可以看[这篇博文](https://blog.csdn.net/weixin_43569478/article/details/108079801)。以及[徐洲更](https://www.jianshu.com/p/a7b6ce208f98)
#### 尝试macs分析组蛋白修饰后IGV可视化
这里接着师兄给的bed文件做bigwig来使用IGV进行可视化，这里仍然是peakcalling

首先仍然是callpeak：
这里做的仍然是Peakcalling，这里做的事H3K4me3的数据，和之前组蛋白修饰那个代码的区别在于调节了窗口大小到147bp。

`macs2 callpeak -g mm -B -q 0.05 --keep-dup 1 --nomodel --extsize 147 -t ICM_rep2.fragment.bed -n ICM_rep2 --outdir ICM_rep2`
然后使用bedclip 生成bdg
`bedClip ICM_rep1/ICM_rep1_treat_pileup.bdg mm10_main/mm10_main.chrom.sizes ICM_rep1/ICM_rep1.tmp.bdg`

`grep -v _ ICM_rep1/ICM_rep1.tmp.bdg > ICM_rep1/ICM_rep1.bdg`

`bedGraphToBigWig ICM_rep2/ICM_rep2.bdg mm10_main/mm10_main.chrom.sizes ICM_rep2/ICM_rep2.bw`
然后可以使用IGV打开
结果如下图：



#### 用macs对数据标准化后IGV可视化
首先对数据进行normalize
`macs2 callpeak --SPMR -g mm -B -q 0.05 --keep-dup 1 --nomodel --extsize 147 -t ICM_rep2.fragment.bed -n ICM_rep2.normalise --outdir ICM_rep2/`

下面的操作和刚刚的操作是一样的，都是把pileup.bdg这个文件中换成bigwig的文件然后丢入IGV：

`bedClip ICM_rep1/ICM_rep1.normalise_treat_pileup.bdg mm10_main/mm10_main.chrom.sizes ICM_rep1/ICM_rep1.normalise.tmp.bdg`
`grep -v _ ICM_rep2/ICM_rep2.normalise.tmp.bdg > ICM_rep2/ICM_rep2.normalise.bdg`
`bedGraphToBigWig ICM_rep1/ICM_rep1.normalise.bdg mm10_main/mm10_main.chrom.sizes ICM_rep1/ICM_rep1.normalise.bw`

IGV的可视化就不在这里说了

### 顺式元件分析
这里要用的`ceasBW` ，网址见：https://bioconda.github.io/recipes/cistrome-ceas/README.html
虽然虽然，homepage和文档 都似乎挂掉了~，有点懵，但是似乎也是刘小乐开发的
安装：`conda install cistrome-ceas`


> 因为不知道chip region的bed文件是谁，用原始READS的bed去试试，报错 
> warnings.warn("ChIP bed file size may be too large to run CEAS with. Make sure it is a 'peak' file!")
> 表明应该输入的是callpeak后的bed。
但是narrowPeak含有太多其他信息，因此采用

`cat ICM_rep1/ICM_rep1.normalise_peaks.narrowPeak| cut -f 1-3 > ICM_rep1/ICM_rep1.normalise_peaks.narrowPeak.bed` 取出NarrowPeak的1-3列的数据并保存
下一步就是用ceasBW进行顺式作用元件的分析
师兄给的代码写出来时：
`ceasBW -w ICM_rep1/ICM_rep1.normalise.bw -b ICM_rep1/ICM_rep1.normalise_peaks.narrowPeak.bed -g mm10.refGene.main.sqlite3 -l mm10_main/mm10_main.chrom.sizes`
但是报错：
```
the pre-computed genome bg annotation is required for ChIP annotation. Use the gene annotation table files provided by CEAS or add a WIG file and set --bg.
```
查看`ceasBW -h`会发现：
```
  --bg                  Run genome BG annotation again. WARNING: This flag is
                        effective only if a WIG file is given through -w
```
和报错符合，并且因为使用了-w 所以要加上这个--bg的参数

加上后` ceasBW -w ICM_rep1/ICM_rep1.normalise.bw -b ICM_rep1/ICM_rep1.normalise_peaks.narrowPeak.bed -g mm10.refGene.main.sqlite3 -l mm10_main/mm10_main.chrom.sizes --bg`就可以运行拉

最后输出的结果会有两个文件,1个记录了所有结果的PDF和这些图的R源代码。
### motif finding

#### 使用MEME
安装meme
`conda install -c bioconda -c conda-forge meme`
然后首先需要使用bedtools中的fastaFromBed把bed转成fasta
但是！
`fasta-from-bed -fi mm10_main/mm10_main.fa -bed ICM_rep1/ICM_rep1_summits.bed -fo ICM_rep1_peaks.fa`
```
Usage: fasta_from_bed <BED file> <Genome filename> <index filename> <FASTA output filename>
```
报错，似乎还需要一个idx文件，但是师兄没有给，于是检索互联网发现：老版的bedtools使用起来和师兄的示例是一样的
于是乎，又重新
`conda create -n bedtools bedtools=2.16.2`
然后跟着师兄的跑
>比较好奇的是idx是什么，因为bed文件记录的是区间，那么只需要基因组的序列以及bed文件就应该可以还原了，仅仅进行一个序列上寻找相应位置的碱基就好，需要注意一个小问题就是：bed文件是数字表示开始和结束，但是对于xls来说基因组开头的第一个碱基的编号为1，而其他文件是0，这个似乎是为了方便用于不同的语言进行分析，narrowpeak是0开始，简单介绍：https://www.jianshu.com/p/f8dd323d3c2c。
以及GFF和Bed的区别：https://www.jianshu.com/p/9208c3b89e44

`fastaFromBed -fi ../mm10_main/mm10_main.fa -bed ICM_rep1_peaks.narrowPeak -fo ICM_rep1_peaks.narrowPeak.fa`
>这里不知道使用哪一个，另外两个跑出来似乎都有问题,然后我选择用narrowpeak ，虽然不是bed但是和bed也是很接近的格式仅仅多了一列，也是.bed文件。
>这里为什么不选用nummtis.bed文件，原因在于它仅仅保留了每个peak的最顶峰的值。用于motif的发现显然不能用这个。

anyway，继续下一步
使用meme进行分析

`meme ICM_rep1/ICM_rep1_peaks.narrowPeak.fa -dna -oc memeOutput/ICM_rep1 -nostatus -time 7200 -maxsize 100000000 -mod zoops -nmotifs 30 -minw 6 -maxw 50 -revcomp`

>**其中-maxsize 我认为应该是使用的数据集的最大大小？，不调大的话就跑不了会提示数据集太大，十分困惑**
具体见：https://www.jianshu.com/p/b1e0429e5897 关于参数的介绍 也可以`meme -h`

>加上`&`可以把命令挂在后头
>`meme ICM_rep2/ICM_rep2_peaks.narrowPeak.fa -dna -oc memeOutput/ICM_rep2/ -nostatus -time 7200 -maxsize 100000000 -mod zoops -nmotifs 30 -minw 6 -maxw 50 -revcomp &`