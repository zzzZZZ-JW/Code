import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jieba
from wordcloud import WordCloud
import re

file = open("教育.txt", "r", encoding="utf-8")
text1 = file.readlines()
file.close()
text1 = str(text1)
st1 = re.sub('[，。、“”‘’！？]', '', str(text1))
cut_words = jieba.lcut(st1)
words = " ".join(cut_words)
mask_img = Image.open("bird.png")
mask_array = np.array(mask_img)
out_file = "Chinese_WordCloud.png"
excludeWords = ['我','了','在','的','我们','是','和','一个','这','那么']
wc = WordCloud(font_path="simhei.ttf",
               max_words=100,
               mask=mask_array,
               width=800,
               height=600,
               stopwords=set(excludeWords),
               background_color="white")
cloud = wc.generate(words)
cloud.to_file("Chinese_WordCloud.png")
plt.imshow(cloud)
plt.axis("off")
plt.show()