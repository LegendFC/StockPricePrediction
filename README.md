# Stock Price Prediction (UCLA CS145 project)
This project is the course project from CS145 in UCLA.

# Get start
First, install tweepy:
> pip install tweepy

Install textblob
> pip install textblob

Install download_corpora
> python -m textblob.download_corpora

Install pandas-datareader
> pip install pandas-datareader

The code have three different components under the src directory: Analysis, GetDJIA and GetTweets. GetTweets can get the tweets from Tiwtter based on the keyword, start time and end time; GetDJIA can crawl the data from the YahooFinance with specific company code; Anaysis directory contains three different model which use the tweets as the input and generate the output result.

The run.sh will analysis the data using three provided models. It may cost 10 minutes to generate the results. The result will be saved into the files:modelresult.png, NN_emotion.png and NN_price.png. The result should be the same with the picture in our report.
