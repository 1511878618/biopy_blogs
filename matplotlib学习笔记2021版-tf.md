#

`Fig,ax =  plt.subplots()`创建了一个fig和相应的ax



# Figure

![../../_images/anatomy.png](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-063223.jpg)

## Axes

ax对象的[相关函数见此处](https://matplotlib.org/stable/api/axes_api.html?highlight=axes#module-matplotlib.axes)

ax也就是axes

对于axes 

首先可以进行的就是

`ax.plot()`绘制一个图形

> 使用`twin1 = ax.twinx()`可以创建一个新的y轴在该axes，实现绘制多个y轴的效果，要绘制相应的曲线则需要对twin1进行操作，twin1和ax是相似的用法。



### Spine

一个axes四周的四条线叫做spine

`ax.spines[['top'],['right']]`可以获得相应的spine

或者也可以`ax.spines.top`获取

常用的调整：

```python
ax.spines.bottom.set_position(('axes',0.1)) #移动spines的位置
## 修改spines的大小与风格
ax.spines.bottom.set_ls('--')
ax.spines.bottom.set_linewidth(5)
ax.spines.bottom.set_color('#a61b29')
## 设置是否显示spines
ax.spines.bottom.set_visible(False)

```



### Axis

### ![截屏2021-07-09 下午5.11.48](https://tf-picture-bed-1259792641.cos.ap-beijing.myqcloud.com/blog/2021-08-18-063224.jpg)

### tick

tick是指坐标轴上的刻度，分为两类

- major_ticks即大一点的刻度
- minor_ticks即小一点的刻度

要获取相应的ticks采用以下代码即可：

```python
# 获取x轴的major_ticks
ax.xaxis.get_major_ticks() #返回一个包含matplotlib.axis.XTick object的列表，可以通过索引进行单个ticks的修改，如：是否显示某个ticks(.set_visible())


# 显示ticks
ax.yaxis.set_ticks_position('right') #y轴对应的两边ticks，显示右边的，而不显示左边的。


```

 

 tick的修改可以采用两种方式进行：

1. 使用locator和formatter进行。前者负责刻度的位置，后者则是负责刻度上的label
2. 使用一组list作为坐标进行ticks的设置，随后对tickslabel进行修改
3. 使用locator去定位，直接修改ticks label（结合前两种）。

#### locator和formatter的方式

[locator](https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.Formatter)和Formatter是配置tick的位置和内容的东西。

Locator是`matplotlib.ticker`中的一系列locator

Formattor是`matplotlib.ticker`中的一系列formatter

```python
import matplotlib

#对x轴的major_ticks进行修改
##设置locator
ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2))#MultipleLocator 会在x轴上按每2个长度进行设置ticks
ax.axis.set_major_locator(matplotlib.ticker.LinearLocator(3))#会在x轴的范围内生成3个分布均匀的ticks
# 类似于LinearLocator
ax.locator_params(axis='x',nbins=5) #可以直接设置x轴只有5个

##设置formatter
ax.xaxis.set_major_formatter('{x:.0f}度')#采用默认的formatter，其中{x:.0f} 的:.0f 是str formatter的方式进行，{}外则是需要添加的文字，x是ticks所位于的坐标。
# 此外还有其他的Formatter，但是使用自己给的str进行显示会比较方便的

#使用ticm_params设置总体的一些参数
ax.tick_params(axis='x',which='major',
               length=5,width=2,color='r',# length 是tick的线的长度，width 是tick的宽度， color 是tick的颜色
               labelsize=20,labelcolor='b')#labelsize 是tickslabel的字体大小，labelcolor是字体的颜色



```

####  直接设置ticks和labels

```python

ax.set_xticks(np.linspace(0,100,12)) #生成一个list作为xticks
#随后设置相应的xticks，使用fontproperties进行字体的设置。
ax.set_xticklabels(['{}月'.format(i) for i in range(1,13)],c='#432101',rotation=30,
                   fontproperties=matplotlib.font_manager.FontProperties('Songti SC',size=20))
#设置yticks
ax.set_yticks([i for i in ax.get_yticks() if i >0]) ##返回的是包含Tick类的list，可以对其中单个tick进行设置
#设置ytickslabels
ax.set_yticklabels(['Level {}'.format(i) for i in ax.get_yticks()],c='#432111',rotation=-30,
                  fontproperties=matplotlib.font_manager.FontProperties('Times New Roman',size=20)) #返回的是包含matplotlib.text.Text类的list，可以对其中的单个ticklabel进行更改
```

