# A任务评价
## mobile
python rts2016-mobileA-eval.py -q rts2016-mobileA-qrels.txt -r PKUICSTRunA1
python rts2016-mobileA-eval.py -q rts2016-mobileA-qrels.txt -r PKUICSTRunA2
python rts2016-mobileA-eval.py -q rts2016-mobileA-qrels.txt -r PKUICSTRunA3

## batch
python rts2016-batchA-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunA1
python rts2016-batchA-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunA2
python rts2016-batchA-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunA3

# B任务评价
## batch
python rts2016-batchB-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunB1
python rts2016-batchB-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunB2
python rts2016-batchB-eval.py -q rts2016-qrels.txt -c rts2016-batch-clusters.json -t rts2016-batch-tweets2dayepoch.txt -r PKUICSTRunB3
