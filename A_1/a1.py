print "Assignment_1"

class wordNode:
	def __init__(self, word, ps):
		self.word = word
		self.ps = ps
		self.nextWords = {}

	def addNextWord(self, word, ps, prob):
		if (ps in self.nextWords):
			self.nextWords[ps].append((word, prob))
		else:
			self.nextWords[ps] = [(word, prob)]

	def getNextWords(self, ps):
		if (ps in self.nextWords):
			return self.nextWords[ps]
		else:
			return []

	def printNode(self):
		print self.word, self.ps, self.nextWords

def parse(graph):

	returnDict = {}
	lines = graph.split('\n')

	for line in lines:
		line = line.strip()
		
		word1, word2, prob = line.split('//')
		word1, word1Ps = word1.split('/')
		word2, word2Ps = word2.split('/')

		if (word1 not in returnDict):
			returnDict[word1] = wordNode(word1, word1Ps)
		
		returnDict[word1].addNextWord(word2, word2Ps, float(prob))	

	return returnDict

def generate(startingWord, sentenceSpec, graph):
	wordGraph = parse(graph) 
	currentNode = wordGraph[startingWord]

	bfsQueue = []
	bfsQueue.append((currentNode.word, 1, currentNode.word))
	wordsToPop = 1
	
	for ps in sentenceSpec[1:]:
		print ps

		numWordsToPop = 0
		for i in range(wordsToPop):
			currentWord, currentProb, currentSentence = bfsQueue.pop(0)

			if (currentWord not in wordGraph):
				continue

			nextWords = wordGraph[currentWord].getNextWords(ps)
			numWordsToPop += len(nextWords)

			for word, prob in nextWords:
				newSentence = currentSentence + ' ' + word
				bfsQueue.append((word, currentProb*prob, newSentence))

		wordsToPop = numWordsToPop

	highestProb = 0
	highestProbSent = ''

	for node, prob, sentence in bfsQueue:
		if prob > highestProb:
			highestProb = prob
			highestProbSent = sentence

	for index, item in enumerate(bfsQueue):
		if index%10 == 0:
			print item[2]

	return highestProbSent

open_file = open('input.txt', 'r')
graph = open_file.read()

print generate('a', ['DT', 'NN', 'VBD', 'NNP', 'IN', 'DT', 'NN'], graph)
