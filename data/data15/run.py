import os

for rel_thr in [0.75, 0.76, 0.77, 0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85]:
    for red_thr in [0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80]:   
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/jm_%.2f_%.2f.dat" % (rel_thr, red_thr)
        os.system(order)

for rel_thr in [0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80]:
    for red_thr in [0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69, 0.70]:
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/dir_%.2f_%.2f.dat" % (rel_thr, red_thr)
        os.system(order)
                


