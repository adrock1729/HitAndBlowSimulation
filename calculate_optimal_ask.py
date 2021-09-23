from functions import *
from multiprocessing import Process, Queue, Lock
from tqdm import tqdm
import time

def calc_distribution_step(numbers, number):
    ret = []
    for (h, b) in all_HB:
        ret.append([x for x in numbers if calcHB(x, number)==(h, b)])
    return ret

def calc_step(d, y):
    dy = calc_distribution_step(d, y)
    return entropy(dy)

def get_optimal_ans(candidates, numbers, name):
    if (len(candidates) == 0):
        return None, 0, name
    elif (len(candidates) == 1):
        return candidates[0], 0, name

    part_length = (len(numbers)//500) + 1
    process_holder = []
    position = 0
    ans = Queue()
    for i in range(part_length):
        if i < part_length - 1:
            partition = numbers[i*500:(i+1)*500]
        else:
            partition = numbers[i*500:]
        def func(partition, position, queue, disc):
            optimal_ans_part = None
            score_part = 0
            prefix = name+"/"+str(position)
            # for number in tqdm(partition, position=position, desc=prefix):
            for number in partition:
                ent = calc_step(candidates, number)
                if (ent > score_part):
                    optimal_ans_part = number
                    score_part = ent
            queue.put((optimal_ans_part, score_part))

        process_holder.append(Process(target=func, args=(partition, position, ans, name)))
        position += 1

    for p in process_holder:
        p.start()
        time.sleep(5 * (len(candidates)/len(all_numbers)))

    for p in process_holder:
        p.join()

    opt_ans = None
    score = 0
    while (not ans.empty()):
        ans_part, score_part = ans.get()
        if (score < score_part):
            score = score_part
            opt_ans = ans_part

    return opt_ans, score, name

def step(cand, nums, resQueue, hb):
    resQueue.put(get_optimal_ans(cand, nums, hb))


if __name__ == "__main__":
    first = all_numbers[0]
    all_result = {}
    dx = calc_distribution(first)
    process_list = []
    resQueue = Queue()
    for i in range(len(all_HB)):
        (h,b) = all_HB[i]
        process_list.append(Process(target=step, args=(dx[i], all_numbers, resQueue, "HB{}{}".format(h,b))))

    for p in process_list:
        p.start()
        p.join()

    with open("score.txt", "w") as f:
        res = ""
        while (not resQueue.empty()):
            ans, score, name = resQueue.get()
            res += "{}:{},{}\n".format(name, ans, score)
        f.write(res)
