import itertools
import pickle
from random import shuffle

import jieba
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


N = 100 #从语料中挑选N个文本量最丰富的词，特征维度，这个需要不断的测试，找出合适的维度

''' 使用：添加积极文本到'''

'''  提取特征方式  '''

# 将所有词作为特征
def bag_of_words(words):
    return dict([(word, True) for word in words])

# 将双词搭配作为特征
def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n) #使用了卡方统计的方法，选择排名前1000的双词
    return bag_of_words(bigrams)

# 所有词和（信息量大的）双词搭配一起作为特征
def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)

''' 提取特征进行分类学习 '''

# 计算posWords和negWords每个词的信息量
def create_word_scores(posWords,negWords):
    # posWords = ["好","棒呆了","很棒","cool","good","漂亮"]
    # negWords = ["差","差极了","很差","terrebiled","没眼看","滚粗"]

    posWords = list(itertools.chain(*posWords)) #把多维数组解链成一维数组
    negWords = list(itertools.chain(*negWords)) #同理

    word_fd = {}
    pos_word_fd = {}
    neg_word_fd = {}

    for word in posWords:
        word_fd.setdefault(word,0)
        word_fd[word]+=1
        pos_word_fd.setdefault(word,0)
        neg_word_fd.setdefault(word,0)
        pos_word_fd[word]+=1

    for word in negWords:
        word_fd.setdefault(word,0)
        word_fd[word]+=1
        neg_word_fd.setdefault(word,0)
        pos_word_fd.setdefault(word,0)
        neg_word_fd[word]+=1

    pos_word_count = len(pos_word_fd) #积极词的数量
    neg_word_count = len(neg_word_fd) #消极词的数量
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(pos_word_fd[word], (freq, pos_word_count), total_word_count) #计算积极词的卡方统计量，这里也可以计算互信息等其它统计量
        neg_score = BigramAssocMeasures.chi_sq(neg_word_fd[word], (freq, neg_word_count), total_word_count) #同理
        word_scores[word] = pos_score + neg_score #一个词的信息量等于积极卡方统计量加上消极卡方统计量
    return word_scores #包括了每个词和这个词的信息量

# 计算posWords和negWords双词搭配的信息量
def create_word_bigram_scores(posWords,negWords):
    # posdata = pickle.load(open('D:/code/sentiment_test/pos_review.pkl','r'))
    # negdata = pickle.load(open('D:/code/sentiment_test/neg_review.pkl','r'))

    posWords = list(itertools.chain(*posWords))
    negWords = list(itertools.chain(*negWords))

    bigram_finder = BigramCollocationFinder.from_words(negWords)
    posBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)
    negBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)

    pos = posWords + posBigrams #词和双词搭配
    neg = negWords + negBigrams

    word_fd = {}
    pos_word_fd = {}
    neg_word_fd = {}

    for word in pos:
        word_fd.setdefault(word,0)
        word_fd[word]+=1
        pos_word_fd.setdefault(word,0)
        neg_word_fd.setdefault(word,0)
        pos_word_fd[word]+=1

    for word in neg:
        word_fd.setdefault(word,0)
        word_fd[word]+=1
        neg_word_fd.setdefault(word,0)
        pos_word_fd.setdefault(word,0)
        neg_word_fd[word]+=1

    pos_word_count = len(pos_word_fd) #积极词的数量
    neg_word_count = len(neg_word_fd) #消极词的数量
    total_word_count = pos_word_count + neg_word_count

    word_scores = {}
    for word, freq in word_fd.items():
        pos_score = BigramAssocMeasures.chi_sq(pos_word_fd[word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(neg_word_fd[word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    return word_scores

# 根据信息量进行倒序排序，选择排名靠前的信息量的词
def find_best_words(word_scores, number):
    best_vals = sorted(word_scores.items(), key=lambda s:s[1], reverse=True)[:number]
    #把词按信息量倒序排序。number是特征的维度，是可以不断调整直至最优的
    best_words = set([w for w, s in best_vals])
    return best_words

# 选出的这些词作为特征，选择信息量丰富的特征
def best_word_features(words,best_words):
    return dict([(word, True) for word in words if word in best_words])

''' 情感分析：载入数据 '''

#停用词
stopWords = [word.strip() for word in open("stopword")]
#标点符号
punctuations = [word.strip("\n") for word in open("punctuation")]

# 载入数据
def load_data():
    pos_text = [line.strip() for line in open("../file/train/pos","r")]
    neg_text = [line.strip() for line in open("../file/train/neg","r")]
    pos = []
    neg = []

    for line in pos_text:
        word_list = delivery_word(line)
        pos.append(word_list)

    for line in neg_text:
        word_list = delivery_word(line)
        neg.append(word_list)

    shuffle(pos) #把积极文本的排列随机化
    shuffle(neg)
    return pos,neg

# 分词使用jieba
def delivery_word(comment):
    # 使用全模式
    seg_list = jieba.cut(comment,cut_all=False)
    word_list = []
    #去掉停用词，标点符号
    for word in seg_list:
       if word not in stopWords and word not in punctuations and word != '\n' and word!=' ' and not word.isdigit():
           word_list.append(word)
    return word_list

''' 情感分析：赋予类标签 '''

# 为积极文本赋予"pos" feature_extraction_method是将文本特征化的方法
def pos_features(pos_text,feature_extraction_method,best_words):
    posFeatures = []
    for i in pos_text:
        posWords = [feature_extraction_method(i,best_words),'pos'] #为积极文本赋予"pos"
        posFeatures.append(posWords)
    return posFeatures

#为消极文本赋予"neg"
def neg_features( neg_text,feature_extraction_method,best_words):
    negFeatures = []
    for j in neg_text:
        negWords = [feature_extraction_method(j,best_words),'neg'] #为消极文本赋予"neg"
        negFeatures.append(negWords)
    return negFeatures

''' 测试训练以及检验效果 '''

def score(classifier,train,testSet,tag_test):
    classifier = SklearnClassifier(classifier) #在nltk 中使用scikit-learn 的接口
    classifier.train(train) #训练分类器
    pred = classifier.classify_many(testSet)
    # classifier.prob_classify()
    # pred = classifier.batch_classify(testSet) #对开发测试集的数据进行分类，给出预测的标签
    return accuracy_score(tag_test, pred) #对比分类预测结果和人工标注的正确结果，给出分类器准确度


def test_and_store_model():
    #信息量丰富的词和双词搭配
    pos,neg = load_data()
    word_scores = create_word_bigram_scores(pos,neg)
    best_words = find_best_words(word_scores, N) #选择信息量最丰富的N个的特征
    posFeatures = pos_features(pos,best_word_features,best_words)
    negFeatures = neg_features(neg,best_word_features,best_words)

    train = posFeatures[15:]+negFeatures[15:] # 训练集合
    devtest = posFeatures[10:15]+negFeatures[10:15] #
    test = posFeatures[:10]+negFeatures[:10] #测试集

    test_list = []
    test_result_list = []

    for item in test:
        test_list.append(item[0])
        test_result_list.append(item[1])

    build_model(BernoulliNB(),train,best_words)
    #朴素贝叶斯
    print('BernoulliNB`s accuracy is %f' %score(BernoulliNB(),train,test_list,test_result_list))
    #分布数据的贝叶斯算法
    print('MultinomiaNB`s accuracy is %f' %score(MultinomialNB(),train,test_list,test_result_list))
    #逻辑回归算法
    print('LogisticRegression`s accuracy is %f' %score(LogisticRegression(),train,test_list,test_result_list))
    #svc算法
    print('SVC`s accuracy is %f' %score(SVC(),train,test_list,test_result_list))
    #线性svc
    print('LinearSVC`s accuracy is %f' %score(LinearSVC(),train,test_list,test_result_list))
    print('NuSVC`s accuracy is %f' %score(NuSVC(),train,test_list,test_result_list))


''' 训练模型以及存储 '''

def build_model(classifier,train,best_words):
    classifier = SklearnClassifier(classifier)
    classifier.train(train)
    pickle.dump(classifier, open('../file/train/classifier.pkl','wb'))
    pickle.dump(best_words, open('../file/train/best_words.pkl','wb'))

def load_model():
    classifier = pickle.load(open('../file/train/classifier.pkl','rb'))
    best_words = pickle.load(open('../file/train/best_words.pkl','rb'))
    return classifier,best_words

def predict(clf,comment,best_words):
    # feat = []
    comment_words = delivery_word(comment)
    pred = clf.prob_classify(best_word_features(comment_words,best_words))
    return pred

def test_result():
    model,best_words = load_model()
    comment = "很不错的软件，旧手机都没问题"
    pred = predict(model,comment,best_words)
    print("积极："+str(pred.prob('pos')) + "  消极：" + str(pred.prob('neg')) + '\n')