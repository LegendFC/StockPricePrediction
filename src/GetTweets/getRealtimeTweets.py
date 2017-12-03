import tweepy,getopt,sys,TweetProcessor
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	def __init__(self):
		self.processor = TweetProcessor.processor()

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def on_status(self, status):
		analysis = textblob.TextBlob(self.clean_tweet(status.text))
		print ('\n%s;%s;%s;%s;%s;%s;%s' % (processor.getSentiment(analysis),processor.getDetailSentiment(analysis), processor.getSubjectivity(analysis), processor.getDetailSubjectivity(analysis),\
																processor.getNumWords(analysis), processor.getNumSentences(analysis), processor.getNumNouns(analysis)))

consumer_key = "CCTQiQkVMkLwlsRslD6DhBJOU"
consumer_secret = "dpJdX1xFdDk3o0baxSiNhd2WbDhr9VJUkmOUZLKVjJCMHgO87h"
access_token = "923018874601160704-nRH0UIpkw3kTFsoSrC3479qGb3cYnh1"
access_token_secret = "1qD2lYpJyYieMdrbJ4SUZRkOe7jInkECxFsTnW5zN3Mji"

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		print "you should input the target search word like --querysearch='Google'"
		return

	try:
		opts, args = getopt.getopt(argv, "", ("querysearch="))
		query = ""
		for opt,arg in opts:
			if opt == '--querysearch':
				query = arg

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)

		myStreamListener = MyStreamListener()
		myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
		myStream.filter(track=[query])
	except arg:
		print('Arguments parser error, try -h' + arg)

if __name__ == '__main__':
	main(sys.argv[1:])