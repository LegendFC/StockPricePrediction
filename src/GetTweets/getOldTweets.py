# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs,textblob,re,json
import TweetProcessor

if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=", "stdout=", "isJson=", 'count='))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"
		isStdOut = False
		isJson = False
		count = 0
		targetCount = -1

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg

			elif opt == '--stdout':
				isStdOut = True
			
			elif opt == '--isJson':
				isJson = True

			elif opt == '--count':
				targetCount = arg

		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		if not isJson:
			outputFile.write('date\tsentiment\tdetailSentiment\tsubjectivity\tdetailSubjectivity\tnumWords\tnumSentences\tnumNouns')
		processor = TweetProcessor.processor()
		print('Searching...\n')

		def clean_tweet(tweet):
			return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

		def receiveBuffer(tweets):
			for t in tweets:
				# set sentiment
				analysis = textblob.TextBlob(clean_tweet(t.text))
				text = clean_tweet(t.text)
				if isStdOut:
					print t.username + "\n" + t.text + "\n" + t.date.strftime("%Y-%m-%d %H:%M") + "\n" + t.geo
				if isJson:
					json.dump({'username': t.username, 'time': t.date.strftime("%Y-%m-%d %H:%M"), 'text': t.text, 'geo': t.geo}, outputFile)
					outputFile.write('\n')
				else:
					analysis = textblob.TextBlob(text)
					outputFile.write(('\n%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (t.date.strftime("%Y-%m-%d"), processor.getSentiment(analysis),processor.getDetailSentiment(analysis), processor.getSubjectivity(analysis), processor.getDetailSubjectivity(analysis),\
																processor.getNumWords(analysis), processor.getNumSentences(analysis), processor.getNumNouns(analysis))))

			outputFile.flush();
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
