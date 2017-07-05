from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

text = open('../wikiTitles.txt').read()
wordcloud = WordCloud().generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

plt.show()
