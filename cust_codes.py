from flask import Flask
import pandas as pd
from collections import defaultdict


app = Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = ('')
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

userFilePath = ''
panels = pd.read_csv("")
countsDictionary = panels.count()
user_list = []

def compareGenes(lst):
	matchCounts = {}
	matchNames = defaultdict(list)
	for pan in panels.columns.values:
		matchCounts[pan] = 0
		matchNames[pan] = []
		for x in panels[pan]:
			for i in lst:
				if i == x:
					matchCounts[pan] += 1
					matchNames[pan].append(i)
	return {'matchCounts':matchCounts,'matchNames':matchNames}

def findBestMatches(matchDict):
	percents = defaultdict(float)
	for key, value in countsDictionary.items():
		percents[key] = float(matchDict[key]) / float(value)
	topName = max(percents, key=percents.get)
	topMatchPercent = percents[topName]
	return {'topName':topName, 'topMatchPercent':topMatchPercent}

def haves(geneDict, topMatchName):
	return geneDict[topMatchName]

def haveNots(topMatchName, fil):
	x = panels[topMatchName].tolist()
	notInPanel = list(set(fil) - set(x))
	return notInPanel

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
