import json

def main():
    with open('./mbpp.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = json.loads(line)

            with open('./output/MBPP-prompt/MBPP/' + str(line['task_id']) + '.py', 'w', encoding='utf-8') as fw:
                fw.write('\'\'\''+line['text']+ '\n')
                fw.write('\'\'\'\n'+ '\n')

                fw.write('\'\'\'\n')
                fw.write('Standard answer: \n')
                fw.write(line['code']+ '\n')
                fw.write('\'\'\'\n')

                test_list = line['test_list']
                for test_case in test_list:
                    fw.write(test_case+ '\n')

                challenge_test_list = line['challenge_test_list']
                for challenge_test_case in challenge_test_list:
                    fw.write(challenge_test_case+ '\n')

if __name__ == '__main__':
    main()