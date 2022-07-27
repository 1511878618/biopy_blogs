
import matplotlib.pyplot as plt
import seaborn as sns

def vocalnoPlot(data:pd.DataFrame,
                x = 'log2FoldChange',
                y = 'pvalue',
                title = 'vocanlo',
                xlim = None,
                ylim = None,
                colors = None,
                **kwargs):
    # 先设置一下自己的颜色
    
    """
    example use: 
        vocalnoPlot(differentialGeneTable, x = 'fc', y = 'pval', xlim=[0, 4], title = "differential analysis vocanlo")
        plt.savefig("pic.png",dpi = 200)
    """
    if not colors:
        colors = ["#01c5c4","#ff414d", "#686d76"]
        
    sns.set_palette(sns.color_palette(colors))

    # 绘图
    ax=sns.scatterplot(x=x, y=y,data=data,
                    hue='type',#颜色映射
                    hue_order=["down", "up", "nosig"],
                    edgecolor = None,#点边界颜色
                    s=8,#点大小
                    )
    # 标签
    ax.set_title(title)
    ax.set_xlabel("log2FC")
    ax.set_ylabel("-log10(pvalue)")
    if isinstance(xlim, list):
        ax.set_xlim(xlim)
    if isinstance(xlim, list):
        ax.set_ylim(ylim)
    #移动图例位置
    ax.legend(loc='center right', bbox_to_anchor=(0.95,0.76), ncol=1)
    return ax 