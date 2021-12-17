# Twitter Vaccination and Pandemic Response
In this project, we aimed to understand the general response to the pandemic and vaccination in the last month. To do so we collected tweet data from the Twitter API, annotated the data using an open coding process and finally performed data analysis. More details on our results can be seen in our paper: A Data Analytic Approach to COVID-19 Discussion and Sentiment on Twitter.

## General Overview and Results

In this project we collected a sample of tweets with the goal of understanding the current conversations about the COVID-19 pandemic in the English-speaking world. This sample was collected using query keywords that are relevant to the pandemic and that could give us access to the differ- ent conversations around it, such as “covid”, “lockdown”, and “vaccine”. We then conducted an open coding on a sub- set of our sample to gather the main topics on these discus- sions, striving to make our topics as well-defined as possible. These included topics such as “Politics and Global Affairs”, “Science”, “Pro-vaxx” and “Anti-vaxx”.

Subsequently, we conducted a variety of data analyses to understand the type of engagement Twitter users have with these topics, as well as the sentiment with which they engage with them. We also performed TF-IDF analysis to obtain the ten most relevant words that characterize each topic and a network analysis to investigate the keywords that appear in the same tweets the most.

Our results show that COVID-related tweets generally have a negative sentiment. However, the group which seems to be the most negative of them all is the anti-vaxxers: al- most 60% of their tweets are negative. We found that tweets about scientific research are the most neutral, and that pro- vaxx tweets occur equally in positive, neutral and negative tweets. Our TF-IDF analysis shows that tweets about sci- entific research and about politics mention Africa more of- ten than any other place, probably due to the fact that the data was collected when Omicron was reported and investi- gated by African scientists. Tweets about health and safety measures mainly talk about lockdowns, while anti-vaxx dis- course is best characterized by the use of the word “lied”.

Furthermore, we analyzed concurrent usage of the key- words used to collect our data and found that “vaccine” and “covid” occur together most often relative to our other key- words. We discuss and link our different results to provide a synthesized overview of the overall response to vaccination and the pandemic as suggested by our data. Finally, we dis- cuss some of the limitations of this data science project such as the technical limitations imposed by the basic Twitter API access we had for data collection.
## Setup

### Dependencies

#### Using conda

Run `conda create --name <envname> --file requirements.txt`.

#### Using pip

Run `pip -r requirements.txt`.

### Dotenv

Create a .env file with required variables for authentication.

## Running 

1. Collect data by running `python3 src/collect_data.py`
2. Perform analysis using the other python files.

