eval_hw4.py is the evaluation code, the input format is also in it.

qrels.txt is generated from qrels2014.txt, the groundtruth.  qrels.txt removes the ids not in tweets.txt, the TREC2014 dataset downloaded from the group. The deleting process is in process.py .

result.txt is just used for test the code can run normally. As for correctness, I'm not sure. process.py is its generated procedure.

input format, result.txt format

query_id doc_id
query_id doc_id
query_id doc_id
query_id doc_id
query_id doc_id
query_id doc_id
...