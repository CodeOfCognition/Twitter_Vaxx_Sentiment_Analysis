import argparse
import json
import pandas

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<annotated_data.csv>', required=True)
    args = parser.parse_args()

    return args.i

#checks whether there are any invalid labels
def check_label_validity(df, labels):
    df_invalid = df.loc[~df.topic.isin(labels)]
    numInvalidEntries = len(df_invalid)
    if numInvalidEntries > 0:
        print(f"{numInvalidEntries} The following entries have invalid labels:")
        print(df_invalid)
        return -1
    else:
        return 0

def get_counts(df, labels):
    counts = dict()
    for l in labels:
        counts[l] = len(df.loc[df.topic == l])
    return counts

def get_sentiments(df, labels):
    sentiments = dict()
    for l in labels:
        sentiments[l] = dict()
    for l in labels:
        numEntries = len(df.loc[df.topic == l])
        sentiments[l]["negative"] = len(df[(df.topic == l) & (df.sentiment == -1)]) / numEntries
        sentiments[l]["neutral"] = len(df[(df.topic == l) & (df.sentiment == 0)]) / numEntries
        sentiments[l]["positive"] = len(df[(df.topic == l) & (df.sentiment == 1)]) / numEntries
        sentiments[l]["average"] = (sentiments[l]["positive"] - sentiments[l]["negative"])
    return sentiments

def main():
    # inputFile = parse_args()
    inputFile = "data/raw/annotated_data.tsv"
    outputFile = "data/results/sentiment_results.json"
    df = pandas.read_csv(inputFile, sep="\t")
    df["topic"] = df["topic"].str.lower()

    labels = ["g", "s", "p", "a", "m", "o", "ov"]
    check_label_validity(df, labels)
    counts = get_counts(df, labels)
    sentiment = get_sentiments(df, labels)

    output = {"counts" : counts, "sentiment analysis": sentiment}

    with open(outputFile, "wt") as f:
        json.dump(output, f)


    



if __name__ == "__main__":
    main()

