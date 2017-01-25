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

class LineChart(object):
    def __init__(self,x_label="x",y_label="y",title=""):
        self.lines = []
        self.x_label = x_label
        self.y_label = y_label
        self.title = title

    def addLine(self,line):
        self.lines.append(line)

    def removeLine(self,line):
        self.lines.remove(line)

    def showLines(self,show_broken = True, show_bar = False,show_value = False, values=None, is_save=False,is_datetime = False,img="figure"):
        if len(self.lines) == 0:
            return

        plt.figure(1)
        for i in range(0,len(self.lines)):
            line = self.lines[i]
            if show_broken:
                # plt.plot(line.x_list,line.y_list)
                if is_datetime:
                    ax = plt.gca()
                    ax.plot_date(line.x_list,line.y_list, 'o-',label='$'+line.label+'$')
                    ax.xaxis.set_major_formatter( DateFormatter('%Y-%m-%d') )
                    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
                else:
                    plt.plot(line.x_list,line.y_list, 'o-',label='$'+line.label+'$')
            if show_bar:
                plt.bar(line.x_list, line.y_list, alpha = .5)
            if show_value:
                value = values[i]
                for j in range(0,len(line.x_list)):
                    x = line.x_list[j]
                    y = line.y_list[j]
                    # plt.text(x*93/100, y*101/100, values[j])
                    if is_datetime == False:
                        plt.annotate(value[j],xy=(x*94/100, y*101/100))
                    else:
                        plt.annotate(value[j],xy=(x,y))

        plt.legend(loc='upper center', bbox_to_anchor=(0.8,0.8),fancybox=True)
        plt.xlabel(self.x_label,fontproperties=myfont)
        plt.ylabel(self.y_label,fontproperties=myfont)
        plt.title(self.title,fontproperties=myfont)

        plt.show()
        if is_save == True:
            plt.savefig(img)