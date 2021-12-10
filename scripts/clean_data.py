import pandas

#Facilitates relabeling. Ex) allows all tweets labeled "ov" to be changed to "v".
def change_labels(df, labelPairs):
    for pair in labelPairs:
        df.loc[df.label == pair[0], "label"] = pair[1]
    return df

def clean_data(df):
    punc = '!"$%&()*+,”-“./‘:’;<=>?[\]^_`{|}~'
    punc += "'"

    df["tweet"] = df["tweet"].str.lower() #lowercase
    df["tweet"] = df["tweet"].apply(lambda x: " ".join(filter(lambda y: '&amp;' not in y, x.split()))) #words with weird ampersands removed
    df["tweet"] = df["tweet"].apply(lambda x: " ".join(filter(lambda y: 'https://' not in y, x.split()))) #links removed
    df["tweet"] = df["tweet"].apply(lambda x: ''.join([i for i in x if i not in punc])) #remove punctuation
    df["tweet"] = df["tweet"].apply(lambda x: x.encode('ascii', 'ignore').decode('ascii')) #removes emojis
    df["tweet"] = df["tweet"].apply(lambda x: " ".join(filter(lambda y: y[0]!='@', x.split()))) #remove mentions (@user)
    
    return df


def main():
    inputFile = "data/annotated_sample.tsv"
    outputFile = "data/annotated_sample_clean.tsv"
    labelPairs = [] # list of tuples that we want to change the label of. Ex) ("v", "o") changes all labels "v" to "o"

    df = pandas.read_csv(inputFile, sep="\t")
    df = clean_data(df)

    if not labelPairs == []:
        df = change_labels(df, labelPairs)
    
    df.to_csv(path_or_buf = outputFile, sep="\t", index=False)




if __name__ == "__main__":
    main()


    #get rid of urls and user names, lowercase, emojis, keep hashtags, remove punctuation (not dashes or #)