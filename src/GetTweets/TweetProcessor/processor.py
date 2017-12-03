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
import textblob

class processor:
    veryPositiveThreshold = .6
    positiveThreshold = .2
    negativeThreshold = -.2
    veryNegativeThreshold = -.6

    verySubjectiveThreshold = .8
    subjectiveThreshold = .6
    neutralThreshold = .4
    objectiveThreshold = .2

    def __init__(self):
        pass

    def getSentiment(self, analysis):
        sentiment = 'neutral'
        if analysis.sentiment.polarity > self.positiveThreshold:
            sentiment = 'positive'
        elif analysis.sentiment.polarity < self.negativeThreshold:
            sentiment = 'negative'
        return sentiment




    def getDetailSentiment(self, analysis):
        sentiment = 'neutral'
        if analysis.sentiment.polarity > self.veryPositiveThreshold:
            sentiment = 'verypositive'
        elif analysis.sentiment.polarity > self.positiveThreshold:
            sentiment = 'positive'
        elif analysis.sentiment.polarity < self.veryNegativeThreshold:
            sentiment = 'verynegative'
        elif analysis.sentiment.polarity < self.negativeThreshold:
            sentiment = 'negative'
        return sentiment

### SUBJECTIVITY
    def getSubjectivity(self, analysis):
        sub = 'objective'
        if analysis.sentiment.subjectivity > self.subjectiveThreshold:
            sub = 'subjective'
        elif analysis.sentiment.subjectivity > self.neutralThreshold:
            sub = 'neutral'
        return sub


    def getDetailSubjectivity(self, analysis):
        sub = 'veryobjective'
        if analysis.sentiment.subjectivity > self.verySubjectiveThreshold:
            sub = 'verysubjective'
        elif analysis.sentiment.subjectivity > self.subjectiveThreshold:
            sub = 'subjective'
        elif analysis.sentiment.subjectivity > self.neutralThreshold:
            sub = 'neutral'
        elif analysis.sentiment.subjectivity > self.objectiveThreshold:
            sub = 'objective'
        return sub

### LENGTHS
    def getNumWords(self, analysis):
        return len(analysis.words)

    def getNumSentences(self, analysis):
        return len(analysis.noun_phrases)

    def getNumNouns(self, analysis):
        return len(analysis.noun_phrases)



