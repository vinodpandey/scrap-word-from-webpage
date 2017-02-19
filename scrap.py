from lxml import etree
import urllib2
from io import StringIO
import sys
from bs4 import BeautifulSoup
import string

# To fix: UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys)
sys.setdefaultencoding("utf8")

print 'loading words to set'
# load words file to a set
word_set = set()
with open("words.txt", "r+") as f:
    for line in f:
        word_set.add(line.replace("\n", "").lower())


print 'getting content from remote URL'
# get words from remote URL
response = urllib2.urlopen('http://www.pbs.org/parents/education/math/math-tips-for-parents/glossary-math-terms/')
html_content = unicode(response.read())

print 'processing content'
parser = etree.HTMLParser()
tree = etree.parse(StringIO(html_content), parser)

data = etree.tostring(tree.xpath('//*[@id="post-5595"]')[0], method="html")

# removing html tags and special characters
soup = BeautifulSoup(data, "lxml")
text = soup.get_text().replace('\n', ' ')
text = ''.join([x for x in text if x in string.ascii_letters + '\'- ' ])

words_list = text.split(' ')

print 'adding new words to set'
for words in words_list:
    word_set.add(words.lower())

print 'saving new words to file'
with open("new-words.txt", "a") as f:
    for word in word_set:
        f.write(word.lower() + "\n")
