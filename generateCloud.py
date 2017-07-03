from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generateCloud(filer):
    text = open(filer).read()
    wordcloud = WordCloud().generate(text)
    return wordcloud


if __name__ == '__main__':
    generateWordCloud('const.txt')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

