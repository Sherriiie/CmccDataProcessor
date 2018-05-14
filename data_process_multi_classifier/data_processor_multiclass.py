import datetime
import array
import os
import random
import jieba
import re
import random
import xlrd


original_query_file = open('query_original_part.txt', encoding='utf-8', mode='w')
# stop_words = [line.rstrip() for line in open('stop_words.txt', encoding='utf-8', mode='r')]
source_directory = 'D:\code\CMCC\data\source.1245.new_source.8.new_tianqi'

#split the queries to make every character in query is seperated by space ' '
def data_processor_split(filepath):
    file_write = open(filepath + '_split', encoding='utf-8', mode='w')
    with open(filepath, encoding='utf-8', mode='r') as file_read:
        for line in file_read:
            parts = line.strip().split('\t')
            new_line = ' '.join(parts[0]) + '\t' + parts[1] +'\n'
            file_write.write(new_line)

def create_vocabulary_dict(filepath):
    with open(filepath, encoding='utf-8', mode='r') as file1:
        with open('final/vocabulary.txt', encoding='utf-8', mode='w') as file2:
            index = 0
            vocab_dict = dict()
            for line in file1:
                index = index + 1
                # characters = list(line.strip().replace(' ','').replace('\t', '').replace('\n', ''))
                characters = list(line.strip().split('\t')[0].replace(' ','').replace('\t', '').replace('\n', ''))
                for char in characters:
                    if char in vocab_dict.keys():
                        vocab_dict[char] = vocab_dict[char] + 1
                    else:
                        vocab_dict[char] = 1
                if (index%100 == 0):
                    print('line %d processed successfully' %(index))
            print('line %d processed successfully' % (index))
            for key in vocab_dict.keys():
                if vocab_dict[key] > 5:
                    file2.write(key + '\n')
            print('vocabulary processed successfully')

def get_dataset_by_intent(path_read):
    path_intent_root = './intent_extraction/'
    file_write_diagnosis = open(path_intent_root+'intent_diagnosis', encoding='utf-8', mode='w')
    file_write_request_userinfo = open(path_intent_root+'intent_request_userinfo', encoding='utf-8', mode='w')
    file_write_request_attribute = open(path_intent_root+'intent_request_attribute', encoding='utf-8', mode='w')			# attribute is merged with business here
    file_write_request_open = open(path_intent_root+'intent_request_open', encoding='utf-8', mode='w')
    file_write_request_change = open(path_intent_root+'intent_request_change', encoding='utf-8', mode='w')
    file_write_request_cancel = open(path_intent_root+'intent_request_cancel', encoding='utf-8', mode='w')
    file_write_request_complaint = open(path_intent_root+'intent_request_complaint', encoding='utf-8', mode='w')
    file_write_request_recommendation = open(path_intent_root+'intent_request_recommendation', encoding='utf-8', mode='w')
    file_write_request_compare = open(path_intent_root+'intent_request_compare', encoding='utf-8', mode='w')
    file_write_request_business = open(path_intent_root+'intent_request_business', encoding='utf-8', mode='w')
    file_write_request_relation = open(path_intent_root+'intent_request_relation', encoding='utf-8', mode='w')
    file_write_request_other= open(path_intent_root+'intent_request_other', encoding='utf-8', mode='w')

    counter_diagnosis = 0
    counter_request_userinfo = 0
    counter_request_attribute = 0
    counter_request_open = 0
    counter_request_change = 0
    counter_request_cancel = 0
    counter_request_complaint = 0
    counter_request_recommendation = 0
    counter_request_compare = 0
    counter_request_business = 0
    counter_request_relation = 0
    counter_request_other = 0
    pattern_attribute = r'开通方法|办理方法|取消方法|退订方法|价格|多少钱|资费|对象'

    with open(path_read, encoding='utf-8', mode='r') as file_read:
        index = 0
        index_valid = 0
        for line in file_read:
            index += 1
            index_valid += 1
            if (line == '\n'):
                index_valid += -1
                continue
            # print('Query {0} is being processd. '.format(index))
            if ('为什么' in line or '怎么办' in line):		 # intent == 'diagnosis'
                counter_diagnosis += 1
                file_write_diagnosis.write(line)
            elif ( re.search(re.compile(pattern_attribute), line)!= None):
                counter_request_attribute += 1
                file_write_request_attribute.write(line)
            elif ('开通' in line or '办理' in line):
                counter_request_open += 1
                file_write_request_open.write(line)
            elif ('取消' in line):
                counter_request_cancel += 1
                file_write_request_cancel.write(line)
            elif ('变更' in line or '更换' in line):
                counter_request_change += 1
                file_write_request_change.write(line)
            elif ('我的' in line):
                counter_request_userinfo += 1
                file_write_request_userinfo.write(line)
            elif ('投诉' in line):
                counter_request_complaint += 1
                file_write_request_complaint.write(line)
            elif ('推荐' in line):
                counter_request_recommendation += 1
                file_write_request_recommendation.write(line)
            elif ('对比' in line or '区别' in line):        # '比较' 没有考虑
                counter_request_compare += 1
                file_write_request_compare.write(line)
            elif ('介绍' in line):
                counter_request_business += 1
                file_write_request_business.write(line)
            elif ('关系' in line):
                counter_request_relation += 1
                file_write_request_relation.write(line)
            # elif ('' in line):
            # 	counter_request_attribute += 1
            # 	file_write_request_attribute.write(line)
            else:
                intent_result = filter_intent_attribute(line)
                if (intent_result == 'intent_attribute'):
                    counter_request_attribute += 1
                    file_write_request_attribute.write(line)
                elif (intent_result == 'intent_diagnosis'):
                    counter_diagnosis += 1
                    file_write_diagnosis.write(line)
                elif (intent_result == 'intent_compare'):
                    counter_request_compare += 1
                    file_write_request_compare.write(line)
                else:
                    counter_request_other += 1
                    file_write_request_other.write(line)
        print('{0} queries are being processd. \n{1} queries are valid.'.format(index, index_valid))


def filter_intent_attribute(line):
    intent_attribute = ['话费发票怎么打印', 'PIN码查询方法', '号码停机进入保留期有什么影响', '无应答呼叫转移设置方法', '最低消费查询方法', '4G飞享套餐短彩信资费', '无条件呼叫转移设置方法', '实名制修改方法','电子发票发票获取方法',
                        '空中充值发票怎么领取', '移动网站订单查询方法', '过户需要具备哪些条件', '万能副卡设置方法', '呼叫转移设置方法', '查询本机号码方法', '怎么在微信捆绑手机号码？', '什么时候可以查询上月账单', '手机上网参数设置方法' ]
    intent_diagnosis = ['积分商城礼品怎么兑换不了', '充值成功但话费未到账', '积分兑换不了原因']
    intent_compare = ['飞信会员与非会员区别', '修改密码和重置密码区别']
    intent_business = ['和对讲业务功能', '销户是什么意思？', '账单增值业务费是什么', '增值业务是什么意思？', '委托书是什么意思']
    intent_recommendation = ['和对讲业务功能', '销户是什么意思？', '账单增值业务费是什么', '增值业务是什么意思？', '委托书是什么意思']
    part = line.strip().split('\t')[1]
    if part in intent_attribute:
        return 'intent_attribute'
    elif part in intent_diagnosis:
        return 'intent_diagnosis'
    elif part in intent_compare:
        return 'intent_compare'
    else:
        return 'Other'

def refine_training_data(filepath):
    file_writer = open(filepath + '.refined', encoding='utf-8', mode='w')
    new_lines = []
    pattern_recommendation = r'套餐|上网|流量|宽带|手机'
    pattern_attribute = r'开通方法|办理方法|取消方法|退订方法|价格|多少钱|资费介绍|对象'
    pattern_relation = r'之间关系|的关系|什么关系'

    with open(filepath, encoding='utf-8', mode='r') as file_reader:
        for line in file_reader:
            line_orginal = line.strip()
            parts = line_orginal.split('\t')
            line = line.strip().replace(' ', '')

# category 6 is of high confidence
            if (parts[1] == '6'):
                    new_lines.append(line_orginal)
            else:
                if(re.search(re.compile(pattern_recommendation), line) != None and '推荐' in line):
                    if (parts[1] != '4'):
                        # print('4: '+line)
                        pass
                    new_lines.append(parts[0] + '\t' +'4')
                elif (re.search(re.compile(pattern_attribute), line) != None):
                    if (parts[1] != '2'):
                        pass
                        # print('2: '+line)
                    new_lines.append(parts[0] + '\t' +'2')
                elif (re.search(re.compile(pattern_relation), line) != None):
                    if (parts[1] != '1'):
                        print('1: '+line)
                    new_lines.append(parts[0] + '\t' +'1')

                elif ('比较' in line):        # convert the intention of compare with pattern of '比较' to 'other'
                    if (parts[1] == '3'):
                        new_lines.append(parts[0] + '\t' +'0')

                else:
                    new_lines.append(line_orginal)

    file_writer.write('\n'.join(new_lines))



def get_intent_raw(path_read, path_write_all, path_write_log, intent):
    file_write = open(path_read + '_raw', encoding='utf-8', mode='w' )
    file_write_all = open( path_write_all, encoding='utf-8', mode='a')
    file_write_log = open( path_write_log, encoding='utf-8', mode='a')
    counter = 0
    with open(path_read, encoding='utf-8', mode='r') as file_read:
        for line in file_read:
            counter += 1
            parts = line.strip().split('\t')
            query_raw = parts[0]
            file_write.write(query_raw + '\t' + str(intent) + '\n')
            file_write_all.write(query_raw + '\t' + str(intent) + '\n')
        print('%d lines were written!' %counter)
    file_write_log.write('{0}_raw {1} lines were written!\n'.format(path_read, counter))




def map_intent_with_id():
    intent_dict = {'relation': 1, 'attribute': 2, 'compare': 3, 'recommendation': 4, 'userinfo': 5, 'diagnosis': 6,
                   'cancel': 7, 'change': 8, 'open': 9, 'business': 2, 'complaint': 10, 'other': 0, }
    intent_redict = {0: 'other', 1: 'relation', 2: 'attribute', 3: 'compare', 4: 'recommendation', 5: 'userinfo',
                     6: 'diagnosis',
                     7: 'cancel', 8: 'change', 9: 'open', 10: 'business', 11: 'complaint'}

    file_write_all = open('./intent_extraction/' + 'all_original', encoding='utf-8', mode='w')
    file_write_all.close()
    file_write_log = open('./intent_extraction/' + '_log', encoding='utf-8', mode='w')
    file_write_log.close()
    for file in os.listdir('./intent_extraction/'):
        if ('intent' in file and not 'raw' in file):
            intent_file = file.strip().split('_')[-1]
            intent_id = intent_dict[intent_file]
            get_intent_raw('./intent_extraction/' + file, './intent_extraction/all_original', './intent_extraction/log', intent_dict[intent_file])


def random_data(path_in, path_out, count):
    file_out_training = open('training.txt', encoding='utf-8', mode='w')
    file_out_evaluation_all = open(path_out+'_all', encoding='utf-8', mode='w')
    file_out_evaluation_cmcc = open(path_out+'_cmcc', encoding='utf-8', mode='w')
    file_out_log = open('_log', encoding='utf-8', mode='w')

    with open(path_in, encoding='utf-8', mode='r') as file_in:
        lines = file_in.readlines()
        random.shuffle(lines)
        counter_evaluation = 0
        counter_training = 0
        index = 0
        counter_intent = [0,0,0,0] # [intent_2, intent_3, intent_4, intent_5]

        while ( counter_evaluation < count and index < len(lines)):
            if (not '�' in lines[index]):
                file_out_evaluation_all.write(lines[index])
                intent_id = lines[index].strip().split('\t')[1]
                intents_cmcc = ['2','3','4','5']
                if (intent_id in intents_cmcc):
                    file_out_evaluation_cmcc.write(lines[index])
                    counter_intent[int(intent_id)-2] += 1
                counter_evaluation += 1
                index += 1
            else:
                index += 1
        print('{1} data written into file \'{2}\' \n{0} bad data disposed.\n'.format((index - counter_evaluation), counter_evaluation, path_out))
        file_out_log.write('{1} data written into file \'{2}\' \n{0} bad data disposed.'.format((index - counter_evaluation), counter_evaluation, path_out))
        file_out_log.write('{0} intent2, attribute\n{1} intent3, compare\n{2} intent4, recommendation\n{3} intent5, userinfo\n'.format(str(counter_intent[0]), str(counter_intent[1]), str(counter_intent[2]), str(counter_intent[3]) ))
        flag = index

        while(index < len(lines)):
            if (not '�' in lines[index]):
                file_out_training.write(lines[index])
                counter_training += 1
                index += 1
            else:
                index += 1
        print('{1} data written into file \'{2}\' \n{0} bad data disposed.'.format((index - flag - counter_training), counter_training,
                                                                                  'training.txt'))
# lower all case
# replace all ',' '"' ‘\n’ ''' inside segments, upper the case
def data_checker(filepath):
    with open(filepath, encoding='utf-8', mode='r') as f1:
        with open(filepath + '_checker', encoding='utf-8', mode='w') as f2:
            index = 0
            for line in f1:
                if('�' in line):
                    print('bad line:', line)
                else:
                    line = line.upper()
                    index = index +1
                    # print('====== index = ', index)
                    segments = line.split('\t')
                    if (len(segments) != 2):
                        raise Exception("Invalid level!", index, line)
                    new_line = segments[0].replace(',', '').replace('"', '').replace('‘', '').replace('\n', '').replace('”', '').replace('“', '').replace('’', '') + '\t' \
                               + segments[1].replace(',', '').replace('"', '').replace('‘', '').replace('\n', '').replace('”', '').replace('“', '').replace('’', '')
                    new_line1 = new_line.strip().replace('  ', ' ') + '\n'
                    f2.write(new_line1)
            print('====== index = ', index)

# ngcct-2018-02-04.txt, extract for intent labelling, remove stop words,
def process_rawdata_intent(seperator):
    with open('ngcct_segment.txt', encoding='utf-8', mode='wt') as segment_data_file:
        with open('ngcct-2018-02-04-1200-part1.txt', encoding='utf-8', mode='rt') as data_file:
            jieba.load_userdict('user_dict.txt')
            index = 0
            for line in data_file:
                line = line.lower()
                index = index + 1
                print('processing index = ' + str(index))
                pattern1 = re.compile(r'(.*?)"(用户)",.*?"(.*?)",".*')        # for user
                pattern2 = re.compile(r'(.*?)"(坐席)",.*?"(.*?)",".*')        # for operator
                matcher1 = re.search(pattern1, line)
                matcher2 = re.search(pattern2, line)
                if(matcher1 != None ):
                    groups = matcher1.groups()
                    writeToFile(groups[2])
                    segs = jieba.cut(groups[2])
                    segs = remove_stop_words(segs)          # remove stop words
                    new_line = groups[0] + '\t' + groups[1] + '\t' + seperator.join(segs)
                    new_line = merge(new_line, '\t\t')          # merge
                    segment_data_file.write(new_line + '\n')
                elif (matcher2 != None):
                    groups = matcher2.groups()
                    writeToFile(groups[2])
                    segs = jieba.cut(groups[2])
                    segs = remove_stop_words(segs)
                    new_line = groups[0] + '\t' + groups[1] + '\t' + seperator.join(segs)
                    new_line = merge(new_line, '\t\t')
                    segment_data_file.write(new_line + '\n')

def writeToFile(line):
    original_query_file.write(line + '\n')

def remove_stop_words(segs):
    #stop_words = [line.rstrip() for line in open('stop_words.txt', encoding='utf-8', mode='rt')]
    # print('The number of stop words: ' + str(len(stop_words)))
    # stopwords = {}.fromkeys(['的', '附近'])
    final = list()
    for seg in segs:
        if seg not in stop_words:
            final.append(seg)
    return final

def merge(words, seprator):
    pattern = re.compile( r'(.*?\d)(\t\t)([元块年月日天号时分Mm兆折十百千万亿个Gg位].*)')
    matcher = re.search(pattern, words)
    while (matcher != None):
        groups = matcher.groups();
        words = groups[0] + groups[2]
        matcher = re.search(pattern, words)

    pattern = re.compile(r'(.*?)(\t\t/\t\t)(.*)')
    matcher = re.search(pattern, words)
    while (matcher != None):
        groups = matcher.groups();
        words = groups[0] + re.sub('\t\t/\t\t', '/', groups[1]) + groups[2]
        matcher = re.search(pattern, words)

    pattern = re.compile(r'(.*?个)(\t\t)(月.*)')
    matcher = re.search(pattern, words)
    while (matcher != None):
        groups = matcher.groups();
        words = groups[0] + groups[2]
        matcher = re.search(pattern, words)
    return words

# contains 50 items for each type in cmcc evaluation data
def evaluation_balance():
    file_out_balanced = open('evaluation.txt.cmcc.banlanced', encoding='utf-8', mode='w')
    new_lines = ''
    with open('evaluation.txt.cmcc', encoding='utf-8', mode='r') as file_in:
        counter_intent2 = 0
        counter_intent5 = 0
        for line in file_in:
            parts = line.strip().split('\t')
            intent_category = parts[1]
            if (intent_category == '2'):
                counter_intent2 += 1
                if (counter_intent2 <= 100):
                    new_lines += line
            elif (intent_category == '5'):
                counter_intent5 += 1
                if (counter_intent5 <= 100):
                    new_lines += line
            else:
                new_lines += line
    file_out_balanced.write(new_lines)

# process the excel files
def read_excel():
    wb = xlrd.open_workbook('evaluation.labelbyhand.xlsx')
    file_writer = open('evaluation.labelbyhand.add' , encoding='utf-8', mode='w')
    sheet1 = wb.sheet_by_name(u'all.labelbyhand')
    new_line = ''
    counter = 0
    # temp = sheet1.row_values()
    for index_row in range(sheet1.nrows):
        # print(sheet1.row_values(index_row))
        if(sheet1.row_values(index_row)[1] == 5.0):
            new_line += sheet1.row_values(index_row)[0] + '\t' + str(sheet1.row_values(index_row)[1])[:1] + '\n'
            counter += 1
    file_writer.write(new_line)
    print('total lines 3', str(counter))


def pick_evaluation_out_from_all(filepath):
    file_log = open('./final/_log', encoding='utf-8', mode='w')
    file_evaluation = open('./final/evaluation.txt', encoding='utf-8', mode='r')
    file_evaluation1 = open('./final/evaluation.add.txt', encoding='utf-8', mode='w')
    file_evaluation_labeled = open('./final/evaluation.labeled.txt', encoding='utf-8', mode='w')
    file_training = open('./final/training.txt', encoding='utf-8', mode='w')
    lines_all = open(filepath, encoding='utf-8', mode='r').readlines()
    random.shuffle(lines_all)
    evaluation_query = file_evaluation.readlines()
    # for line in evaluation_query:
    #     if (line.strip().split('\t')[1] == '5'):
    #         file_training.write(line)
    #     else:
    #         file_evaluation_labeled.write(line)

    counter1 = 0
    counter4 = 0
    evaluation_query_add = []
    # evaluation_query = [ query.strip().split('\t')[0] for query in evaluation_query]
    for line in lines_all:
        parts = line.strip().split('\t')
        if (line in evaluation_query):
            file_log.write(line)
        # elif (parts[1] == '1' and counter1 <50):
        #     evaluation_query_add.append(line)
        #     file_log.write(line)
        #     counter1 += 1
        # elif (parts[1] == '4' and counter4 <50):
        #     evaluation_query_add.append(line)
        #     file_log.write(line)
        #     counter4 += 1
        else:
            file_training.write(line)

    file_evaluation1.write(''.join(list(set(evaluation_query_add))))


if __name__ == '__main__':
    print("we are in %s"%__name__)

    # get_dataset_by_intent('../_merge')   # filtered the blank lines
    # get_dataset_by_intent('test')   # filtered the blank lines
    # map_intent_with_id()
    # data_checker('./intent_extraction/all_original')
    # data_processor_split('./intent_extraction/all_original_checker')
    # random_data('all_split', 'evaluation.txt', 10000)
    # create_vocabulary_dict('final/training.txt')
    # evaluation_balance()
    read_excel()
    # pick_evaluation_out_from_all('./final/all_original_checker_split')
    # refine_training_data('./final/training.txt')
