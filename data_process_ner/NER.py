import re
import random
import json
import os


stop_words = [line.rstrip() for line in open('stop_words.txt', encoding='utf-8', mode='r')]
original_query_file = open('query_original_part.txt', encoding='utf-8', mode='w')

source_directory = 'D:\code\CMCC\data\source.1245.new_source.8.new_tianqi'

class EntityExtraction4Peopledaily(object):
    'extract entities corresponding their labels from data of PeopleDaily in 1988'
    def __init__(self):
        return

    def label_Entity_peopledaily(self, entity_initial):
        if ('product_name' in entity_initial):
            separator = '/PRODUCT'
            entity_initial = entity_initial.replace('product_name:', '')
        elif ('time' in entity_initial):
            separator = '/TIME'
            entity_initial = entity_initial.replace('time:', '')
        elif ('person_name' in entity_initial):
            separator = '/PERSON'
            entity_initial = entity_initial.replace('person_name:', '')
        elif ('company_name' in entity_initial):
            separator = '/COMPANY'
            entity_initial = entity_initial.replace('company_name:', '')
        elif ('org_name' in entity_initial):
            separator = '/ORG'
            entity_initial = entity_initial.replace('org_name:', '')
        elif ('location' in entity_initial):
            separator = '/LOCATION'
            entity_initial = entity_initial.replace('location:', '')
        else:
            separator = '/O'
            # entity_initial = entity_initial.replace('person_name:', '')
        separator += '||'
        entity_labeled = entity_initial + separator
        return entity_labeled

    def label_data_peopledaily(self):
        # split paragraph into sentances.
        separator_O = '/O||'
        pattern = re.compile(r'(.*?){{(.*?)}}(.*)')
        file_write = open('data_labeled.txt', encoding='utf-8', mode='w')
        # with open('data_to_label_part.txt', encoding='utf-8', mode='r') as file_read:
        with open('data_to_label.txt', encoding='utf-8', mode='r') as file_read:
            for sentance in file_read:
                sentance = sentance.strip()
                count = sentance.count('{{')
                sentance_labeled = ''
                tail = sentance
                for i in range(count + 1):
                    matcher = re.search(pattern, tail)
                    if (matcher != None):
                        head = matcher.group(1)
                        entity = matcher.group(2)
                        tail = matcher.group(3)
                        if (head != ''):
                            sentance_labeled += separator_O.join(head) + separator_O
                        entity_labeled = self.label_Entity_peopledaily(entity)
                        sentance_labeled += entity_labeled
                    else:
                        sentance_labeled += separator_O.join(tail) + separator_O
                sentance_labeled = sentance_labeled.replace('\n', '')
                sentance_labeled += '\n'
                file_write.write(sentance_labeled)

    def split_into_sentances_peopledaily(self):
        # split paragraph into sentances.
        file_write1 = open('.\\BosonNLP_NER_6C\\data_to_label.txt', encoding='utf-8', mode='w')
        content = ''
        with open('.\\BosonNLP_NER_6C\\BosonNLP_NER_6C.txt', encoding='utf-8', mode='r') as file_read:
            # with open('test.txt', encoding='utf-8', mode='r') as file_read:
            for paragraph in file_read:
                paragraph = paragraph.replace('?', '。')
                paragraph = paragraph.replace('!', '。')
                paragraph = paragraph.replace('~', '。')
                while ('。。' in paragraph):
                    paragraph = paragraph.replace('。。', '。')
                sentances = paragraph.split('。')
                sentances_new = '。\n'.join(sentances)
                content += sentances_new + '\n'
        content = content.replace('\n。\n', '\n')
        while ('\n\n' in content):
            content = content.replace('\n\n', '\n')
        paras = content.split('\n')
        for index in range(len(paras)):
            paras[index] = paras[index].strip()
            if len(paras[index]) <= 10:  # replace all sentances who's length is less than 10
                paras[index] = '###'
        content_new = '\n'.join(paras)
        content_new = content_new.replace('\n###\n', '\n')
        content_new = content_new.replace('\n###\n', '\n')
        content_new = content_new.replace('\\n', '')
        content_new = content_new.replace(' ', '')
        file_write1.write(content_new)


# format the entity labels to fitting the model
class EntityExtraction4Cmcc(object):
    'format the entity brace labels to fitting the model, 9 labels in total '
    def __init__(self):
        self.labels = ['business','attribute','act','date','price','data','call','pronoun','operator', 'location']


    def label_entity_cmcc(self, entity_initial):
        separator = ''
        for label in self.labels:
            if (label in entity_initial):
                separator = '/' + label.upper()
                entity_initial = entity_initial.replace(label+':', '')
                break
        # if ('product_name' in entity_initial):
        #     separator = '/PRODUCT'
        #     entity_initial = entity_initial.replace('product_name:', '')
        # elif ('time' in entity_initial):
        #     separator = '/TIME'
        #     entity_initial = entity_initial.replace('time:', '')
        # elif ('person_name' in entity_initial):
        #     separator = '/PERSON'
        #     entity_initial = entity_initial.replace('person_name:', '')
        # elif ('company_name' in entity_initial):
        #     separator = '/COMPANY'
        #     entity_initial = entity_initial.replace('company_name:', '')
        # elif ('org_name' in entity_initial):
        #     separator = '/ORG'
        #     entity_initial = entity_initial.replace('org_name:', '')
        # elif ('location' in entity_initial):
        #     separator = '/LOCATION'
        #     entity_initial = entity_initial.replace('location:', '')
        if (separator == ''):
            separator = '/O'
            # entity_initial = entity_initial.replace('person_name:', '')
        separator += '||'
        entity_labeled = entity_initial + separator

        return entity_labeled

    def label_data_cmcc(self, path_file):
        separator_O = '/O||'
        pattern = re.compile(r'(.*?){{(.*?)}}(.*)')
        file_write = open(path_file + '.labeled', encoding='utf-8', mode='w')
        # with open('data_to_label_part.txt', encoding='utf-8', mode='r') as file_read:
        with open(path_file, encoding='utf-8', mode='r') as file_read:
            for sentance in file_read:
                sentance = sentance.strip()
                count = sentance.count('{{')
                sentance_labeled = ''
                tail = sentance
                for i in range(count + 1):
                    if tail == '':
                        break
                    matcher = re.search(pattern, tail)
                    if (matcher != None):
                        head = matcher.group(1)
                        entity = matcher.group(2)
                        tail = matcher.group(3)
                        if (head != ''):
                            sentance_labeled += separator_O.join(head) + separator_O
                        entity_labeled = self.label_entity_cmcc(entity)
                        sentance_labeled += entity_labeled
                    else:
                        sentance_labeled += separator_O.join(tail) + separator_O
                sentance_labeled = sentance_labeled.replace('\n', '')
                sentance_labeled += '\n'
                file_write.write(sentance_labeled)


'''
extract 9 categories of entity labels for cmcc scenario
'''
class EntityLabelCmcc(object):
    def __init__(self):
        # 9 types of entities
        self.patterns = dict()
        self.config_path = 'Configure/'
        # self.entity_business = self.read_entity_from_config(self.config_path + 'gd-knowledge-20180205_TemplateToKnowledgeName.json')
        # self.entity_business += self.read_entity_from_config(self.config_path + 'gx-knowledge-20180205_TemplateToKnowledgeName.json')
        # self.entity_attribute = self.read_entity_from_config(self.config_path + 'attribute_merge.json')
        # self.entity_attribute += self.read_entity_from_config(self.config_path + 'attribute.add')

        self.entity_business = self.read_entity_from_config(self.config_path + 'gd-knowledge-20180205_TemplateToKnowledgeName.json')
        self.entity_business += self.read_entity_from_config(self.config_path + 'gx-knowledge-20180205_TemplateToKnowledgeName.json')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add1.rewrite')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add2_manual.rewrite')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add3_userdict.rewrite')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add4_cmcc.json')
        self.entity_attribute = self.read_entity_from_config(self.config_path + 'attribute_merge.json')
        self.entity_attribute += self.read_entity_from_config(self.config_path + 'attribute.add')

        self.entity_location = self.read_entity_from_config(self.config_path + 'location_add.rewrite')


        self.entity_business = list(set(self.entity_business))
        self.entity_attribute = list(set(self.entity_attribute))
        self.entity_location = list(set(self.entity_location))

        self.pattern_business = list()
        self.pattern_attribute = list()
        self.pattern_act = list()
        self.pattern_date = list()
        self.pattern_price = list()
        self.pattern_data = list()
        self.pattern_call = list()
        self.pattern_pronoun = list()
        self.pattern_operator = list()
        self.pattern_location = list()

        self.pattern_business = [re.compile(entity_b.replace('(','\(').replace(')','\)'))for entity_b in self.entity_business]
        self.pattern_attribute = [re.compile(entity_a.replace('(','\(').replace(')','\)'))for entity_a in self.entity_attribute]
        self.pattern_location = [re.compile(entity_l.replace('(','\(').replace(')','\)'))for entity_l in self.entity_location]
        self.pattern_act.append(re.compile(r'开通|办理|变更|取消'))
        self.pattern_date.append(re.compile(r'\d+年\d+月\d+日|\d+月\d+日'))
        self.pattern_price.append(re.compile(r'\d+元'))
        self.pattern_data.append(re.compile(r'\d+[M兆G]'))
        self.pattern_call.append(re.compile(r'\d+分钟|\d+min'))
        self.pattern_pronoun.append(re.compile(r'这个|这|那个|那|它们|它|他们|他|她们|她'))
        self.pattern_operator.append(re.compile(r'不多于|多于|不大于|大于|不少于|少于|不小于|小于|不超过|超过'))

        self.patterns['business'] = self.pattern_business
        self.patterns['attribute'] = self.pattern_attribute
        self.patterns['location'] = self.pattern_location
        self.patterns['act'] = self.pattern_act
        self.patterns['date'] = self.pattern_date
        self.patterns['price'] = self.pattern_price
        self.patterns['data'] = self.pattern_data
        self.patterns['call'] = self.pattern_call
        self.patterns['pronoun'] = self.pattern_pronoun
        self.patterns['operator'] = self.pattern_operator
        self.new_lines = []

    def read_entity_from_config(self, filepath_config):
        # file_config = open('gd-knowledge-20180205_TemplateToKnowledgeName.json', encoding='utf-8', mode='r')
        config_dict = json.load(open(filepath_config, encoding='utf-8', mode='r'))
        content_list = list()

        for key in config_dict.keys():
            content_list += config_dict[key]
        content_list = list(set(content_list))
        print('number of entity in configure file: ', str(len(content_list)))
        return content_list

    def extract_entity(self, path_read):
        # normaliza file
        file_write = open(path_read + '.extractentity', encoding='utf-8', mode='w')
        counter_entity = 0
        counter_labels = 0
        for pattern_key in self.patterns.keys():
            # print('====== pattern_key: ', pattern_key)
            pattern_list = self.patterns[pattern_key]

            with open(path_read, encoding='utf-8', mode='r') as file_read:
                if (self.new_lines == []):
                    lines = file_read.readlines()
                    lines = [line.upper() for line in lines]
                else:
                    lines = self.new_lines
                    self.new_lines = []
                counter_line = 0
                for line in lines:
                    if counter_line >= 500:
                        break
                    counter_line += 1
                    if(counter_line % 100 ==0):
                        print('====== counter_line: ', str(counter_line))
                    for pattern in pattern_list:
                        iters = re.finditer(pattern, line)
                        for iter in iters:
                            if (self.get_entity_flag(line, iter.group())):
                                print(iter.group())
                                counter_entity += 1
                                counter_labels += len(iter.group())
                                line = line.replace(iter.group(), '{{' +pattern_key +':'+ iter.group() +'}}')
                    self.new_lines.append(line)
        print('\nThere are {0} entities in file {1}'.format(counter_entity, path_read))
        print('\nThere are {0} entity labels in file {1}'.format(counter_labels, path_read))
        file_write.write(''.join(self.new_lines))

    #figure out if the entity is contained in another longer entity and has already been labeled
    def get_entity_flag(self, line, matcher):
        pattern = re.compile(r'.*({{.*?)'+matcher)
        m = pattern.search(line)
        if(m==None):
            return True
        elif ('}}' in m.group(1)):
            return True
        else:
            return False


def attribute_merge_into_json():
    attribute_dict = dict()
    for file_name in os.listdir('./'):
        if('attribute_' in file_name and not 'merge' in file_name):
            lines = open(file_name, encoding='utf-8', mode='r').readlines()
            lines = [line.strip() for line in lines]
            if ('' in lines):
                lines.remove('')
            attribute_dict[file_name[10:-4]] = lines
    with open('attribute__merge.json', encoding='utf-8', mode='w') as file_write:
        file_write.write(json.dumps(obj=attribute_dict, indent=2, ensure_ascii=False))

def segment(seperator):
    with open('data_segment.txt', encoding='utf-8', mode='wt') as segment_data_file:
        with open('data_2017.03_2017.08.txt', encoding='utf-8', mode='rt') as data_file:
            jieba.load_userdict('user_dict.txt')
            count = 0
            for line in data_file:
                count = count + 1
                print('count: ', str(count))
                line = line.lower()
                sentence = line.strip().split('\t')
                if (sentence[0] != ''):
                    sentence1 = sentence[0]
                    words = jieba.cut(sentence1.replace(' ', ''))
                    words = remove_stop_words(words)  # remove stop words
                    words = seperator.join(words)
                    words = merge(words, '\t\t')
                    segment_data_file.write(sentence[0] + '\t\t'+ words + '\n')

def writeToFile(line):
    original_query_file.write(line + '\n')

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

# ngcct-2018-02-04.txt
def process_rawdata(seperator):
    with open('ngcct_segment.txt', encoding='utf-8', mode='wt') as segment_data_file:
        with open('ngcct-2018-02-04-1200-part3.txt', encoding='utf-8', mode='rt') as data_file:
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

def remove_stop_words(segs):
    #stop_words = [line.rstrip() for line in open('stop_words.txt', encoding='utf-8', mode='rt')]
    # print('The number of stop words: ' + str(len(stop_words)))
    # stopwords = {}.fromkeys(['的', '附近'])
    final = list()
    for seg in segs:
        if seg not in stop_words:
            final.append(seg)
    return final

def upper_user_dict():
    with open('user_dict.txt', encoding='utf-8', mode='wt') as user_dict_file:
        with open('user_dict_raw.txt', encoding='utf-8', mode='rt') as user_dict_raw_file:
            distinct_dict = list()
            for line in user_dict_raw_file:
                line = line.upper()
                if line not in distinct_dict:
                    distinct_dict.append(line)
            for element in distinct_dict:
                user_dict_file.write(element)
            print('There are %d words in user dictionary' % (len(distinct_dict)))

# normalization
def replace_illegal_chars():
    with open('label_data', encoding='utf-8', mode='r') as file1:
        with open('label_data_after', encoding='utf-8', mode='w') as file2:
            for line in file1:
                if(not '�' in line and line != '\n'):
                    file2.write(line.upper())

def random_data(path_in, path_out, count):
    with open(path_in, encoding='utf-8', mode='r') as file_in:
        file_out2 = open(path_out+'.part4', encoding='utf-8', mode='w')
        with open(path_out+'.part3.10w', encoding='utf-8', mode='w') as file_out:
            lines = file_in.readlines()
            random.shuffle(lines)
            counter = 0
            counter2 = 0
            index = 0
            while ( counter < count and index < len(lines)):
                if (not '�' in lines[index]):
                    file_out.write(lines[index])
                    counter += 1
                    index += 1
                else:
                    index += 1
            while ( index < len(lines)):
                if (not '�' in lines[index]):
                    file_out2.write(lines[index])
                    counter2 += 1
                    index += 1
                else:
                    index += 1
            print('{0} bad data disposed \n{1} data written into file \'{2}\' \n{3} data written into file \'{4}\''.format((index - counter - counter2), counter, path_out+'.part1', counter2, path_out+'.part2'))

def random_data_nodup(path_in, path_out, count):
    with open ('log_combined_normalized_for_cmcc', encoding='utf-8', mode='r') as file_records:
        records = file_records.readlines()
    with open(path_in, encoding='utf-8', mode='r') as file_in:
        with open(path_out, encoding='utf-8', mode='w') as file_out:
            lines = file_in.readlines()
            random.shuffle(lines)
            counter = 0
            index = 0
            while ( counter < count and index < len(lines)):
                if (not '�' in lines[index] and not lines[index] in records):
                    file_out.write(lines[index])
                    counter += 1
                    index += 1
                else:
                    index += 1
            print('{0} bad data disposed \n{1} data written into file \'{2}\''.format((index - counter), counter, path_out))

# split the _merge dataset into original queries and standard questions
def split_data_set():
    file_writer1 = open('_merge.originalquery', encoding='utf-8', mode='w')
    file_writer2 = open('_merge.standardquery', encoding='utf-8', mode='w')
    original_query = set()
    standard_query = set()
    with open('_merge', encoding='utf-8', mode='r') as file_reader:
        for line in file_reader:
            line = line.strip().replace(' ','').upper().split('\t')
            if (len(line) >= 2):
                original_query.add(line[0])
                standard_query.add(line[1])
    print('len of original query: ', str(len(original_query)))
    print('len of standard query: ', str(len(standard_query)))
    file_writer1.write('\n'.join(original_query))
    file_writer2.write('\n'.join(standard_query))


class TrainingDataProcessor(object):
    'data process with _merge extracted entities labels for NER model training data'
    def __init__(self, path_root):
        self.path_root = path_root
        return

    '''
        将entity用花括号标出来
    '''
    def format_with_brace(self, path_read):
        file_writer = open(self.path_root+path_read+'.brace', encoding='utf-8', mode='w')
        lines = []
        with open(self.path_root+path_read, encoding='utf-8', mode='r') as file_reader:
            for line in file_reader:
                parts = line.strip().split('\t')
                if ('_' not in parts[1]):
                    line_new = parts[0]
                else:
                    flags = parts[1].split(' ')
                    chars = list(parts[0])
                    line_new = []
                    length = len(parts[0])
                    for index in range(length):
                        if (flags[index] == 'o'):
                            line_new.append(chars[index])
                        else:
                            tmp_tag = flags[index].split('_')[0] + ':'
                            if(index == 0 and flags[1] =='o'):
                                line_new.append('{{' + tmp_tag + chars[index] +'}}')
                            elif(index == 0 and flags[1] !='o'):
                                line_new.append('{{' + tmp_tag + chars[index])
                            elif(index == (length-1)):
                                line_new.append(chars[index]+'}}')
                            else:
                                if(flags[index] != flags[index - 1]):
                                    line_new.append('{{' + tmp_tag)
                                else:
                                    pass
                                line_new.append(chars[index])
                                if(flags[index] != flags[index + 1]):
                                    line_new.append('}}')
                                else:
                                    pass
                lines.append(''.join(line_new))
            lines_new = '\n'.join(lines)
            file_writer.write(lines_new)

    # valid data means each query contains at least 1 NE label
    def get_valid_data(self, path_file):
        file_writer = open(self.path_root+path_file+'.valid', encoding='utf-8', mode='w')
        line_new = []
        with open(self.path_root+path_file,  encoding='utf-8', mode='r') as file_reader:
            for line in file_reader:
                if('{{' in line):
                    line_new.append(line)
        file_writer.write(''.join(line_new))


'''
for entity linking
only extract entities of BUSINESS and ATTRIBUTE from standard query
'''
class CDSSMSentenceAndPhrase(object):
    def __init__(self):
        # 9 types of entities
        self.patterns = dict()
        self.pattern_tag = dict()
        self.config_path = 'Configure/'
        self.entity_business = self.read_entity_from_config(self.config_path + 'gd-knowledge-20180205_TemplateToKnowledgeName.json')
        self.entity_business += self.read_entity_from_config(self.config_path + 'gx-knowledge-20180205_TemplateToKnowledgeName.json')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add1.rewrite')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add2_manual.rewrite')
        self.entity_business += self.read_entity_from_config(self.config_path + 'entity_add3_userdict.rewrite')
        self.entity_attribute = self.read_entity_from_config(self.config_path + 'attribute_merge.json')
        self.entity_attribute += self.read_entity_from_config(self.config_path + 'attribute.add')
        self.entity_business = list(set(self.entity_business))
        self.entity_attribute = list(set(self.entity_attribute))
        self.entity_business = [ent.upper() for ent in self.entity_business]
        self.entity_attribute = [ent.upper() for ent in self.entity_attribute]
        self.pattern_business = list()
        self.pattern_attribute = list()
        self.pattern_act = list()
        self.pattern_date = list()
        self.pattern_price = list()
        self.pattern_data = list()
        self.pattern_call = list()
        self.pattern_pronoun = list()
        self.pattern_operator = list()

        self.pattern_business = [re.compile(re.sub('[()（）]', '', entity_b)) for entity_b in self.entity_business]
        self.pattern_attribute = [re.compile(re.sub('[()（）]', '', entity_a)) for entity_a in self.entity_attribute]
        self.pattern_act.append(re.compile(r'开通|办理|变更|取消|查询'))
        self.pattern_date.append(re.compile(r'\d+年\d+月\d+日|\d+月\d+日'))
        self.pattern_price.append(re.compile(r'\d+元'))
        self.pattern_data.append(re.compile(r'\d+[M兆G]'))
        self.pattern_call.append(re.compile(r'\d+分钟|\d+MIN'))
        self.pattern_pronoun.append(re.compile(r'这个|这|那个|那|它们|它|他们|他|她们|她'))
        self.pattern_operator.append(re.compile(r'不多于|多于|不大于|大于|不少于|少于|不小于|小于|不超过|超过'))

        self.patterns['business'] = self.pattern_business
        self.patterns['attribute'] = self.pattern_attribute
        self.patterns['act'] = self.pattern_act
        self.patterns['date'] = self.pattern_date
        self.patterns['price'] = self.pattern_price
        self.patterns['data'] = self.pattern_data
        self.patterns['call'] = self.pattern_call
        self.patterns['pronoun'] = self.pattern_pronoun
        self.patterns['operator'] = self.pattern_operator
        self.new_lines = []
        # tag: o other; a attribute; b business; c price; d datetime; e dataflow; f call duration; g act
        # self.pattern_tag['attribute'] = 'a'


    def read_entity_from_config(self, filepath_config):
        # file_config = open('gd-knowledge-20180205_TemplateToKnowledgeName.json', encoding='utf-8', mode='r')
        config_dict = json.load(open(filepath_config, encoding='utf-8', mode='r'))
        content_list = list()

        for key in config_dict.keys():
            content_list += config_dict[key]
        content_list = list(set(content_list))
        print('number of entity in configure file: ', str(len(content_list)))
        return content_list

    def extract_entity(self, path_read):
        # normaliza file
        file_write = open(path_read + '.extractentity', encoding='utf-8', mode='w')
        counter_entity = 0
        counter_line = 0
        with open(path_read, encoding='utf-8', mode='r') as file_read:
            for line in file_read:
                counter_line += 1
                print(line)
                line = line.upper().strip()
                if (counter_line % 100 == 0):
                    print('====== counter_line: ', str(counter_line))

                flag = [0 for i in range(len(line))]        # mark if the word is in any labels
                # tag: o other; a attribute; b business; c price; d datetime; e dataflow; f call duration; g act
                tag = ['o' for i in range(len(line))]
                for pattern_key in self.patterns.keys():
                    # print('====== pattern_key: ', pattern_key)
                    pattern_list = self.patterns[pattern_key]
                    for pattern in pattern_list:
                        matcher = re.finditer(pattern, line)
                        for m in matcher:
                            suffx = '_'+str(counter_entity + 1)
                            flag, tag, counter_entity = self.get_entity_flag(line, m, flag, tag, pattern_key + suffx, counter_entity)

                self.new_lines.append(line + '\t' + ' '.join(tag) + '\n')
            print('\nThere are {0} entities in file {1}'.format(counter_entity, path_read+'.extractentity'))
        file_write.write(''.join(self.new_lines))

    '''
    #figure out if the entity is contained in another longer entity and has already been labeled
    def get_entity_flag(self, line, matcher):
        pattern = re.compile(r'.*({{.*?)'+matcher+'.*')
        m = re.search(pattern, line)
        if(m==None):
            return True
        elif ('}}' in m.group(1)):
            return True
        else:
            return False
    '''

    def get_entity_flag(self, line, matcher, flag, tag, pattern_key, counter_entity):
        mark = ''
        idx_start = matcher.start()
        idx_end = matcher.end()

        flag_matcher = flag[idx_start: idx_end]
        if( 1 not in flag_matcher):
            mark = 'NoOverlap'
        elif(flag_matcher == [1 for i in range(len(flag_matcher))]):
            mark = 'Child'
        elif (1 in flag_matcher and 0 in flag_matcher):
            if(flag[idx_start] == 0 and flag[idx_end-1] == 0 ):
                mark = 'Parent'
            elif(flag[idx_start] == 1):
                if (idx_start >= 1 and flag[idx_start - 1] == 1):
                    mark = 'Cross'
                else:
                    mark = 'Parent'

            elif (flag[idx_end-1] == 1):
                if (idx_end < len(tag) and flag[idx_end] == 1):
                    mark = 'Cross'
                else:
                    mark = 'Parent'
        if mark == 'NoOverlap':
            counter_entity += 1
            for i in range(idx_start, idx_end):
                flag[i] = 1
                tag[i] = pattern_key
        elif(mark == 'Child'):
            pass
        elif(mark == 'Parent'):
            for i in range(idx_start, idx_end):
                flag[i] = 1
                tag[i] = pattern_key
        else:
            # flag == 'Cross', partly overlap, intersect with each other
            pass
        return flag, tag, counter_entity


def rewrite_entity_config(path_read):
    file_write = open(path_read+'.rewrite', encoding='utf-8', mode='w')
    entity_list = list()
    entity_dict = dict()
    with open(path_read, encoding='utf-8', mode='r') as file_read:
        for line in file_read:
            line = line.strip()
            if (line == ''):
                pass
            else:
                # tmp = line.split(' ')   # should the entity separated by space? or delete space?
                tmp = [line.replace(' ', '')]
                entity_list += tmp
                # entity_list.append(tmp[0])
    entity_list = list(set(entity_list))
    if('' in entity_list):
        entity_list.remove('')
    entity_dict["实体配置"] = entity_list
    file_write.write(json.dumps(obj=entity_dict, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    print('============== main entrance')
    print("we are in %s"%__name__)
    # split_into_sentances()
    # label_data()
    # attribute_merge_into_json()
    # split_data_set()
    # file_path = 'test'
    # file_path = '_merge.originalquery.part1'
    # rewrite_entity_config('Configure\\location_add')
    # file_path = 'cmcc_query_standard'
    file_path = 'test.txt'
    entity_extractor = EntityLabelCmcc()
    entity_extractor.extract_entity(path_read=file_path)
    # training_data_processor = TrainingDataProcessor('TrainingData\\')
    # training_data_processor.get_valid_data('_merge.originalquery.part1.extractentity')
    # training_data_processor.get_valid_data('cmcc_query_standard_nodup_ner.extractentity')
    #
    # data_labeler = EntityExtraction4Cmcc()
    # data_labeler.label_data_cmcc('TrainingData\\cmcc_query_standard_nodup_ner.extractentity.valid')
    # data_labeler.label_data_cmcc('TrainingData\\test1.extractentity.valid')

    # random_data('D:\code\CMCC\data_share\share_data_yuguang\\fanyuguang\cmcc_original queries.txt', 'queries', 5000)          # random data for self labeling by hand
    # random_data('queries.part2', 'queries', 100000)            # random data for cmcc labeling


    # cdssm = CDSSMSentenceAndPhrase()
    # cdssm.extract_entity(path_read=file_path)
    #
    # training_data_processor = TrainingDataProcessor('TrainingData\\')
    # training_data_processor.format_with_brace('cmcc_query_standard.extractentity')
    # training_data_processor.get_valid_data('cmcc_query_standard.extractentity')
    # data_labeler = EntityExtraction4Cmcc()
    # data_labeler.label_data_cmcc('TrainingData\\test1.extractentity.valid')
    #
