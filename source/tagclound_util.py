from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#生成词云
def generateTagClound(filename,taglist):
    # text = "google linux tencent ali baidu wangyi didi zhihu jingdong "
    # wordcloud = WordCloud().fit_words(text)
    d = path.dirname(__file__)
    text = ' '.join(taglist)
    wordcloud = WordCloud(background_color="black", margin=5, width=1800, height=800).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file(d,filename)
