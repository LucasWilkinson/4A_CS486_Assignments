import heapq
print "Assignment_1\n"

class wordNode:
	def __init__(self, word, ps):
		self.word = word
		self.ps = ps
		self.nextWords = {}

	def addNextWord(self, word, ps, prob):
		if (ps in self.nextWords):
			self.nextWords[ps].append((word+ps, prob))
		else:
			self.nextWords[ps] = [(word+ps, prob)]

	def getNextWordKeys(self, ps):
		if (ps in self.nextWords):
			return self.nextWords[ps]
		else:
			return []

	def printNode(self):
		print self.word, self.ps, self.nextWords

def parse(graph):

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
	nodeCount = 0
	wordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[wordKey]
	
	bfsQueue = []
	bfsQueue.append((wordKey, 1, currentNode.word))
	nodeCount += 1
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

				tempWordsToPop += 1		
				newSentence = currentSentence + ' ' + wordGraph[wordKey].word
				bfsQueue.append((wordKey, currentProb*prob, newSentence))
				nodeCount += 1

		wordsToPop = tempWordsToPop

	highestProb = 0
	highestProbSent = ''

	for node, prob, sentence in bfsQueue:
		if prob > highestProb:
			highestProb = prob
			highestProbSent = sentence

	# for index, item in enumerate(bfsQueue):
	# 	if index%10 == 0:
	# 		print item[2]

	return highestProb, highestProbSent, nodeCount

def depthFirstSearch(startingWord, sentenceSpec, wordGraph):
	nodeCount = 1
	firstWordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[firstWordKey]

	dfsStack = [] 
	unvisitedChildren = len(currentNode.getNextWordKeys(sentenceSpec[1]))
	currSent = currentNode.word
	currWord = currentNode.word
	currProb = 1
	dfsStack.append((firstWordKey, currProb, currSent, unvisitedChildren))

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
			nodeCount += 1

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

	return bestProb, bestSentence, nodeCount

def heuristicSearch(startingWord, sentenceSpec, wordGraph, maxProb):
	nodeCount = 1
	openList = []

	firstWordKey = startingWord+sentenceSpec[0]
	currentNode = wordGraph[firstWordKey]

	children = currentNode.getNextWordKeys(sentenceSpec[1])

	for child in children:
		wordKey, currProb = child

		if (wordKey not in wordGraph):
			continue

		currWord = wordGraph[wordKey].word
		currSent = [startingWord, currWord]

		stepsRemaining = len(sentenceSpec) - len(currSent)
		predictedProb = currProb * maxProb ** stepsRemaining

		listEntry = (-predictedProb, currProb, wordKey, list(currSent))
		heapq.heappush(openList, listEntry)
		nodeCount += 1

	while(True):
		try:
			negPredictedProb, currProb, wordKey, currSent = heapq.heappop(openList)
		except IndexError:
			return 0, '', nodeCount

		predictedProb = -negPredictedProb

		if len(currSent) == len(sentenceSpec): # end condition: complete sentence with best probability
			return currProb, listToSentence(currSent), nodeCount

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
			predictedProb = currProb * newChildProb * maxProb ** stepsRemaining
			currChildProb = currProb * newChildProb

			listEntry = (-predictedProb, currChildProb, wordKey, list(currChildSent))
			heapq.heappush(openList, listEntry)
			nodeCount += 1

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

# bfsProb, bfsSentence, dfsProb, dfsSentence, hsProb, hsSentence = generate('benjamin', ['NNP', 'VBD', 'DT', 'JJS', 'NN'], graph)

searchStrategies = ["BREADTH_FIRST"]#, "DEPTH_FIRST", "HEURISTIC"]

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

# running some git tests
# bfs: a queen answered hans up the apple


# OUTPUT
# Breadth First:

# "a son thanked god for the apple" is one of the highest probability sentences (7.08856997623e-06%).

# Depth First:

# "a son thanked god for the water" is one of the highest probability sentences (7.08856997623e-06%).
