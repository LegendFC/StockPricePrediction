### I'm not sure where this goes but this is what I've done. I hope I understood correctly what I was supposed to do.
### These are the features I could think of extracting using Textblob. I didn't see other librarys that would be more useful than 
###     textblob
### I think sentiment will work the best but I did the same thing for subjectivity 
### I also got the number of words, sentences and nouns
### Features:   sentiment - {neutral,positive,negative} OR {neutral,positive,verypositive,negative,verynegative}
###             subjectivity - {neutral,subjective,objective} OR {neutral,subjective,verysubjective,objective,veryobjective}
###             numWords
###             numSentences
###             numNouns

### SENTIMENT
positiveThreshold = .2
negativeThreshold = -.2
for t in tweets:
    analysis = textblob.TextBlob(clean_tweet(t.text))
    sentiment = 'neutral'
    if analysis.sentiment.polarity > positiveThreshold:
        sentiment = 'positive'
    elif analysis.sentiment.polarity < negativeThreshold:
        sentiment = 'negative'


veryPositiveThreshold = .6
positiveThreshold = .2
negativeThreshold = -.2
veryNegativeThreshold = -.6
for t in tweets:
    analysis = textblob.TextBlob(clean_tweet(t.text))
    sentiment = 'neutral'
    if analysis.sentiment.polarity > veryPositiveThreshold:
        sentiment = 'verypositive'
    elif analysis.sentiment.polarity > positiveThreshold:
        sentiment = 'positive'
    elif analysis.sentiment.polarity < veryNegativeThreshold:
        sentiment = 'verynegative'
    elif analysis.sentiment.polarity < negativeThreshold:
        sentiment = 'negative'

### SUBJECTIVITY
subjectiveThreshold = .6
neutralThreshold = .4
for t in tweets:
    analysis = textblob.TextBlob(clean_tweet(t.text))
    subjectivity = 'objective'
    if analysis.sentiment.subjectivity > subjectiveThreshold:
        sentiment = 'subjective'
    elif analysis.sentiment.subjectivity > neutralThreshold:
        sentiment = 'neutral'

verySubjectiveThreshold = .8
subjectiveThreshold = .6
neutralThreshold = .4
objectiveThreshold = .2
for t in tweets:
    analysis = textblob.TextBlob(clean_tweet(t.text))
    subjectivity = 'veryobjective'
    if analysis.sentiment.subjectivity > verySubjectiveThreshold:
        sentiment = 'verysubjective'
    elif analysis.sentiment.subjectivity > subjectiveThreshold:
        sentiment = 'subjective'
    elif analysis.sentiment.subjectivity > neutralThreshold:
        sentiment = 'neutral'
    elif analysis.sentiment.subjectivity > objectiveThreshold:
        sentiment = 'objective'

### LENGTHS
for t in tweets:
    analysis = textblob.TextBlob(clean_tweet(t.text))
    numWords = len(analysis.words)
    numSentences = len(analysis.sentences0)
    numNouns = len(analysis.noun_phrases)



