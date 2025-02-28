import os

def test(fpath,output_file):
    bad_file = 0
    good_file = 0

    files = sorted(os.listdir(fpath))
    for file in files:
        file_path = os.path.join(fpath, file)
        result = os.system('python3 ' + file_path)

        if result == 0:
            good_file += 1
            print('[{}] ran successfully'.format(file))
        else:
            bad_file += 1
            print('[{}] failed to run'.format(file))

    print('The number of successful runs is [{}], and the number of failed runs is [{}].'.format(good_file, bad_file))

test(r'./output/Answers/MBPP/',r'./output/run/MBPP/result.txt')
