import datetime
import array


class DataProcessor(object):
    def __init__(self):
        return

    def clean_data(self):
        file_write1 = open('_merge.querypair.v1', encoding='utf-8', mode='w')
        file_write2 = open('_merge.originalquery.v1', encoding='utf-8', mode='w')
        file_write3 = open('_merge.standardquery.v1', encoding='utf-8', mode='w')
        raw_dict = {}
        new_query_ori = ''
        new_query_standard = ''
        new_pair = ''
        with open('D:\code\CMCC\data_share\source.1245.new_source.8.new_tianqi\\training_data\\_merge', encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                parts = line.strip().split('\t')
                if (len(parts) < 2):
                    print(line)
                else:
                    raw_dict[parts[0].strip()] = parts[1].strip()
        counter = 0
        with open('D:\code\CMCC\data_share\share_data_yuguang\\fanyuguang\\cmcc_original_queries.txt', encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                counter += 1
                if(counter%100==0):
                    print("counter : " , str(counter))
                line = line.strip()
                if (line != ''):
                    if (line in raw_dict.keys()):
                        new_query_ori = new_query_ori + raw_dict[line] +'\n'
                        new_query_standard = new_query_standard + line +'\n'
                        new_pair = new_pair + line + '\t' + raw_dict[line] + '\n'
                    else:
                        print(line)

        file_write2.write(new_query_ori)
        file_write3.write(new_query_standard)
        file_write1.write(new_pair)
        print('lines:', str(counter))


def data_processor_train():
    with open('_merge', encoding='utf-8', mode='r') as file1:
        with open('after', encoding='utf-8', mode='w') as file2:
            index = 0
            for line in file1:
                index = index + 1
                segments = line.strip().split('\t')
                try:
                # temp_array = list(segments[0].strip())
                # temp_string = ' '.join(temp_array)
                    new_line = ' '.join(list(segments[0].strip())) + '\t' + ' '.join(list(segments[1].strip())) + '\n'

                    file2.write(new_line)
                    if (index%100 == 0):
                        print('line %d processed successfully' %(index))
                except:
                    print('exception index %d' %index)

# process label5 evaluation.txt, escape, no segment here.
def data_processor_evaluation_label5():
    with open('label.qq.cmcc.5.validation.norm_', encoding='utf-8', mode='rt') as old_data_file:
        with open('label.qq.cmcc.5.validation.norm_.temp', encoding='utf-8', mode='wt') as new_data_file:
            for line in old_data_file:
                temp = line.strip().replace(' ', '').split('\t\t')
                parts = list()
                parts.append(temp[0])
                temp1 = temp[1].strip().split('\t')
                parts.append(temp1[0])
                parts.append(temp1[1])
                if (len(parts) == 3):
                    if (parts[1] =='Perfect'):
                        parts[1] = parts[2]
                        parts[2] = 1
                    elif(parts[1] =='Bad'):
                        parts[1] = parts[2]
                        parts[2] = 0
                    else:
                        raise Exception('ERROR')
                    new_line = ''
                    for part in parts:
                        if(part == 1 or part == 0):
                            new_line = new_line + '\t' + str(part)
                        else:
                            new_line = new_line + '\t' + ' '.join(part)
                    new_line = new_line.strip()
                    new_line = new_line + '\n'
                    new_data_file.write(new_line)
            return

# process label6 evaluation.txt, escape, no segment here.
def data_processor_evaluation_label6():
    with open('label.6_evaluation', encoding='utf-8', mode='rt') as old_data_file:
        with open('label.6_evaluation_temp', encoding='utf-8', mode='wt') as new_data_file:
            new_line = ''
            index = 0
            for line in old_data_file:
                index += 1
                print('index,', index)
                parts = line.strip().replace(' ', '').split('\t')
                if (len(parts) == 3):
                    new_line += ' '.join(parts[1].strip()) + '\t' + ' '.join(parts[2].strip()) + '\t' + parts[0] + '\n'
            new_data_file.write(new_line)
            return

# delete the queries with no correct answers in standard evaluation set
def delete_no_answer_query():
    # with open('label.qq.cmcc.5.validation.norm_.temp', encoding='utf-8', mode='r') as data_file:
    with open('label.6_evaluation_temp', encoding='utf-8', mode='r') as data_file:
        new_text = ''
        segments2 = list()
        queries = list()
        answers = list()
        ticks = list()
        correct_count = 0  # correct cnt
        false_count = 0
        bad_line_index = list()
        line_index = 0
        for line in data_file:
            line = line.strip()
            line_index = line_index + 1
            segments1 = line.replace('\ufeff', '').split('\t')  # replace the BOM \ufeff
            if (segments2 == [] or segments1[0] == segments2[0]):
                queries.append(line)
                answers.append(segments1[1])
                ticks.append(segments1[2])
                segments2 = segments1
            else:
                if (ticks.count('1') >= 1):
                    new_text = new_text + '\n'.join(queries) + '\n'
                    correct_count += 1
                else:
                    bad_line_index.append(str(line_index - 1))
                    false_count += 1
                queries = []
                answers = []
                ticks = []
                queries.append(line)
                answers.append(segments1[1])
                ticks.append(segments1[2])
                segments2 = segments1

    with open('label.6_evaluation.final', encoding='utf-8', mode='w') as new_text_file:
        new_text_file.write(new_text)


    print('\n===================\n' + 'Total query count %d' % (correct_count + false_count ))
    print('Correct evaluation %d' % correct_count)
    print('False evaluation %d' % false_count)
    print('Bad line count %d ' % len(bad_line_index))
    print(bad_line_index)

def create_vocabulary_dict():
    with open('training.txt', encoding='utf-8', mode='r') as file1:
        with open('vocabulary.txt', encoding='utf-8', mode='w') as file2:
            index = 0
            vocab_dict = dict()
            for line in file1:
                index = index + 1
                characters = list(line.strip().replace(' ','').replace('\t', '').replace('\n', ''))
                for char in characters:
                    if char in vocab_dict.keys():
                        vocab_dict[char] = vocab_dict[char] + 1
                    else:
                        vocab_dict[char] = 1
                if (index%100 == 0):
                    print('line %d processed successfully' %(index))
            for key in vocab_dict.keys():
                if vocab_dict[key] > 5:
                    file2.write(key + '\n')
            print('vocabulary processed successfully')

# lower all case
# replace all ',' '"' ‘\n’ inside segments
def data_checker():
    with open('training.txt', encoding='utf-8', mode='r') as f1:
        with open('training_checker.txt', encoding='utf-8', mode='w') as f2:
            index = 0
            for line in f1:
                line = line.upper()
                index = index +1
                print('====== index = ', index)
                segments = line.split('\t')
                if (len(segments) != 2):
                    raise Exception("Invalid level!", index, line)
                new_line = segments[0].replace(',', '').replace('"', '').replace('\n', '') + '\t' + segments[1].replace(',', '').replace('"', '').replace('\n', '') + '\n'
                f2.write(new_line)
    return


def create_evaluation_set():
    with open('evaluation.txt', encoding='utf-8', mode='r') as f1:
        with open('evaluation_single.txt', encoding='utf-8', mode='w') as f2:
            index = 0
            for line in f1:
                line = line.upper()
                index = index + 1
                print('====== index = ', index)
                segments = line.split('\t')
                new_line = segments[0] + '\n' + segments[1]
                f2.write(new_line)


# extraction the data that are predicted wrong in evaluation
def extract_false_evaluations():
    with open('evaluation.txt.scoring.label5.test', encoding='utf-8', mode='r') as f1:
        with open('evaluation.txt.scoring.label5.test.error', encoding='utf-8', mode='w') as f2:
            segments2  = list()
            queries = list()
            answers = list()
            scores = list()
            ticks = list()
            correct_count = 0   #  correct cnt
            false_count = 0
            bad_line_index = list()
            line_index = 0
            for line in f1:
                line_index = line_index + 1
                segments1 = line.strip().replace('\ufeff', '').split('\t')          # replace the BOM \ufeff
                if (segments2 == [] or segments1[0] == segments2[0]):
                    queries.append(line)
                    answers.append(segments1[1])
                    scores.append(segments1[3])
                    ticks.append(segments1[2])
                    segments2 = segments1
                else:
                    max_index = scores.index(max(scores))
                    if (ticks[max_index] == '1'):
                        correct_count = correct_count + 1
                        print('correct evaluation %d' % correct_count)
                    elif (ticks.count('1') == 1):
                        false_count = false_count + 1
                        # tmp = ticks.index('1')
                        f2.write(queries[ticks.index('1')])
                        f2.write(queries[max_index])
                    else:
                        bad_line_index.append(str(line_index - 1))

                    queries = []
                    answers = []
                    scores = []
                    ticks = []
                    queries.append(line)
                    answers.append(segments1[1])
                    scores.append(segments1[3])
                    ticks.append(segments1[2])
                    segments2 = segments1
    print('\n===================\n' + 'Total query count %d' % (correct_count + false_count + len(bad_line_index) ))
    print('Correct evaluation %d' % correct_count)
    print('False evaluation %d' % false_count)
    print('Bad line count %d ' % len(bad_line_index))
    print(bad_line_index)






if __name__ == '__main__':
    # data_processor_evaluation_label6()
    # data_processor_evaluation_label5()
    # delete_no_answer_query()  # for the evaluation set
    # create_vocabulary_dict()
    # extract_false_evaluations()

    # create_evaluation_set()
    # extract_false_evaluations()
    data_processor = DataProcessor()
    data_processor.clean_data()
