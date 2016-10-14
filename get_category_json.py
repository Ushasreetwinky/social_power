"""TO get category of each tweet."""
import pickle
import json
import sys
from datetime import datetime
from pytagcloud.lang.counter import get_tag_counts
from collections import OrderedDict
handle = sys.argv[1]
date = datetime.today().strftime('%d_%m_%Y').replace(" ", "_")


class DefaultListOrderedDict(OrderedDict):
    """creating ordered dict."""

    def __missing__(self, k):
        """Creating key if missing."""
        self[k] = []
        return self[k]


def read_file():
    """Function to read 1000 tweet file."""
    with open(handle + '_' + date + '.json') as json_data:
        d = json.load(json_data)
        minister_thousand = d[0:1000]
    get_category(minister_thousand)


def word_cloud(text):
    """Function to get word cloud data."""
    counts = get_tag_counts(text)
    text_data = []
    stop_words = ['rt', 'ji', 'wish', 'wishes', 'wished', 'shri', 'pm', 'gv',
                  'duttyogi', 'srikidambi', 'tomar', 'amp']
    i = 0
    print len(counts)
    while len(text_data) < 100:
        dic = {}
        if(counts[i][0] not in stop_words):
            dic[counts[i][0]] = counts[i][1]
            text_data.append(dic)
        i += 1
    print text_data
    with open(handle + '_' + date + '_word_cloud.json', 'w') as f:
        json.dump(text_data, f, indent=1)
        f.close()


def get_category(minister_thousand):
    """Function to get category of tweets."""
    cl = pickle.load(open("pmo-category-engine.p", "U"))
    category = []
    tweet_text = ""
    print len(minister_thousand)
    for tweet in minister_thousand:
        text_data = tweet['text'].encode('ascii', 'ignore')
        if "https" not in text_data:
            tweet_text += text_data
        else:
            tweet_text += text_data[:text_data.index("https")]
        text = tweet['text'].lower()
        prob_dist = cl.prob_classify(text)
        tweet['category'] = prob_dist.max()
        category.append(tweet)
    print tweet_text
    word_cloud(tweet_text)
    with open(handle + '_' + date + '_results.json', 'w') as f:
        json.dump(category, f, indent=1)
        f.close()


if __name__ == "__main__":
    """Main function."""
    print "entered second"
    read_file()
    pass
