# Stock Price Prediction (UCLA CS145 project)
This project is the course project from CS145 in UCLA.

# Get start
First, install tweepy:
> pip install tweepy

Signup the tweet account:
Username: tu_yukai
Phone: 3105629182
Password: cs145cs145

Create the application: stock-prediction-cs145

Generate access token and token secret.

Use GetOldTweets-python to get the target tweets.

Install textblob
> pip install textblob

Install pandas-datareader
> pip install pandas-datareader

To crawl the old Tweets, type command
> python src/GetTweets/getOldTweets.py --querysearch="Google" --since 2017-01-01 --until 2017-11-01


To crawl the real time Tweets, type command
> python src/GetTweets/getRealtimeTweets.py --querysearch="Google"

To crawl the stock price, type command
>python src/GetDJIA/djia.py --symbol='GOOG' --since='2017-01-01' --until='2017-10-01'