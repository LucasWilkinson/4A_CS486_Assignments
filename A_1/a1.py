print "Assignment_1\n"

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


def breadthFirstSearch(startingWord, sentenceSpec, wordGraph):
	currentNode = wordGraph[startingWord]
	
	bfsQueue = []
	bfsQueue.append((currentNode.word, 1, currentNode.word))
	wordsToPop = 1
	
	for ps in sentenceSpec[1:]:

		tempWordsToPop = 0
		for i in range(wordsToPop):
			currentWord, currentProb, currentSentence = bfsQueue.pop(0)

			if (currentWord not in wordGraph):
				continue

			nextWords = wordGraph[currentWord].getNextWords(ps)
			tempWordsToPop += len(nextWords)

			for word, prob in nextWords:
				newSentence = currentSentence + ' ' + word
				bfsQueue.append((word, currentProb*prob, newSentence))

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

	return highestProb, highestProbSent

def zzdepthFirstSearch(startingWord, sentenceSpec, wordGraph):
	currentNode = wordGraph[startingWord]

	dfsStack = [] 
	unvisitedChildren = currentNode.getNextWords(sentenceSpec[1])
	print sentenceSpec[1], unvisitedChildren
	currSent = currentNode.word
	currWord = currentNode.word
	currProb = 1
	dfsStack.append((currWord, currProb, currSent, unvisitedChildren))

	bestProb = 0
	bestSentence = ''

	while len(dfsStack) != 0:
		currWord, currProb, currSent, unvisitedChildren = dfsStack[-1]
		
		if len(unvisitedChildren) > 0:
			# pop the next unvisited child from the stack entry
			# NOTE: unvisitedChildren is a copy of dfsStack[-1][3], however for 
			# here we use dfsStack[-1][3] so it updates the actual stack entry
			nextWord, nextProb = dfsStack[-1][3].pop(0)

			if (nextWord not in wordGraph):
				continue

			nextChild = wordGraph[nextWord]

			currWord = nextChild.word
			currProb = nextProb*currProb
			currSent = currSent + ' ' + currWord

			if len(dfsStack) + 1 < len(sentenceSpec):
				nextPs = sentenceSpec[len(dfsStack) + 1]
				unvisitedChildren = nextChild.getNextWords(nextPs)	
			else:
				unvisitedChildren = []

				print currProb, currSent

				if currProb > bestProb:
					bestProb = currProb
					bestSentence = currSent

			dfsStack.append((currWord, currProb, currSent, unvisitedChildren)) 
				
		else:
			dfsStack.pop()

	return bestProb, bestSentence

def depthFirstSearch(startingWord, sentenceSpec, wordGraph):
	currentNode = wordGraph[startingWord]

	dfsStack = [] 
	unvisitedChildren = len(currentNode.getNextWords(sentenceSpec[1]))
	currSent = currentNode.word
	currWord = currentNode.word
	currProb = 1
	dfsStack.append((currWord, currProb, currSent, unvisitedChildren))

	bestProb = 0
	bestSentence = ''

	while len(dfsStack) != 0:
		currWord, currProb, currSent, unvisitedChildren = dfsStack[-1]
		currentNode = wordGraph[currWord]
		depth = len(dfsStack) - 1

		if unvisitedChildren > 0:
			nextPs = sentenceSpec[depth + 1]

			nextWord, nextProb = currentNode.getNextWords(nextPs)[unvisitedChildren - 1]

			dfsStack[-1] = (currWord, currProb, currSent, unvisitedChildren - 1)
			
			if (nextWord not in wordGraph):
				continue

			nextChild = wordGraph[nextWord]

			currWord = nextChild.word
			currProb = nextProb*currProb
			currSent = currSent + ' ' + currWord
			depth += 1

			if (depth + 1) >= len(sentenceSpec):
				unvisitedChildren = 0
				if currProb > bestProb:
					bestProb = currProb
					bestSentence = currSent
			else:
				nextPs = sentenceSpec[depth + 1]
				unvisitedChildren = len(nextChild.getNextWords(nextPs))
				dfsStack.append((currWord, currProb, currSent, unvisitedChildren)) 

		else:
			dfsStack.pop()

	return bestProb, bestSentence

def generate(startingWord, sentenceSpec, graph):
	wordGraph = parse(graph) 

	bfsProb, bfsSentence = breadthFirstSearch(startingWord, sentenceSpec, wordGraph)
	# print "Breadth First\n------------------------------------"
	# print '"' + sentence + '" is the highest probability sentence (' + str(prob*100) + '%).'


	dfsProb, dfsSentence = depthFirstSearch(startingWord, sentenceSpec, wordGraph)
	# print "Depth First\n------------------------------------"
	# print '"' + sentence + '" is the highest probability sentence (' + str(prob*100) + '%).'

	return bfsProb, bfsSentence, dfsProb, dfsSentence

open_file = open('input.txt', 'r')
graph = open_file.read()

bfsProb, bfsSentence, dfsProb, dfsSentence = generate('a', ['DT', 'NN', 'VBD', 'NNP', 'IN', 'DT', 'NN'], graph)

print "Breadth First:\n"
print '"' + bfsSentence + '" is one of the highest probability sentences (' + str(bfsProb*100) + '%).'

print ''

print "Depth First:\n"
print '"' + dfsSentence + '" is one of the highest probability sentences (' + str(dfsProb*100) + '%).'

# running some git tests
# bfs: a queen answered hans up the apple