import numpy as np
from argparse import ArgumentParser
import json


class CalSimilarity:
    def __init__(self, candidates_path, candidates_path_with_index='training_withindex.txt'):
        self.candidates_path = candidates_path
        self.candidates = []
        self.text_index = {}
        self.intent_index = {}
        self.vector_index = {}
        self.read_candidates()
        self.candidates_path_with_index = candidates_path_with_index
        return

    def cal_cosine(self, vec1, vec2):
        #  vector has been normalized
        # vec1_len = np.sqrt(np.dot(vec1, vec1))
        # vec2_len = np.sqrt(np.dot(vec2, vec2))
        # print('vector length', vec1_len, vec2_len)
        cosine = np.dot(vec1, vec2)
        return cosine

    def read_candidates(self):
        with open(self.candidates_path, encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                parts = line.strip().split('\t')
                parts[2] = np.array(parts[2].split(' '), dtype=float)
                self.candidates.append(parts)
                self.intent_index[parts[0]] = parts[1]
                self.vector_index[parts[0]] = parts[2]
            print("Read all candidates done. ")

    def read_candidates_text_index(self, path_read):
        print('Begin read_candidates_with_index')
        with open(path_read, encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                parts = line.strip().split('\t')
                self.text_index[parts[0]] = parts[2]
            print("Read all candidates for text index done. ")

    def get_topN(self, vec, topN=1):
        cosines = []
        for index in range(len(self.candidates)):
            cand_vec = self.candidates[index][2]
            cos = self.cal_cosine(cand_vec, vec)
            if len(self.candidates[index]) < 4:
                self.candidates[index].append(cos)  # schema of every candidate: index, intent_id, vector, cos
            else:
                self.candidates[index][3] = cos
            cosines.append(cos)
        index_top = self.get_top_index(cosines, topN)
        candidates_top = []
        for index in index_top:
            candidates_top.append(self.candidates[index])
        return candidates_top

    def get_top_index(self, cosines_in, N):
        cosines = cosines_in.copy()
        sorted_index = np.argsort(cosines)
        index = [sorted_index[-i - 1] for i in range(N)]
        # for i in index:
        #     print(cosines[i])
        return index

    def evaluate(self, topN=5):
        file_path = 'evaluation.vector.txt'
        new_lines = []
        new_lines_index = []
        index = 0
        file_write = open('prediction_scores.txt', encoding='utf-8', mode='w')
        file_write_index = open('prediction_scores_index.txt', encoding='utf-8', mode='w')
        with open(file_path, encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                index += 1
                print('==== Line %d' % (index))
                id_scores = []
                id_scores_index = []
                parts = line.strip().split('\t')
                parts[1] = np.array(parts[1].split(' '), dtype=float)
                candidates_top = self.get_topN(parts[1],
                                               topN)  # schema of every candidate: index, intent_id, vector, cos
                for cand in candidates_top:
                    id_scores.append(cand[1] + ' ' + '%.4f' % cand[3])
                    id_scores_index.append(cand[1] + ' ' + '%.4f' % cand[3] + ' ' + cand[0])
                new_lines.append('\t'.join(id_scores))
                new_lines_index.append('\t'.join(id_scores_index))
            file_write.write('\n'.join(new_lines))
            file_write_index.write('\n'.join(new_lines_index))
        print("Evaluation of score calculating finished")


    def conclude_precision(self, prediciton_path_raw='prediction_scores_index.txt', prediciton_path_ranked='ranker_results.txt', answer_path='evaluation.txt'):
        self.candidates_path_with_index = 'training_withindex.txt'
        self.read_candidates_text_index(self.candidates_path_with_index)
        file_predict_raw = open(prediciton_path_raw, encoding='utf-8', mode='r')
        file_predict_ranked = open(prediciton_path_ranked, encoding='utf-8', mode='r')
        file_answer = open(answer_path, encoding='utf-8', mode='r')
        lines_prediction_ranked = file_predict_ranked.readlines()
        lines_prediction_raw = file_predict_raw.readlines()
        lines_answer = file_answer.readlines()
        # log_writer = open('evaluation_log.txt', encoding='utf-8', mode='w')
        log_dict = {}
        correct_number = 0
        for i in range(len(lines_answer)):
            value = {}
            value['prediction_ranked'] = lines_prediction_ranked[i].strip()
            value['prediction_raw_index'] = lines_prediction_raw[i].strip()
            def get_text_with_index(input1):
                output1 = dict()
                for index in input1:
                    output1[index] = self.text_index[index]
                return output1
            index_temp = [var.split(' ')[-1] for var in lines_prediction_raw[i].strip().split('\t')]
            value['prediction_raw_index_text'] = get_text_with_index(index_temp)
            answer = lines_answer[i].strip().split('\t')[-1]
            prediction = lines_prediction_ranked[i].strip().split('\t')[1]
            if answer == prediction:
                correct_number += 1
                value['prediction_flag'] = True
            else:
                print(answer + '\t' + prediction)
                value['prediction_flag'] = False
            log_dict[lines_answer[i].strip()] = value


        with open('evaluation_log.json', encoding='utf-8', mode='w') as outfile:
            json.dump(log_dict, outfile, indent=2, ensure_ascii=False)
        print('Evaluation log has been written into json file evaluation_log.json')
        precison = correct_number * 1.0 / len(lines_answer)
        print("correct_number=%d, precision=%0.4f" % (correct_number, precison))

    def get_raw_trigger_queries(self):
        # get top 10 closest neighbour for every training vector.
        topN = 10
        new_lines = []
        path_read = self.candidates_path
        file_write = open('prediction_index_scores.4narrow.txt', encoding='utf-8', mode='w')
        with open(path_read, encoding='utf-8', mode='r') as file_reader:
            index = 0
            for line in file_reader:
                index += 1
                if (index % 100 == 0):
                    print('==== Line %d' % (index))
                index_intent_scores = []
                parts = line.strip().split('\t')
                parts[2] = np.array(parts[2].split(' '), dtype=float)
                candidates_top = self.get_topN(parts[2], topN)
                for cand in candidates_top:
                    index_intent_scores.append(cand[0] + ' ' + cand[1] + ' ' + '%.4f' % cand[3])
                new_lines.append('\t'.join(index_intent_scores))
            file_write.write('\n'.join(new_lines))
        print("Method narrow_trigger_queries() finished")

    def exe_narrow_trigger_queries(self, path_read, gap=0.1):
        print('In exe_narrow_trigger_queries()')
        with open(path_read, encoding='utf-8', mode='r') as file_reader:
            file_write = open('prediction_index_scores.4narrow.done.txt', encoding='utf-8', mode='w')
            index = 0
            self.narrowed_index = set()
            for line in file_reader:
                index += 1
                if (index % 100 == 0):
                    print('==== Line %d' % (index))
                index_intent_score_list = line.strip().split('\t')
                item_current = index_intent_score_list[0]  # index, intent, score
                index_intent_score_current = item_current.split(' ')
                for item in index_intent_score_list:
                    index_intent_score = item.split(' ')
                    if index_intent_score_current[1] == index_intent_score[1]:  # same intent
                        flag = self.add_vector(index_intent_score[0], gap)
                        if flag:
                            self.narrowed_index.add(index_intent_score[0])
                            # new_lines.append('\t'.join(list(set(self.narrowed_index))))
            print('The number of narrowed index is {0}, gap {1}'.format(len(self.narrowed_index), gap))
            file_write.write('\n'.join(list(self.narrowed_index)))
        print("Method exe_narrow_trigger_queries() finished")

    def get_narrowed_index(self, path_read):
        file_writer = open(path_read[:-4] + '.narrowedindex.txt', encoding='utf-8', mode='w')
        training_index = set()
        with open(path_read, encoding='utf-8', mode='r') as file_reader:
            for line in file_reader:
                parts1 = line.strip().split('\t')
                for p in parts1:
                    parts2 = p.split(' ')
                    training_index.add(parts2[0])
        training_index = list(training_index)
        file_writer.write('\n'.join(training_index))
        print("Method get_narrowed_index() finished, len=", str(len(training_index)))

    def add_vector(self, index, gap):
        for n_index in self.narrowed_index:
            n_vector = self.vector_index[n_index]
            vector = self.vector_index[index]
            cosine = self.cal_cosine(n_vector, vector)
            if np.abs(cosine) <= gap:
                return False
        return True

    def index2vector(self, path_read):
        file_writer = open('training.vector.narrowed.txt', encoding='utf-8', mode='w')
        new_lines = []
        with open(path_read, encoding='utf-8', mode='r') as file_reader:
            for line in file_reader:
                index = line.strip()
                # intent = self.intent_index[index]
                # vector = map(str, self.vector_index[index])
                # vector_str = ' '.join(vector)
                new_line = index + '\t' + self.intent_index[index] + '\t' + ' '.join(map(str, self.vector_index[index]))
                new_lines.append(new_line)
        print("Method get_narrowed_index() finished, len=", str(len(new_lines)))
        file_writer.write('\n'.join(new_lines))

if __name__ == '__main__':
    """
    ### For bash script ###
    parser = ArgumentParser(description='Add some params.')
    parser.add_argument("-o", "--option", dest="option", choices=['narrow','precision'],
                        help="narrow or precision option")
    parser.add_argument("-g", "--gap", dest="gap", type=float,
                        help="gap between trigger queries. ", metavar="FILE")
    args = parser.parse_args()
    if args.option == 'narrow':
        if args.gap == None:  # evaluation.test.txt
            raise Exception("Param 'gap' should not be none.")
        else:
            print("gap=", str(args.gap))
            print("==== Begin to narrow the trigger queries.")
            calculator = CalSimilarity(candidates_path='training.vector.2000.txt')
            ### calculator.narrow_trigger_queries()  # get closest quires
            calculator.exe_narrow_trigger_queries('prediction_index_scores.4narrow.txt', args.gap)
            calculator.index2vector(path_read='prediction_index_scores.4narrow.done.txt')
            calculator = CalSimilarity(candidates_path='training.vector.narrowed.txt')
            calculator.evaluate()
    if args.option == 'precision':
        calculator = CalSimilarity(candidates_path='training.vector.narrowed.txt')
        # calculator.evaluate()
        # rank the scores with KNN and get results
        CalSimilarity.conclude_precision()

    """
    # calculator = CalSimilarity(candidates_path='training.vector.2000.txt')
    # # calculator.get_raw_trigger_queries()  # get closest quires for each training item
    #
    # calculator.exe_narrow_trigger_queries('prediction_index_scores.4narrow.txt', 0.0001)
    # calculator.index2vector(path_read='prediction_index_scores.4narrow.done.txt')
    calculator = CalSimilarity(candidates_path='training.vector.narrowed.txt')
    # calculator.evaluate(5)
    # # rank the scores with KNN and get results
    calculator.conclude_precision()
