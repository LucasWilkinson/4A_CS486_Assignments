import heapq
print "Assignment_1\n"

"""
This class represents a single node in our graph. 
This node is to placed into a dictionary using the word concatenated with its part of 
speech as the key. 
"""
class wordNode:
	def __init__(self, word, ps):
		"""
		Initializer 
		"""
		self.word = word
		self.ps = ps
		self.nextWords = {}

	def addNextWord(self, word, ps, prob):
		"""
		This function stores words that follow the node's word and organizes them by parts 
		of speech
		"""
		if (ps in self.nextWords):
			self.nextWords[ps].append((word+ps, prob))
		else:
			self.nextWords[ps] = [(word+ps, prob)]

	def getNextWordKeys(self, ps):
		"""
		Description:
			Finds all words that follow this node's word that have the part of speech ps.

		Returns:
			This function returns a list of words that follow this node's word. The list is a 
			list of tuples with the format (wordkey, prob). 

			Where wordkey represents the next word and its part of speech concatenated together 
			(this should be used to index the dictionary that contains all of these nodes).

			Where prob represents the probability this word follows the node's word.
		"""
		if (ps in self.nextWords):
			return self.nextWords[ps]
		else:
			return []

	def printNode(self):
		"""
		Prints the attributes of the node for debugging 
		"""
		print self.word, self.ps, self.nextWords

def parse(graph):
	"""
	This function takes the input word list and probability pairs and places them into a dictionary structure.
	Each dictionary entry's key is the first word and its part of speech concatenated, and the value is a wordNode
	containing the data of key. 

	The function then takes the next words from the input and places them into the 'nextWords' attribute dictionary.
	"""

	returnDict = {}
	lines = graph.split('\n')
	highestProb = 0

	for line in lines:
		line = line.strip()
		
		word1, word2, prob = line.split('//')
		word1, word1Ps = word1.split('/')
		word2, word2Ps = word2.split('/')

		prob = float(prob)

		if prob > highestProb:
			highestProb = prob

		wordKey = word1+word1Ps

		if (wordKey not in returnDict):
			returnDict[wordKey] = wordNode(word1, word1Ps)
		
		returnDict[wordKey].addNextWord(word2, word2Ps, prob)	

	return returnDict, highestProb

def breadthFirstSearch(startingWord, sentenceSpec, wordGraph):
	"""
	Description:
		Searches the passed in graph for a sentence starting with startingWord that complies with 
		sentenceSpec and has the highest probability using a breadth first search strategy.

	returns:
		prob, sentence, nodesVisited

		Where prob the probability the return sentence occurs.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 0
	wordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[wordKey]
	
	bfsQueue = []
	bfsQueue.append((wordKey, 1, currentNode.word))
	nodesVisited += 1
	wordsToPop = 1
	
	for ps in sentenceSpec[1:]:

		tempWordsToPop = 0
		for i in range(wordsToPop):
			currentWordKey, currentProb, currentSentence = bfsQueue.pop(0)

			if (currentWordKey not in wordGraph):
				continue

			nextWordsKeys = wordGraph[currentWordKey].getNextWordKeys(ps)

			for wordKey, prob in nextWordsKeys:

				if (wordKey not in wordGraph):
					continue

				# travelling to child

				tempWordsToPop += 1		
				newSentence = currentSentence + ' ' + wordGraph[wordKey].word
				bfsQueue.append((wordKey, currentProb*prob, newSentence))
				nodesVisited += 1

		wordsToPop = tempWordsToPop

	highestProb = 0
	highestProbSent = ''

	for node, prob, sentence in bfsQueue:
		if prob > highestProb:
			highestProb = prob
			highestProbSent = sentence

	return highestProb, highestProbSent, nodesVisited

def depthFirstSearch(startingWord, sentenceSpec, wordGraph):
	"""
	Description:
		Searches the passed in graph for a sentence starting with startingWord that complies with 
		sentenceSpec and has the highest probability using a depth first search strategy.

	returns:
		prob, sentence, nodesVisited

		Where prob the probability the return sentence occurs.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 0
	firstWordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[firstWordKey]

	dfsStack = [] 
	unvisitedChildren = len(currentNode.getNextWordKeys(sentenceSpec[1]))
	currSent = currentNode.word
	currWord = currentNode.word
	currProb = 1
	dfsStack.append((firstWordKey, currProb, currSent, unvisitedChildren))
	nodesVisited += 1

	bestProb = 0
	bestSentence = ''

	while len(dfsStack) != 0:
		currWordKey, currProb, currSent, unvisitedChildren = dfsStack[-1]
		currentNode = wordGraph[currWordKey]
		depth = len(dfsStack) - 1

		if unvisitedChildren > 0:
			nextPs = sentenceSpec[depth + 1]

			nextWordKey, nextProb = currentNode.getNextWordKeys(nextPs)[unvisitedChildren - 1]

			dfsStack[-1] = (currWordKey, currProb, currSent, unvisitedChildren - 1)
			
			if (nextWordKey not in wordGraph):
				continue

			nextChild = wordGraph[nextWordKey]

			# travelling to child

			currWord = nextChild.word
			currWordKey = nextWordKey
			currProb = nextProb*currProb
			currSent = currSent + ' ' + currWord
			depth += 1
			nodesVisited += 1

			if (depth + 1) >= len(sentenceSpec):
				unvisitedChildren = 0
				if currProb > bestProb:
					bestProb = currProb
					bestSentence = currSent
			else:
				nextPs = sentenceSpec[depth + 1]
				unvisitedChildren = len(nextChild.getNextWordKeys(nextPs))
				dfsStack.append((currWordKey, currProb, currSent, unvisitedChildren)) 

		else:
			dfsStack.pop()

	return bestProb, bestSentence, nodesVisited

def heuristic(currProb, maxProb, stepsRemaining):
	return currProb * maxProb ** stepsRemaining

def heuristicSearch(startingWord, sentenceSpec, wordGraph, maxProb):
	"""
	Description:
		Searches the passed in graph for a sentence starting with startingWord that complies with 
		sentenceSpec and has the highest probability using a heuristic search strategy (A*) with the
		heuristic being the 
			h(n) = maxProb^numWordsRemaing.
		maxProb = max probability between any two words in the graph 
		numWordsRemaing = the number of words still needed to complete the sentenceSpec

	returns:
		prob, sentence, nodesVisited

		Where prob the probability the return sentence occurs.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 1
	openList = []

	firstWordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[firstWordKey]

	children = currentNode.getNextWordKeys(sentenceSpec[1])

	for child in children:
		wordKey, currProb = child

		if (wordKey not in wordGraph):
			continue

		# travelling to child

		currWord = wordGraph[wordKey].word
		currSent = [startingWord, currWord]

		stepsRemaining = len(sentenceSpec) - len(currSent)
		predictedProb = heuristic(currProb, maxProb, stepsRemaining)

		listEntry = (-predictedProb, currProb, wordKey, list(currSent))
		heapq.heappush(openList, listEntry)
		nodesVisited += 1

	while(True):
		try:
			negPredictedProb, currProb, wordKey, currSent = heapq.heappop(openList)
		except IndexError:
			return 0, '', nodesVisited

		predictedProb = -negPredictedProb

		if len(currSent) == len(sentenceSpec): # end condition: complete sentence with best probability
			return currProb, listToSentence(currSent), nodesVisited

		currentNode = wordGraph[wordKey]
		depth = len(currSent)
		children = currentNode.getNextWordKeys(sentenceSpec[depth])

		for child in children:
			wordKey, newChildProb = child

			if (wordKey not in wordGraph):
				continue

			currWord = wordGraph[wordKey].word
			currChildSent = currSent + [currWord]

			stepsRemaining = len(sentenceSpec) - len(currSent)
			predictedProb = heuristic(currProb * newChildProb, maxProb, stepsRemaining)
			currChildProb = currProb * newChildProb

			listEntry = (-predictedProb, currChildProb, wordKey, list(currChildSent))
			heapq.heappush(openList, listEntry)
			nodesVisited += 1

def listToSentence(sentenceList):
	sentence = ''
	for word in sentenceList:
		sentence = sentence + word + ' '
	return sentence.rstrip()

def generate(startingWord, sentenceSpec, searchStrategy,  graph):
	wordGraph, maxProb = parse(graph) 
	
	prob = 0
	sentence = ' '
	nodesVisited = 0

	if (searchStrategy == "BREADTH_FIRST"):
		prob, sentence, nodesVisited = breadthFirstSearch(startingWord, sentenceSpec, wordGraph)
	elif (searchStrategy == "DEPTH_FIRST"):
		prob, sentence, nodesVisited = depthFirstSearch(startingWord, sentenceSpec, wordGraph)
	elif (searchStrategy == "HEURISTIC"):
		prob, sentence, nodesVisited = heuristicSearch(startingWord, sentenceSpec, wordGraph, maxProb)

	return prob, sentence, nodesVisited

open_file = open('input.txt', 'r')
graph = open_file.read()

searchStrategies = ["BREADTH_FIRST", "DEPTH_FIRST", "HEURISTIC"]

for searchStrategy in searchStrategies:
	# prob, sentence, nodesVisited = generate('a', ['DT', 'NN', 'VBD', 'NNP', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS', 'NNS',], searchStrategy, graph)
	# prob, sentence, nodesVisited = generate('benjamin', ['NNP','VBD','DT','NN'], searchStrategy, graph)
	# prob, sentence, nodesVisited = generate('a', ['DT','NN','VBD','NNP'], searchStrategy, graph)
	# prob, sentence, nodesVisited = generate('benjamin', ['NNP','VBD','DT','JJS','NN'], searchStrategy, graph)
	prob, sentence, nodesVisited = generate('a', ['DT','NN','VBD','NNP','IN','DT','NN'], searchStrategy, graph)

	print '-' + searchStrategy + '-'
	print 'Sentence: ' + sentence
	print 'Probability:' + str(prob*100) + '%'
	print 'Number of nodes visited: ' + str(nodesVisited) + '\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
