from pylab import *

myfont = matplotlib.font_manager.FontProperties(fname='微软雅黑.ttf')
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

class Line(object):
    def __init__(self,label,capacity):
        self.label = label
        self.capacity = capacity
        self.x_list = []
        self.y_list = []
        self.sort()

    def sort(self):
        d = self.capacity
        self.x_list = sorted(d.keys())
        for x in self.x_list:
            self.y_list.append(d[x])

class BrokenLineChart(object):
    def __init__(self,x_label="x",y_label="y",title=""):
        self.lines = []
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

    def addLine(self,line):
        self.lines.append(line)

    def removeLine(self,line):
        self.lines.remove(line)

    def showLines(self,is_save=False,img="figure"):
        if len(self.lines) == 0:
            return

        plt.figure()
        # count = self.lines.count()
        for line in self.lines:
            plt.plot(line.x_list,line.y_list,label='$'+line.label+'$')
        plt.legend()
        plt.xlabel(self.x_label,fontproperties=myfont)
        plt.ylabel(self.y_label,fontproperties=myfont)
        plt.title(self.title,fontproperties=myfont)
        plt.show()
        if is_save == True:
            plt.savefig(img)
