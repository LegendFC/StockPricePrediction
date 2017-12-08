python src/GetTweets/getOldTweets.py --querysearch="Texas Instruments" --since="2016-12-01" --until="2017-12-01" --output="TXN_data.txt"
python src/GetDJIA/djia.py --symbol='TXN' --since='2016-12-01' --until='2017-12-01' --output="TXN_price.txt"
python src/Analysis/lr_svm_model.py
python src/Analysis/NN_Model_for_emotion.py
python src/Analysis/NN_Model_for_price.py