from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#生成词云
def generateTagClound(filename,taglist):
    # text = "google linux tencent ali baidu wangyi didi zhihu jingdong "
    # wordcloud = WordCloud().fit_words(text)
    d = path.dirname(__file__)
    # text = ' '.join(taglist)
    # wordcloud = WordCloud().generate(text)
    # alice_coloring = plt.imread(path.join(d, "alice_color.png"))
    wordcloud = WordCloud(font_path="微软雅黑.ttf",background_color="gray", margin=5, width=1500, height=1000,ranks_only=True)\
        .generate_from_frequencies(taglist)

    # plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    print(d+"/file/figures/"+filename)
    wordcloud.to_file("../file/figures/"+filename+".jpg")