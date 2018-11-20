import json

def read_json_file(file_name):
    #input tweet.txt
    #output tweet_id_set
    with open(file_name, 'r', errors='ignore') as f:
         tweet_id_set = set()
         for line in f:
            json_obj = json.loads(line.strip())
            tweetid = json_obj['tweetId']
            tweet_id_set.add(tweetid)
    return tweet_id_set

def filer_qrels_file(file_name, out_file_name, tweet_id_set):
    with open(out_file_name, 'w', encoding='utf-8') as f_out:
        with open(file_name, 'r', errors='ignore') as f_in:
            for line in f_in:
                ele = line.strip().split(' ')
                if ele[2] in tweet_id_set:
                    f_out.write(line)

def query_result_simulation(file_name, out_file_name, tweet_id_set):
    with open(out_file_name, 'w', encoding='utf-8') as f_out:
        with open(file_name, 'r', errors='ignore') as f_in:
            for line in f_in:
                ele = line.strip().split(' ')
                # if ele[2] in tweet_id_set and int(ele[3]) > 0:
                if ele[2] in tweet_id_set:
                    f_out.write(' '.join([ele[0], ele[2]]) + '\n')



def filter_out_of_set():
    id_file = 'tweets.txt'
    in_file = 'qrels2014.txt'
    out_file = 'qrels.txt'
    sim_file = 'result.txt'
    tweet_id_set = read_json_file(id_file)
    # remove unrelated ids
    # filer_qrels_file(in_file, out_file, tweet_id_set)
    # generate simulate test_set
    query_result_simulation(in_file, sim_file, tweet_id_set)

if __name__ == '__main__':
    filter_out_of_set()