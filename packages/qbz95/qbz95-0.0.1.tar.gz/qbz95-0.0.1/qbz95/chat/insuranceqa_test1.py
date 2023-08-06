import insuranceqa_data as insuranceqa

train_data = insuranceqa.load_pool_train()
# test_data = insuranceqa.load_pool_test()
# valid_data = insuranceqa.load_pool_valid()
answers_data = insuranceqa.load_pool_answers()

lines = []
with open('insuranceqa.json', 'w') as f:
    for i in range(len(train_data)):
        # print('-------------------------------------------------')
        x = train_data[str(i)]
        question = x['zh']
        answers = x['answers']
        # print("question={}, answers={}".format(question, answers))
        answer = answers_data[answers[0]]['zh']
        line = '"question_id":{0},"question":"{1}","answer":"{2}"'.format(i, question, answer)
        lines.append('{"index":{}}' + '\n{' + line + '}\n')
    content = "".join(lines)
    f.write(content)

# for i in range(1):
#     print('-------------------------------------------------')
#     x = answers_data[str(26078)]
#     print(x)

# valid_data, test_data and train_data share the same properties
# for x in train_data:
#     print('index %s value: %s ++$++ %s ++$++ %s' % \
#           (x, d[x]['zh'], d[x]['en'], d[x]['answers'], d[x]['negatives']))


# print(answers_data)
# for x in answers_data:
#     print('index %s: %s ++$++ %s' % (x, d[x]['zh'], d[x]['en']))