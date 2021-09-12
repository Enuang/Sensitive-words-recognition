# -*- coding:utf-8 -*-
import sys
import pypinyin
import init

org_path = 'D:/MyCode/Sensitive words recognition/test/org.txt'
word_path = 'D:/MyCode/Sensitive words recognition/test/words.txt'
ans_path = 'D:/MyCode/Sensitive words recognition/ans.txt'


class DFA(object):

    def __init__(self, sensitive_word):
        # sensitive_word:敏感词库
        # ignore_word:无意义词库

        self.root = dict()
        self.ignore_word = [' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                            '[', ']', ';', ':', '"', ',', '<', '>', '.', '/', '?',
                            '{', '}', '`', '-', '_', '+', '=', '|', '\\', '\'',
                            '？', '、', '。', '，', '》', '《', '；', '：', '“', '‘',
                            '【', '】', '！', '￥', '…', '·', '~',
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for word in sensitive_word.keys():
            self.add_word(word)

    def add_word(self, word):
        # 添加词库

        node = self.root
        for i in range(len(word)):
            char = word[i]
            if char in node.keys():
                # 存在，直接赋值
                node = node.get(word[i])
                if node['end']:
                    new_node = dict()
                    if i == len(word) - 1:  # 最后一个
                        new_node['end'] = True
                    else:  # 不是最后一个
                        new_node['end'] = False
                else:
                    node['end'] = False
            else:
                # 不存在，构建dict
                new_node = dict()

                if i == len(word) - 1:  # 最后一个
                    new_node['end'] = True
                else:  # 不是最后一个
                    new_node['end'] = False

                node[char] = new_node
                node = new_node

    def check_word(self, txt, begin_index):
        # 检查文字中是否包含匹配的字符
        # begin_index: 起始下标
        # txt:待检测的文本
        # return:存在，返回敏感词长度，不存在返回0

        flag = False
        node = self.root
        tmp_length = 0  # 包括特殊字符的敏感词的长度
        spare = 0

        for i in range(begin_index, len(txt)):
            words = txt[i]

            word_pinyin = pypinyin.lazy_pinyin(words)
            spare += len(word_pinyin[0]) - 1

            for word in word_pinyin[0]:
                lword = word.lower()
                # 检测是否是特殊字符
                if lword in self.ignore_word and tmp_length > 0:
                    tmp_length += 1
                    continue
                # 获取指定key
                node = node.get(lword)
                if node:  # 存在
                    tmp_length += 1
                    if node.get("end"):  # 判断是否为最后一个
                        if word_pinyin[0].index(word) != len(word_pinyin[0])-1:
                            else_word = word_pinyin[0][word_pinyin[0].index(word)+1]
                            node1 = node.get(else_word)
                            if node1 and (node1.get('end') == False):
                                continue
                        if i != len(txt) - 1:
                            else_word = txt[i + 1]
                            node1 = node.get(else_word)
                            if node1 and (node1.get('end') == False):
                                continue
                        flag = True
                        break
                else:  # 不存在，返回0
                    return 0
            if tmp_length - spare > 0 and flag:
                return tmp_length - spare
        return 0

    def get_word(self, txt):
        # 获取匹配到的词语
        matched_word = list()
        right_word = list()
        for i in range(len(txt)):
            length = self.check_word(txt, i)
            if length > 0:
                word = txt[i:i + length]
                matched_word.append(word)
                for j in word:
                    if j in self.ignore_word:
                        word = word.replace(j, '')
                    if 'A' <= j <= 'Z':
                        word = word.replace(j, j.lower())
                str1 = "".join(pypinyin.lazy_pinyin(word))
                right_word.append(sw[str1])
        return matched_word, right_word


if __name__ == '__main__':
    # word_file = open(sys.argv[1], encoding='UTF-8').readlines()
    # sw = init.new_swd(word_file)
    # org_file = open(sys.argv[2], encoding='UTF-8').readlines()

    sw = open(word_path, encoding='utf-8').readlines()
    sw = init.new_swd(sw)
    org = open(org_path, encoding='utf-8').readlines()

    dfa = DFA(sensitive_word=sw)

    #for i in org:
     #   match, right = dfa.get_word(i)
      #  print(match)
       # print(right)

    # ans_file = open(sys.argv[3], 'w', encoding='UTF-8')

    ans_file = open(ans_path, 'w', encoding='utf-8')
    ans = list()
    total = 0
    for i in org:
        match, right = dfa.get_word(i)
        if match and right:
            num = org.index(i)
            for j in match:
                ind = match.index(j)
                ans.append('Line' + str(num + 1) + ': ' + '<' + right[ind] + '> ' + match[ind])
                total += 1
    ans.insert(0, 'Total: ' + str(total))
    for i in ans:
        ans_file.write(i + '\n')
    ans_file.close() 

