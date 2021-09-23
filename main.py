from functions import *
from calculate_optimal_ask import *
import json
from tqdm import tqdm
import time
from datetime import datetime
from multiprocessing import Process, Queue

def create_next_calc_list(res):
    ret = []
    for key in res.keys():
        if key == "HB":
            continue
        if res[key]["score"] == 0:
            continue
        if len([key_ for key_ in res.keys() if key in key_]) > 1:
            continue
        ret += [key+"{}{}".format(h,b) for (h,b) in all_HB]
    return ret

def cnv_str2list(str_num):
    return list(map(lambda x:int(x), str_num))


if __name__ == "__main__":
    with open("result3.json", "r") as f:
        pre_res = json.loads(f.read())

    if len(pre_res.keys()) == 1:
        first = cnv_str2list(pre_res["HB"]["value"])
        all_result = {}
        dx = calc_distribution(first)
        process_list = []
        resQueue = Queue()
        for i in range(len(all_HB)):
            (h,b) = all_HB[i]
            process_list.append(Process(target=step, args=(dx[i], all_numbers, resQueue, "{}{}".format(h,b))))

        for p in process_list:
            p.start()
            p.join()

        while (not resQueue.empty()):
            ans, score, name = resQueue.get()
            pre_res.update({"HB"+name:{"value":"".join(list(map(str, ans))), "score":score}})
            print("HB{}: {}, {}".format(name, ans, score))

    next_branch_list = create_next_calc_list(pre_res)
    print(next_branch_list)

    while len(next_branch_list)!=0:
        for key in next_branch_list:
            nums = [(cnv_str2list(pre_res[key[:2+2*i]]["value"]), int(key[2+2*i]), int(key[2*i + 3])) for i in range(len(key)//2 - 1)]
            d = intersect_all([calcHBX(x, h, b) for (x, h, b) in nums])
            if len(d)==0:
                continue
            process_list = []
            resQueue = Queue()
            for i in range(len(all_HB)):
                (h,b) = all_HB[i]
                process_list.append(Process(target=step, args=(d, all_numbers, resQueue, "{}{}".format(h,b))))

            for p in process_list:
                p.start()
                p.join()

            max_score = 0
            opt_ans = []
            while (not resQueue.empty()):
                ans, score, name = resQueue.get()
                if max_score <= score:
                    max_score = score
                    opt_ans = ans
                    pre_res.update({key:{"value":"".join(list(map(str, ans))), "score":score}})

            print("{}: {}, {}".format(key, opt_ans, max_score))
        next_branch_list = create_next_calc_list(pre_res)

    with open("result3.json", "w") as f:
        f.write(json.dumps(pre_res))
