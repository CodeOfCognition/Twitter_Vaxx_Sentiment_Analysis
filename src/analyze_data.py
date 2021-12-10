import pandas
import math
import json

def get_idf(df, uniqueWords, topics):
    idfDict = dict.fromkeys(uniqueWords, 0)

    #for each topic, see if each word occurs in that topic
    for t in topics:
        tDF = df.loc[df["topic"] == t] #dataframe with only rows of topic t
        tWords = set(tDF["tweet"].str.cat(sep=" ").split()) #all words in lDF
        for word in idfDict.keys():
            if word in tWords:
                idfDict[word] = idfDict[word] + 1
    # at this point each word in idfDict contains the number of topics that uses that word

    for word in idfDict.keys():
        idfDict[word] = math.log((len(topics) / idfDict[word]), 10)

    return idfDict


def get_tf(df, uniqueWords, topics):
    tfDict = dict()
    for t in topics:
        tfDict[t] = dict.fromkeys(uniqueWords, 0)
    for t in topics:
        lDF = df.loc[df["topic"] == t] #dataframe with only rows of topic t
        lWords = lDF["tweet"].str.cat(sep=" ").split() #all words in lDF
        for word in lWords:
            tfDict[t][word] = tfDict[t][word] + 1
    return tfDict


def get_tfidf(df, uniqueWords, topics, idfDict, tfDict, n):
    tfidfDict = dict()
    topWordsDict = dict.fromkeys(topics, None)
    n = 10
    for t in topics:
        tfidfDict[t] = dict()
        for word in uniqueWords:
            tfidfDict[t][word] = tfDict[t][word] * idfDict[word]
    for t in topics:
        tfidfDict[t] = dict(sorted(tfidfDict[t].items(), key=lambda x:x[1], reverse=True)) #sort the tfidf values for a pony
        topWords = list(tfidfDict[t].keys())[:n] # get n items
        topWordsDict[t] = topWords
    return topWordsDict


def main():
    inputFile = "data/annotated_sample_clean.tsv"
    outputFile = "data/results"

    df = pandas.read_csv(inputFile, sep="\t")
    uniqueWords = set(df["tweet"].str.cat(sep=" ").split())
    topics = set(df["topic"].str.cat(sep=" ").split())
    idfDict = get_idf(df, uniqueWords, topics)
    tfDict = get_tf(df, uniqueWords, topics)
    results = get_tfidf(df, uniqueWords, topics, idfDict, tfDict, 5)
    print("look")
    print(results)
    with open(outputFile, "wt") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()
