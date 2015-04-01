#-*- coding: utf-8 -*-
import urllib2
import json
from bs4 import BeautifulSoup

class iclba_parse(object):
    """
    A web crawler gets data from iciba.com
    """

    def __init__(self, url):
        """
        the property needed in the special html
        self.word_pos = "word_name_h1"
        self.soundmark_pos = "prons"
        self.soundmark_pos_child = "fl"
        """

        self.set_url(url)
        return

    def set_url(self, url):
        """
        set the url which wants to parse words
        """
        self.url = url
        self.page = urllib2.urlopen(url).read()
        self.soup = BeautifulSoup(self.page)
        return

    def get_word(self):
        """
        get the word from html
        """
        word = self.soup.find(id="word_name_h1").string
        return json.dumps({'word': word})

    def get_meaning(self):
        """
        get the meaning of the word
        """
        r = []
        meaning_div = self.soup.find("div", {"class": "group_pos"} )
        for item in meaning_div.find_all('p'):
            category = item.find("strong").string
            chinese = []
            for label in item.find("span"):
                chinese.append(label.string)
            r.append({category: chinese})
        return json.dumps(r)

    def get_soundmark(self):
        """
        get the soundmark from html
        Return: ["XXX", "XXX"]
        """
        soundmark = self.soup.select(".prons > .eg > .fl > strong")
        r = []
        for item in soundmark:
            item_str = item.string
            if item_str != "[" and item_str != "]":
                r.append(item_str)
        return json.dumps(r)

    def get_sentences(self):
        """
        get all exaple sentences fo the word
        Return: [{sen_key: sen_value}, {...}]
        """
        sentences = self.soup.find_all("dl", {"class": "vDef_list"})
        r = []
        for sentence in sentences:
            eng = sentence.find("dt")
            # use this trick to find the hold sentence
            # delete the uncorrected element
            eng_a = eng.find("a")
            eng_a.extract()
            # replace the span node to the origin word
            keyword = eng.find("span").find("b").string
            eng.find("span").replace_with(keyword)
            # put all the sections together
            eng_str = ""
            for item in eng:
                eng_str += item.string
            chinese = sentence.find("dd").string
            r.append({eng_str.strip(): chinese})
        return json.dumps(r)

def main():
    word_spider = iclba_parse("http://www.iciba.com/support")
    word_json = word_spider.get_word()
    print "word: ", word_json
    meaning_json = json.loads(word_spider.get_meaning())
    for mean in meaning_json:
        for key, value in mean.items():
            value = map(lambda x: unicode(x), value)
            print key, ''.join(value)
    sd_json = json.loads(word_spider.get_soundmark())
    print "soundmark: ", sd_json[0], sd_json[1]
    sen_json = json.loads(word_spider.get_sentences())
    for sen in sen_json:
        for key, value in sen.items():
            value = map(lambda x: unicode(x), value)
            print key, ''.join(value)
    return

if __name__ == "__main__":
    main()

