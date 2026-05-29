import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud
import re
import jieba.analyse as analyse

file = open("教育.txt", "r", encoding="utf-8")
text1 = file.readlines()
file.close()

st1 = re.sub('[，。、“”‘’！？]', '', str(text1))
keywords = analyse.extract_tags(st1, topK=20, withWeight=True)

print("TF-IDF算法提取的前20个关键词：")
print(keywords)

key_dict = {}

for item in keywords:
    key_dict[item[0]] = item[1]

mask_img = Image.open("bird.png")
mask_array = np.array(mask_img)
wc = WordCloud(
    font_path="simhei.ttf",
    max_words=100,
    mask=mask_array,
    width=800,
    height=600,
    background_color="white"
)

cloud = wc.generate_from_frequencies(key_dict)
cloud.to_file("TFIDF_WordCloud.png")

plt.imshow(cloud)
plt.axis("off")
plt.show()