import os
import re
import argparse
from ltp import LTP


def print_process(process):
    num_processed = int(30 * process)
    num_unprocessed = 30 - num_processed
    print(
        f"{''.join(['['] + ['='] * num_processed + ['>'] + [' '] * num_unprocessed + [']'])}, {(process * 100):.2f} %")


def get_sdp(list_word):
    seg, hidden = ltp.seg(list_word)
    sdp = ltp.sdp(hidden, mode='tree')
    return sdp[0]


def convert_to_sdp(source_dir, target_path, log=False):
    print("Converting.. .")
    for root, dirs, files in os.walk(source_dir):
        total = len(files)
        tgt_dir = target_path + root[len(source_dir):]
        for index, name in enumerate(files):
            file = os.path.join(root, name)
            dict_file = process_file(file)
            _save_bises(dict_file, tgt_dir)
            if log:
                print_process((index + 1) / total)
    return 0


def process_file(file):
    with open(file, 'r', encoding='UTF-8') as f:
        text = f.readlines()
        new_line = []
        for line in text:
            b = re.sub('[(](.*?)[)],', ' ', line)
            b = re.sub(r'\n', '', b)
            a = re.sub(' ', '', b)
            sdp = get_sdp([a])
            p1 = re.compile(r'[(](.*?)[)]', re.S)
            cx = re.findall(p1, line)
            temp_line = [a, b, sdp, cx]
            new_line.append(temp_line)

    return new_line


def _save_bises(bises, path, write_mode='a+'):
    with open(path, mode=write_mode, encoding='UTF-8') as f:
        for bis in bises:
            print(bis)
            line, line_cixin, sdp, tag = bis[0], bis[1], bis[2], bis[3]
            f.write(line + "\t" + line_cixin + "\t" + str(sdp) + "\t" + str(tag))
            f.write('\n')


if __name__ == '__main__':
    ltp = LTP()
    MAX_LEN_SIZE = 150
    convert_to_sdp('../data/train', '../nre', log=True)

    # parser = argparse.ArgumentParser(description="将使用词性标注的文件转换为用BIS分块标记的文件。")
    # parser.add_argument("corups_dir", type=str, help="指定存放语料库的文件夹，程序将会递归查找目录下的文件。")
    # parser.add_argument("output_path", type=str, default='.', help="指定标记好的文件的输出路径。")
    # parser.add_argument("-c", "--combine", help="是否组装为一个文件", default=False, type=bool)
    # parser.add_argument("-s", "--single_line", help="是否为单行模式", default=False, type=bool)
    # parser.add_argument("--log", help="是否打印进度条", default=False, type=bool)
    # parser.add_argument("--max_len", help="处理后的最大语句长度（将原句子按标点符号断句，若断句后的长度仍比最大长度长，将忽略",
    #                     default=150, type=int)
    # args = parser.parse_args()
    # MAX_LEN_SIZE = args.max_len
    # convert_to_bis(args.corups_dir, args.output_path, args.log, args.combine, args.single_line)
