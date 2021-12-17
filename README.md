# Twitter Vaccination and Pandemic Response
In this project, we aimed to understand the general response to the pandemic and vaccination in the last month. To do so we collected tweet data from the Twitter API, annotated the data using an open coding process and finally performed data analysis. More details on our results can be seen in our paper: A Data Analytic Approach to COVID-19 Discussion and Sentiment on Twitter.

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
