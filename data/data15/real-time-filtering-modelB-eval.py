#This file is to take run file (as an input argument) and ground truth non-redundant tweets, judgment pools
#to compute ndcg@k score.
import sys
import math
import json
from sets import Set
import argparse

parser = argparse.ArgumentParser(description='Real-Time Filtering evaluation script - Scenario B (version 1.0)')
parser.add_argument('-q', required=True, metavar='qrels', help='qrels file')
parser.add_argument('-c', required=True, metavar='clusters', help='cluster anotations')
parser.add_argument('-r', required=True, metavar='run', help='run file')

args = parser.parse_args()
file_qrels_path = vars(args)['q']
clusters_path = vars(args)['c']
run_path = vars(args)['r']

K = 10
days = []
for i in range(20, 30):
	days.append("201507%s" % i)

#Take qrels to generate dictionary of {topic number:{tweetid:gain}} 
#where gain is 0(spam/junk, not interesting), 0.5(somewhat interesting), 1(very interesting)
qrels_dt = {}
clusters_day_dt = {}
file_qrels = open(file_qrels_path, "r")
lines = file_qrels.readlines()
for line in lines:
    line = line.strip().split()
    topic_ind = line[0]
    tweetid = line[2]
    score = int(line[3])
    if score == -1:
    	score = 0
    else:
    	if score == 3:
    		score = 1
    	else:
    		if score == 4:
    			score = 2
    if topic_ind not in qrels_dt:
    	qrels_dt[topic_ind] = {}
    	clusters_day_dt[topic_ind] = {}
    	for day in days:
			clusters_day_dt[topic_ind][day] = []
    qrels_dt[topic_ind][tweetid] = score * 1.0 / 2
file_qrels.close()

#Take tweet2dayepoch.txt (tweets from judgment pool) and store the mapping data in dictionary of {tweetid:day}
tweet2day_dt = {}
file_tweet2day = open("tweet2dayepoch.txt", "r")
lines = file_tweet2day.readlines()
for line in lines:
	line = line.strip().split()
	tweet2day_dt[line[0]] = line[1]
file_tweet2day.close()

#Take clustering protocol file and generate dictionary of {topic number:{day:[tweets]}} and dictionary of {topic number:{day:{tweet:clusterid}}}
clusters_clusterid_dt = {}
file_clusters = open(clusters_path, "r")
data = json.load(file_clusters)
topics = data["topics"]
clusterid = 1
for topic in sorted(topics.keys()):
	topic_ind = topic[topic.index("MB") + 2:]
	topic_ind = topic_ind.encode("utf-8")
	if topic_ind not in clusters_clusterid_dt:
		clusters_clusterid_dt[topic_ind] = {}
	clusters_json = topics[topic]["clusters"]
	for i in range(len(clusters_json)):
		clusters_json[i] = [s.encode("utf-8") for s in clusters_json[i]]
	for cluster in clusters_json:
		for tweetid in cluster:
			clusters_day_dt[topic_ind][tweet2day_dt[tweetid]].append(tweetid)
			clusters_clusterid_dt[topic_ind][tweetid] = clusterid
		clusterid = clusterid + 1
file_clusters.close()

#Take input run and generate dictionary of {topic number:{day:[tweetids]}}
runname = ''
run_dt = {}
file_run = open(run_path, "r")
lines = file_run.readlines()
for line in lines:
	line = line.strip().split()
	runname = line[6]
	topic_ind = line[1][line[1].index("MB") + 2:]
	#Only consider the 51 topics selected by NIST
	if topic_ind in qrels_dt:
		if topic_ind not in run_dt:
			run_dt[topic_ind] = {}
		day = line[0]
		if day not in run_dt[topic_ind]:
			run_dt[topic_ind][day] = []
		tweetid = line[3]
		run_dt[topic_ind][day].append(tweetid)
file_run.close()

# print "runtag".ljust(len(runname)) + "\ttopic\tnDCG"
#Compute ndcg
total_score = 0.0
for topic_ind in sorted(qrels_dt):
	topic_score = 0.0
	exist_clusterids = Set()
	for day in days:
		interesting = False
		max_gain_dt = {}
		tweets_fromprotocol = clusters_day_dt[topic_ind][day]
		for tweetid in tweets_fromprotocol:
			clusterid = clusters_clusterid_dt[topic_ind][tweetid]
			if clusterid not in exist_clusterids:
				interesting = True
				if clusterid not in max_gain_dt:
					max_gain_dt[clusterid] = qrels_dt[topic_ind][tweetid]
				else:
					max_gain_dt[clusterid] = max(max_gain_dt[clusterid], qrels_dt[topic_ind][tweetid])
		if interesting:
			if topic_ind in run_dt and day in run_dt[topic_ind]:
				ndcg = 0
				gains = []
				for tweetid in run_dt[topic_ind][day]:
					gain = 0
					if tweetid in clusters_day_dt[topic_ind][day]:
						clusterid = clusters_clusterid_dt[topic_ind][tweetid]
						if clusterid not in exist_clusterids:
							exist_clusterids.add(clusterid)
							gain = qrels_dt[topic_ind][tweetid]
							if clusterid in max_gain_dt:
								gain = max_gain_dt[clusterid]
					gains.append(gain)
				rank_cut = min(len(gains), K)
				dcg = 0.0
				for i in range(rank_cut):
					gain = gains[i]
					dcg = dcg + (pow(2, gain) - 1) * 1.0 / math.log(i + 2, 2)
				#Compute idcg
				top_gains = max_gain_dt.values()
				top_gains.sort(reverse = True)
				rank_cut = min(len(top_gains), K)
				idcg = 0.0
				top_gains = top_gains[:rank_cut]
				for i in range(rank_cut):
					gain = top_gains[i]		
					idcg = idcg + (pow(2, gain) - 1) * 1.0 / math.log(i + 2, 2)
				if idcg != 0:
					ndcg = dcg / idcg
				topic_score = topic_score + ndcg
		else:
			if topic_ind not in run_dt or day not in run_dt[topic_ind]:
				topic_score = topic_score + 1
	topic_score = topic_score / len(days)
	# print "%s\tMB%s\t%.04f" % (runname, topic_ind, topic_score)
	total_score = total_score + topic_score
total_score = total_score / len(qrels_dt)
print "%s\t%.04f" % (runname, total_score)