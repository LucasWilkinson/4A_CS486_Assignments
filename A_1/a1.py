import heapq
print "Assignment_1\n"

class wordNode:
	"""
	This class represents a single node in our graph. 
	This node is to placed into a dictionary using the word concatenated with its part of 
	speech as the key. 
	"""

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
	Description:
		This function takes the input word list and probability pairs and places them into a dictionary structure.
		Each dictionary entry's key is the first word and its part of speech concatenated, and the value is a wordNode
		containing the data of key. 

		The function then takes the next words from the input and places them into the 'nextWords' attribute dictionary.
		While iterating through the list, the function also keeps track of the highest existing probability in the list.

	returns: 
		returnDict, highestProb

		The dictionary of words and their next words.
		The highest probability existing in the input list.
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

		Where prob the probability the return sentence occurs. If the sentence is invalid, 
		a probability of -1 will be returned.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 0
	wordKey = startingWord+sentenceSpec[0]

	if (wordKey not in wordGraph):
		return -1, '', nodesVisited

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

	highestProb = -1
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

		Where prob the probability the return sentence occurs. If the sentence is invalid, 
		a probability of -1 will be returned.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 0
	dfsStack = [] 
	
	firstWordKey = startingWord+sentenceSpec[0]

	if (firstWordKey not in wordGraph):
		return -1, '', nodesVisited

	currentNode = wordGraph[firstWordKey]

	unvisitedChildren = len(currentNode.getNextWordKeys(sentenceSpec[1]))
	currSent = currentNode.word
	currWord = currentNode.word
	currProb = 1
	dfsStack.append((firstWordKey, currProb, currSent, unvisitedChildren))
	nodesVisited += 1

	bestProb = -1
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

			# If we are at the end of our sentenceSpec see if this complete sentence is
			# better then the last best complete sentence 
			if depth >= len(sentenceSpec) - 1:
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


class maxHeap:
	"""
	This class is a max heap wrapper for the heapq library in python to be used by the 
	heuristicSearch function.
	"""

	def __init__(self):
		self.heap = []

	def push(self, predictedProb, currProb, wordKey, currSent):
		# the predicted prob is made negative because heapq operates as a min heap so by making the 
		# probability negative so we can make it behave like a max heap, we just need to multiply it 
		# by negative one when we pop
		listEntry = (-predictedProb, currProb, wordKey, list(currSent))
		heapq.heappush(self.heap, listEntry)

	def pop(self): 
		negPredictedProb, currProb, wordKey, currSent = heapq.heappop(self.heap)
		# the popped probability is negative (discussed in the push function), so must be 
		# so must be multiplied by negative one to rectify it
		predictedProb = -negPredictedProb
		return predictedProb, currProb, wordKey, currSent



def heuristic(currProb, maxProb, stepsRemaining):
	"""
	Description:
		This function calculates the heuristic of the current sentence, the
		highest probability it could have after being a complete sentence. 

	returns: 
		The heuristic, which is the product of the current sentence's probability
		and the best probability in the input file to the exponent of the number
		words remaining.
	"""
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

		Where prob the probability the return sentence occurs. If the sentence is invalid, 
		a probability of -1 will be returned.
		Where sentence is the sentence found with the highest probability
		Where nodesVisited represents the number of nodes (words) considered in the search
	"""
	nodesVisited = 1
	openList = maxHeap()

	firstWordKey = startingWord+sentenceSpec[0]

	if (firstWordKey not in wordGraph):
		return -1, '', nodesVisited

	currentNode = wordGraph[firstWordKey]
	nodesVisited += 1

	children = currentNode.getNextWordKeys(sentenceSpec[1])

	# initializing the heap
	for child in children:
		wordKey, currProb = child

		if (wordKey not in wordGraph):
			continue

		# travelling to child

		currWord = wordGraph[wordKey].word
		currSent = [startingWord, currWord]

		stepsRemaining = len(sentenceSpec) - len(currSent)
		predictedProb = heuristic(currProb, maxProb, stepsRemaining)

		openList.push(predictedProb, currProb, wordKey, list(currSent))
		nodesVisited += 1

	# main search loop
	while(True):
		try:
			predictedProb, currProb, wordKey, currSent = openList.pop()
		except IndexError:
			return -1, '', nodesVisited

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
			currChildProb = currProb * newChildProb
			predictedProb = heuristic(currChildProb, maxProb, stepsRemaining)
			
			openList.push(predictedProb, currChildProb, wordKey, list(currChildSent))
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
