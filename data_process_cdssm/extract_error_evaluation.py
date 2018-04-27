import datetime
import array

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

# evaluation.txt, escape, no segment is good here.
def data_processor_evaluation():
    with open('label.qq.cmcc.5.validation.norm_.old', encoding='utf-8', mode='rt') as old_data_file:
        with open('label.qq.cmcc.5.validation.norm_.txt', encoding='utf-8', mode='wt') as new_data_file:
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


# def data_processor_evaluation():
# 	with open('evaluation.old.txt', encoding='utf-8', mode='rt') as old_data_file:
# 		with open('evaluation.txt', encoding='utf-8', mode='wt') as new_data_file:
# 			for line in old_data_file:
# 				parts = line.strip().replace(' ', '').split('\t')
# 				new_line = ''
# 				for part in parts:
# 					new_line = new_line + '\t' + ' '.join(part)
# 				new_line = new_line.strip()
# 				new_line = new_line + '\n'
# 				new_data_file.write(new_line)

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




if __name__ == '__main__':

    data_processor_evaluation()
    # create_vocabulary_dict()
    # data_processor_evaluation()
    # create_evaluation_set()