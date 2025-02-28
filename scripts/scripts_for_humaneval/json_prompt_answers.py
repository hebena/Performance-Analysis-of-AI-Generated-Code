
import json


def main():
    with open('./human-eval-v2-20210705.jsonl', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            line = json.loads(line)

            with open('./output/Humaneval-prompt1/' + line['task_id'] + '.py', 'w', encoding='utf-8') as fw:
                fw.write(line['prompt'])

                fw.write('\'\'\'\n')
                fw.write('Standard answer: \n')
                fw.write(line['canonical_solution'])
                fw.write('\'\'\'\n')

                fw.write(line['test'])

                fw.write('check(' + line['entry_point'] + ')\n')


if __name__ == '__main__':
    main()