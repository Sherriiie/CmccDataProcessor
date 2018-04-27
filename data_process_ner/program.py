from .NER import EntityLabelCmcc

if __name__ == '__main__':
    print('============== main entrance for program.py')
    print ("we are in %s"%__name__)
    file_path = 'test.txt'
    entity_labeller = EntityLabelCmcc.label_price(file_path)