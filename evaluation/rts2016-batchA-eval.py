#!/usr/bin/python

# This is the evaluation script for the TREC 2016 RTS evaluation
# (scenario A) with batch NIST assessor judgments, v1.0.

__author__ = 'Luchen'
import argparse
import json
import numpy

parser = argparse.ArgumentParser(description='Evaluation script for TREC 2016 RTS scenario A with batch NIST assessor judgments')
parser.add_argument('-q', required=True, metavar='qrels', help='batch qrels file')
parser.add_argument('-c', required=True, metavar='clusters', help='cluster anotations')
parser.add_argument('-t', required=True, metavar='tweetsdayepoch', help='tweets2dayepoch file')
parser.add_argument('-r', required=True, metavar='run', help='run file')

args = parser.parse_args()
qrels_path = vars(args)['q']
clusters_path = vars(args)['c']
file_tweet2day = vars(args)['t']
run_path = vars(args)['r']

K = 10

# We discovered that, from the RTS evaluation broker's perspective,
# some tweets were pushed before they were actually posted on
# Twitter. Since it is unlikely that participants had created time
# traveling devices, we attributed the issue to clock skew on the
# broker. Note that since the broker was an EC2 instance, there is no
# way to debug post hoc. The only reasonable solution we could come up
# with was to add a temporal offset to *all* pushed tweets. We set
# this offset to 139 seconds, the maximum gap between a system push
# time and the created time of the tweet.
#
# NOTE: This effectively sets an upper bound on the temporal
# resolution when interpreting system latencies.
time_travel = 139  # time travel in seconds
days = []
for i in range(2, 12):
    days.append("201608%02d" % i)

# qrels dictionary, {topic: {tweetid: gain}}
qrels_dt = {}
clusters_day_dt = {}
for line in open(qrels_path).readlines():
    line = line.strip().split()
    topic = line[0]
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
    if topic in qrels_dt:
        qrels_dt[topic][tweetid] = score / float(2)
    else:
        qrels_dt[topic] = {tweetid: score / float(2)}
        clusters_day_dt[topic] = {day: [] for day in days}


# created timestamp and date for each tweetid in the qrel
# tweet2day_dt: {tweetid: date}
# tweet2epoch_dt: {tweetid: epoch time}
tweet2day_dt = {}
tweet2epoch_dt = {}
for line in open(file_tweet2day).readlines():
    line = line.strip().split()
    tweet2day_dt[line[0]] = line[1]
    tweet2epoch_dt[line[0]] = line[2]


# cluster dictionaries
# clusters_clusterid_dt: {topic: {tweetid: clusterid}}
# clusters_day_dt: {topic: {date: [tweetids]}}
clusters_clusterid_dt = {}
clusters_topic_dt = json.load(open(clusters_path))["topics"]
for topic in sorted(clusters_topic_dt.keys()):
    clusters_json = clusters_topic_dt[topic]["clusters"]
    if topic not in clusters_clusterid_dt:
        clusters_clusterid_dt[topic] = {}
    for clusterid in clusters_json.keys():
        for tweetid in clusters_json[clusterid]:
            clusters_clusterid_dt[topic][tweetid] = clusterid
            if tweet2day_dt[tweetid] != '20160801':
                clusters_day_dt[topic][tweet2day_dt[tweetid]].append(tweetid)


# run dictionaries
# run_dt: {topic: {date: [tweetids}}
# run_epoch_dt: {topic: {tweetid: adjusted epoch time}}
runname = ''
run_dt = {}
run_epoch_dt = {}
for line in open(run_path).readlines():
    line = line.strip().split()
    runname = line[3]
    topic = line[0]
    if topic in qrels_dt:
        tweetid = line[1]
        # The epoch time of run push is adjusted by the clock offset
        epoch = long(float(line[2])) + long(float(time_travel))
        if topic not in run_dt:
            run_dt[topic] = {}
            run_epoch_dt[topic] = {}
        if tweetid in tweet2day_dt:
            if epoch >= long(tweet2epoch_dt[tweetid]):
                day = tweet2day_dt[tweetid]
                if day in run_dt[topic]:
                    run_dt[topic][day].append(tweetid)
                else:
                    run_dt[topic][day] = [tweetid]
                run_epoch_dt[topic][tweetid] = epoch
           

print "{0}\t{1:5s}\t{2:6s}\t{3:6s}\t{4:6s}\t{5:6s}\t{6:10s}\t{7:10s}\t{8:10s}\t{9:15s}\t{10:15s}".format(
    "runtag".ljust(len(runname)), "topic",
    "EG1", "EG0", "nCG1", "nCG0",
    "GMP.33", "GMP.5", "GMP.66",
    "mean latency", "median latency")

total_eg1, total_eg0, total_ncg1, total_ncg0, total_gmp_33, total_gmp_50, total_gmp_66 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
latency_gained = []
for topic in sorted(qrels_dt):
    topic_eg1, topic_eg0, topic_ncg1, topic_ncg0, topic_gmp_33, topic_gmp_50, topic_gmp_66 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    exist_clusterids = set()
    for day in days:
        interesting = False
        max_gain_dt = {}
        tweets_fromprotocol = clusters_day_dt[topic][day]
        for tweetid in tweets_fromprotocol:
            clusterid = clusters_clusterid_dt[topic][tweetid]
            if clusterid not in exist_clusterids:
                interesting = True
                if clusterid not in max_gain_dt:
                    max_gain_dt[clusterid] = qrels_dt[topic][tweetid]
                else:
                    max_gain_dt[clusterid] = max(max_gain_dt[clusterid], qrels_dt[topic][tweetid])
        if interesting:
            if topic in run_dt and day in run_dt[topic]:
                eg, ncg = 0.0, 0.0
                gmp_33, gmp_50, gmp_66 = 0.0, 0.0, 0.0
                gains = []
                pain_count = 0
                for tweetid in run_dt[topic][day]:
                    gain, delay = 0.0, 0.0
                    if tweetid in clusters_day_dt[topic][day]:
                        clusterid = clusters_clusterid_dt[topic][tweetid]
                        if clusterid not in exist_clusterids:
                            exist_clusterids.add(clusterid)
                            gain = qrels_dt[topic][tweetid]
                            # tweet gain is with respect to its own gain, not max gain in the cluster
                            # if clusterid in max_gain_dt:
                            #    gain = max_gain_dt[clusterid]
                            # latency of each tweet is with respect to the first tweet in the cluster
                            first_tweetid_in_cluster = clusters_topic_dt[topic]["clusters"][clusterid][0]
                            delay = (
                                long(float(run_epoch_dt[topic][tweetid])) - long(tweet2epoch_dt[first_tweetid_in_cluster]))
                            delay = max(0, delay)
                    gains.append(gain)
                    if gain > 0:
                        latency_gained.append(delay)
                    else:
                        pain_count += 1

                eg = sum(gains[:min(len(gains), K)]) / len(run_dt[topic][day])
                max_gains = max_gain_dt.values()
                max_gains.sort(reverse=True)
                max_gain = sum(max_gains[:min(len(max_gains), K)])
                ncg = sum(gains[:min(len(gains), K)]) / max_gain

                gmp_33 = 0.33 * sum(gains[:min(len(gains), K)]) - (1 - 0.33) * pain_count
                gmp_50 = 0.5 * sum(gains[:min(len(gains), K)]) - 0.5 * pain_count
                gmp_66 = 0.66 * sum(gains[:min(len(gains), K)]) - (1 - 0.66) * pain_count
                topic_eg1 += eg
                topic_eg0 += eg
                topic_ncg1 += ncg
                topic_ncg0 += ncg
                topic_gmp_33 += gmp_33
                topic_gmp_50 += gmp_50
                topic_gmp_66 += gmp_66
        else:
            if topic not in run_dt or day not in run_dt[topic]:
                topic_eg1 += 1
                topic_ncg1 += 1

            elif topic in run_dt and day in run_dt[topic]:
                gmp_33 = - (1 - 0.33) * len(run_dt[topic][day])
                gmp_50 = - (1 - 0.5) * len(run_dt[topic][day])
                gmp_66 = - (1 - 0.66) * len(run_dt[topic][day])
    topic_eg1 /= len(days)
    topic_eg0 /= len(days)
    topic_ncg1 /= len(days)
    topic_ncg0 /= len(days)
    topic_gmp_33 /= len(days)
    topic_gmp_50 /= len(days)
    topic_gmp_66 /= len(days)
    print "{0}\t{1:5s}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:<10.4f}\t{7:<10.4f}\t{8:<10.4f}".format(
        runname, topic, topic_eg1, topic_eg0, topic_ncg1, topic_ncg0,
        topic_gmp_33, topic_gmp_50, topic_gmp_66)
    total_eg1 += topic_eg1
    total_eg0 += topic_eg0
    total_ncg1 += topic_ncg1
    total_ncg0 += topic_ncg0
    total_gmp_33 += topic_gmp_33
    total_gmp_50 += topic_gmp_50
    total_gmp_66 += topic_gmp_66
total_eg1 /= len(qrels_dt)
total_eg0 /= len(qrels_dt)
total_ncg1 /= len(qrels_dt)
total_ncg0 /= len(qrels_dt)
total_gmp_33 /= len(qrels_dt)
total_gmp_50 /= len(qrels_dt)
total_gmp_66 /= len(qrels_dt)

print "{0}\t{1:5s}\t{2:.4f}\t{3:.4f}\t{4:.4f}\t{5:.4f}\t{6:<10.4f}\t{7:<10.4f}\t{8:<10.4f}\t{9:<15.1f}\t{10:<15.1f}".format(
        runname, "All", total_eg1, total_eg0, total_ncg1, total_ncg0,
        total_gmp_33, total_gmp_50, total_gmp_66,
        numpy.mean(latency_gained) if latency_gained != [] else 0, numpy.median(latency_gained) if latency_gained != [] else 0)
