import pandas_datareader as pdr
from datetime import datetime
from datetime import date
import dateutil.parser, sys, getopt, codecs


def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		print "you should input the target search word like --symbol='GOOG' --since='2017-01-01' --until='2017-10-01'"

		return

	try:
		opts, args = getopt.getopt(argv, "", ("since=", "until=", "symbol=", "output="))

		startDate = dateutil.parser.parse('2017-01-01')
		endDate = dateutil.parser.parse('2017-10-01')
		symbols = "GOOG"
		outputFileName = "output_got.csv"

		for opt,arg in opts:

			if opt == '--since':
				startDate = dateutil.parser.parse(arg)

			elif opt == '--until':
				endDate = dateutil.parser.parse(arg)

			elif opt == '--symbol':
				symbols = arg

			elif opt == '--output':
				outputFileName = arg

		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		stockPrice = pdr.get_data_yahoo(symbols=symbols, \
										start=datetime(startDate.year, startDate.month, startDate.day),\
										end=datetime(endDate.year, endDate.month, endDate.day))
		print(stockPrice)
		stockPrice.to_csv(outputFile)
	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])