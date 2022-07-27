# samtools
- [samtools官方手册](http://www.htslib.org/doc/samtools.html)

**samtools**是用于处理`bam`和`sam`文件的工具。

## 常用命令

``` shell

samtools view -bS pair_end.sam| samtools sort -o pair_end.bam
samtools index pair_end.bam

# 查看flags

samtools view train_pair.bam | cut -f 2 | sort -S4G | uniq -c

##https://broadinstitute.github.io/picard/explain-flags.html 这个网站可以查看flags
#检查为某个flags（如：81）的reads

samtools view train_pair.bam | awk 'BEGIN{OFS="\t"}{if ($2=81) {print $0}}'|

```