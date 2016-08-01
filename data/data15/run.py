import os

'''
for rel_thr in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85]:
    for red_thr in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85]:
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_jm_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_dir_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_cos_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #os.system(order)
        
'''        
'''
for rel_thr in [0.75, 0.76, 0.77, 0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89, 0.90]:
    for red_thr in [0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79, 0.80]:
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_jm_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #os.system(order)

'''
'''
for rel_thr in [0.67, 0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78]:
    for red_thr in [0.65, 0.66, 0.67, 0.68, 0.69, 0.70, 0.71, 0.72, 0.73, 0.74, 0.75]:
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_dir_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #os.system(order)
'''
for rel_thr in [0.9, 0.95]:
    for red_thr in [0.3, 0.4, 0.5, 0.60, 0.70]:
        print "%.2f\t%.2f" % (rel_thr, red_thr)
        #order = "python real-time-filtering-modelA-eval.py -q qrels.txt -c clusters-2015.json.txt -r ../../src/test/tmp/test_a_cos_%.2f_%.2f.dat" % (rel_thr, red_thr)
        #os.system(order)
        

