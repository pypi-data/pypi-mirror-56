import insuranceqa_data as insuranceqa
import os

# train_data = insuranceqa.load_pairs_train()
test_data = insuranceqa.load_pairs_test()
# valid_data = insuranceqa.load_pairs_valid()

train_data = insuranceqa.load_pool_train()
print(train_data)

vocab_data = insuranceqa.load_pairs_vocab()
print(vocab_data['word2id']['UNKNOWN'])
word = vocab_data['id2word']['10']
print(word)
print(vocab_data['tf'][word])
print(vocab_data['total'])
print(test_data[0])
print(test_data[1])


def ids_to_sentence(ids, id2word):
    words = [id2word[str(id)] for id in ids]
    sentence = ''.join(words)
    return sentence


for i in range(20):
    x = test_data[i]
    question_ids = x['question']
    utterance_ids = x['utterance']
    question = ids_to_sentence(question_ids, vocab_data['id2word'])
    utterance = ids_to_sentence(utterance_ids, vocab_data['id2word'])

    # print(x)
    print('question_ids: %s \nquestion: %s \nutterance: %s' % (question_ids, question, utterance))
    print('-------------------------------------------------')

# valid_data, test_data and train_data share the same properties
# for x in test_data:
#     print('index %s value: %s ++$++ %s ++$++ %s' % \
#      (x['qid'], x['question'], x['utterance'], x['label']))

# vocab_data = insuranceqa.load_pairs_vocab()
# vocab_data['word2id']['UNKNOWN']
# vocab_data['id2word'][0]
# vocab_data['tf']
# vocab_data['total']