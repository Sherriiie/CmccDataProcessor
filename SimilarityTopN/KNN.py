import math
# return list [intent_id, score]
class knn:
    @staticmethod
    def GetTopK(candidates=[('A', 0.91),('B', 0.90), ('B', 0.89), ('B', 0.88), ('B', 0.87), ('C', 0.92)], knnTopK=10, knnThreshold=0.5, certaintyScore=1.0, enableKnnLogDecay=True):
        '''
        rank the input category by its score with KNN algorithm.
        :param candidates:
            schema: list of tuples[('category_id', score)]
        :param knnTopK: knnTopK candidates will be selected at most.
        :param knnThreshold: the confidence score of all candidates should be over knnThreshold.
        :param enableKnnLogDecay: if enable score decay with the re-occurrence order.
        :return: res intent category with score in list of tuple as input format.
        '''

        if len(candidates) == 0:
            return []
        # get TopK valid candidates
        candidates = sorted(candidates, key=lambda c:c[1], reverse=True)[:knnTopK]      # descending order
        # threshold filter
        if len(candidates)>0 and candidates[0][1]>knnThreshold:
            candidates = [cand for cand in candidates if cand[1] > knnThreshold]

        # category_id with max score
        temp_id = []
        temp_cand = {}
        for cand in candidates:
            if cand[0] not in temp_id:
                temp_cand[cand[0]] = cand[1]
                temp_id.append(cand[0])
            else:
                if cand[1] > temp_cand[cand[0]]:
                    temp_cand[cand[0]] = cand[1]
        id_maxscore = temp_cand

        # whether there is any answer with enough confidence
        if candidates[0][1] > certaintyScore:
            return [(k,v) for k,v in id_maxscore.items()]

        # id_weightedsum
        temp_id = []
        temp_cand = {}
        for (cand, i) in zip(candidates, range(len(candidates))):
            val = cand[1] / math.log(i + 2, 2) if enableKnnLogDecay else cand[1]
            if cand[0] not in temp_id:
                temp_cand[cand[0]] = val
                temp_id.append(cand[0])
            else:
                temp_cand[cand[0]] += val
        id_weightedsum = temp_cand

        res = []
        scores = [_[1] for _ in (sorted(id_maxscore.items(), key=lambda k:k[1], reverse=True))]
        for (k, i) in zip(sorted(id_weightedsum.items(), key=lambda w:w[1], reverse=True), range(len(id_weightedsum))):
            res.append((k[0], scores[i]))
        return res

if __name__ == '__main__':
    res = knn.GetTopK([('2', 0.7758925917179603), ('0', 0.6874765056185168), ('0', 0.6644089036758635), ('5', 0.6611151983156341), ('5', 0.6582541939097556)])
    print(res)
