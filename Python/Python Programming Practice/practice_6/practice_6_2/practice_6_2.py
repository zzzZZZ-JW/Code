import numpy as np
from PIL import Image
from wordcloud import WordCloud
file = open("Mocking Bird.txt", "r", encoding="utf-8")
text = file.read()
mask_img = Image.open("heart.png")
mask_array = np.array(mask_img)
wc = WordCloud(background_color="white",
               width=800,
               height=400,
               max_words=100,
               mask=mask_array)
wc.generate(text)
wc.to_file("English_WordCloud.png")