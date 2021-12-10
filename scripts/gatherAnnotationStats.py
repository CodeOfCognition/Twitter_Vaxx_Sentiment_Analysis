import argparse
import pandas

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='<annotated_data.csv>', required=True)
    args = parser.parse_args()

    return args.i

#Facilitates relabeling. Ex) allows all tweets labeled "ov" to be changed to "v".
def change_labels(df, labelPairs):
    for pair in labelPairs:
        df.loc[df.label == pair[0], "label"] = pair[1]
    return df

#checks whether there are any invalid labels
def check_label_validity(df, labels):
    df_invalid = df.loc[~df.label.isin(labels)]
    numInvalidEntries = len(df_invalid)
    if numInvalidEntries > 0:
        print(f"{numInvalidEntries} The following entries have invalid labels:")
        print(df_invalid)
        return -1
    else:
        print("all entries correctly labeled!")
        return 0

def get_stats(df, labels):
    counts = dict()
    for l in labels:
        counts[l] = len(df.loc[df.label == l])
    return counts

def main():
    # inputFile = parse_args()
    inputFile = "data/annotated_sample2.tsv"
    df = pandas.read_csv(inputFile, sep="\t")
    df["label"] = df["label"].str.lower()

    # labelPairs = [("v", "o")] # list of tuples that we want to change the label of. Ex) ("v", "o") changes all labels "v" to "o"
    # df = change_labels(df, labelPairs)

    labels = ["g", "s", "p", "a", "m", "o", "ov"]
    check_label_validity(df, labels)
    counts = get_stats(df, labels)

    print(counts)



if __name__ == "__main__":
    main()


    #get rid of urls and user names, lowercase, emojis, keep hashtags