import tweepy,getopt,sys
#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		print(status.text)

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