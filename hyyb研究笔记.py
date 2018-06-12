
""" 关于 特殊字符的处理 """

""" 1. & """
根据对交通运输行业报告的观察，标题中含有 http://www.htmlhelp.com/reference/html40/entities/special.html 包含的字符，然而正文中没有。
正文中出现过 S&P500,   其他的 '&' 均表示为 '和' 的意思


""" view the hyyb """
def view_reports(dir_name):
    g = iter_files(dir_name)
    for f in g:
        t = json.load(open(f,'r'))
        print (t['hyyb_url'])
        print (t['title'])
        print (t['newsContent_text'])
        yield

g = view_reports(dir_name)
next(g)


""" 正则表达式之匹配中文 """
https://www.w3cschool.cn/regexp/nck51pqj.html
# \w匹配的仅仅是中文，数字，字母，对于国人来讲，仅匹配中文时常会用到，见下
# 匹配中文字符的正则表达式： [\u4e00-\u9fa5]

# 或许你也需要匹配双字节字符，中文也是双字节的字符
# 匹配双字节字符(包括汉字在内)：[^\x00-\xff]


""" 几个想法 关于NLP数据处理"""
1. 感觉一段一段的分析会比较好
2. 每个 paragraph 一般会有一个 开头， 开头可以认为是标注。 但是标注都不一样，或许可以使用 LDA的方法 对 段落进行 clustering。
然后自定义几个标注
3. 更细一点可以分析每一个 sentence, 每个 sentence 都会描述一些内容，内容可以是 客观市场数据描述， 投资组合推荐，  风险提示， 市场分析
4. 对每个行业要做出个别分析，感觉行业之间的混合会加大难度
5. 对数据要做出充分的处理，尤其是 公司 指数 和 数字的挖掘， 数字包括  年月日，  百分比  ， 文件 《。。。》

6. 对每个行业，可以更细分，比如周报，月报， 半年报， 年报， 深度报告等，每一种写法都不一样
7. 感觉DL的做法主要是用来快速找出相同的entity， 及info extraction。并不是主要用来写文章。或许可以用来训练模板


""" 做法 """
1. 第一步可以对报告作出细分， 比如周报，月报， 半年报， 年报， 深度报告等  （或许某些报告可以使用模板， 省去DL）
2. 第一步还可以考虑 机构 的情况， 不同机构写作风格不同， 可以训练出多种写作风格 （甚至across industries）
3. 报告总体可以分为  个股，新股， 行业， 策略， 宏观， 盈利预测， 券商晨会 （来自东方财富网）
4. 报告中不同章节写法相同还是不同？？DNN 直接生产报告还是生产模板？？
5. 如何对章节分类， 如何对句子分类 （有些句子比如，  投资组合：a,b,c   本周组合：d,e,f ）
