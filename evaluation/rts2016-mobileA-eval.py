#!/usr/bin/python

# This is the evaluation script for the TREC 2016 RTS evaluation
# (scenario A) with mobile assessor judgments, v1.0.

__author__ = 'Luchen Tan'
import sys
import argparse


evaluation_starts = 1470096000
evaluation_ends = 1470960000
seconds_perday = 86400
K = 10

parser = argparse.ArgumentParser(description='Evaluation script for TREC 2016 RTS scenario A with mobile assessor judgments')
parser.add_argument('-q', required=True, metavar='qrels', help='qrels file')
parser.add_argument('-r', required=True, metavar='run', help='run file')

args = parser.parse_args()
file_qrels_path = vars(args)['q']
run_path = vars(args)['r']

qrels_dt = {}
for i, line in enumerate(open(file_qrels_path)):
    line = line.strip().split()
    topic = line[0]
    tweetid = line[1]
    judgement = int(line[3])
    if topic not in qrels_dt:
        qrels_dt[topic] = {'rel': [], 'redundant': [], 'non_rel': [], 'all_judged': []}
    if judgement == 2:
        if tweetid not in qrels_dt[topic]['rel']:
            qrels_dt[topic]['rel'].append(tweetid)
    elif judgement == 1:
        if tweetid not in qrels_dt[topic]['redundant']:
            qrels_dt[topic]['redundant'].append(tweetid)
    else:
        if tweetid not in qrels_dt[topic]['non_rel']:
            qrels_dt[topic]['non_rel'].append(tweetid)
    if tweetid not in qrels_dt[topic]['all_judged']:
        qrels_dt[topic]['all_judged'].append(tweetid)

run_dt = {}
runname = ''
for i, line in enumerate(open(run_path)):
    line = line.strip().split()
    topic = line[0]
    tweetid = line[1]
    push_time = int(line[2])
    runname = line[3]
    if topic in qrels_dt:
        day = (push_time - evaluation_starts) / seconds_perday
        #print day
        if 0 <= day < 10:
            if topic in run_dt:
                if day in run_dt[topic]:
                    run_dt[topic][day].append(tweetid)
                else:
                    run_dt[topic][day] = [tweetid]
            else:
                run_dt[topic] = {day: [tweetid]}
        else:
            print line


print " ".join(["run", "topic", "#rel", "#redundant", "#non_rel", "#unjudged", "#total_length"])
total_rel, total_redundant, total_non_rel, total_unjudged, total_length = 0, 0, 0, 0, 0
for topic in sorted(qrels_dt.keys()):
    rel, redundant, non_rel, unjudged, length = 0, 0, 0, 0, 0
    if topic in run_dt:
        pushes = run_dt[topic]
        for day in run_dt[topic]:
            length += len(run_dt[topic][day])
            tweets_counted = run_dt[topic][day][:K]
            for tweetid in tweets_counted:
                if tweetid in qrels_dt[topic]['rel']:
                    rel += 1
                if tweetid in qrels_dt[topic]['redundant']:
                    redundant += 1
                if tweetid in qrels_dt[topic]['non_rel']:
                    non_rel += 1
                if tweetid not in qrels_dt[topic]['all_judged']:
                    unjudged += 1
            unjudged += max(0, len(run_dt[topic][day]) - K)

    print " ".join([runname, topic, str(rel), str(redundant), str(non_rel), str(unjudged), str(length)])
    total_rel += rel
    total_redundant += redundant
    total_non_rel += non_rel
    total_unjudged += unjudged
    total_length += length

print " ".join([runname, "All", str(total_rel), str(total_redundant), str(total_non_rel), str(total_unjudged), str(total_length)])