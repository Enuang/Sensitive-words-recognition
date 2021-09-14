# -*- coding:utf-8 -*-
import sys
import pypinyin
import init


# word_path = 'D:/MyCode/Sensitive_words_recognition/031902305/test/words.txt'
# org_path = 'D:/MyCode/Sensitive_words_recognition/031902305/test/org.txt'
# ans_path = 'D:/MyCode/Sensitive_words_recognition/031902305/test/ans.txt'


class DFA(object):
    def __init__(self, sensitive_word):
        # sensitive_word:敏感词库
        # ignore_word:无意义词库
        self.root = dict()
        self.ignore_word = [' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                            '[', ']', ';', ':', '"', ',', '<', '>', '.', '/', '?',
                            '{', '}', '`', '-', '_', '+', '=', '|', '\\', '\'',
                            '？', '、', '。', '，', '》', '《', '；', '：', '“', '‘',
                            '【', '】', '！', '￥', '…', '·', '~', '—',
                            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for word in sensitive_word.keys():
            self.add_word(word)

    def add_word(self, word):
        # 添加词库
        node = self.root
        for i in range(len(word)):
            char = word[i]
            if char in node.keys():
                # 存在，赋值
                node = node.get(word[i])
                if node['end']:  # 已存在如falung，添加falungong的后续节点
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

    def check_pinyin(self, word, node):  # 查找字符的拼音，返回节点
        for char in word:
            if char not in node:
                return False, node
            else:
                node = node[char]
        return True, node

    def check_word(self, txt, begin_index, end_index, node, res):
        if node.get('end'):
            res.append(end_index - begin_index)  # 将得到的包含特殊字符的敏感词长度返回
        while end_index + 1 < len(txt) and txt[end_index] in self.ignore_word:  # 忽略特殊字符
            if node == self.root:
                return res
            end_index += 1
        if end_index > len(txt) - 1:
            return res
        word = txt[end_index]
        if word in init.chaizi and word in node:  # 递归找当前偏旁、拼音
            self.check_word(txt, begin_index, end_index + 1, node[word], res)
        word = pypinyin.lazy_pinyin(word)[0].lower()
        flag, node = self.check_pinyin(word, node)
        if flag:
            self.check_word(txt, begin_index, end_index + 1, node, res)
        return res

    def find_right(self, word, index, str1, ans):  # 递归找匹配的原敏感词
        if word in sw:
            ans = word
            return ans
        if str1 in sw:
            ans = str1
            return ans
        for i in range(index, len(word)):
            if 'a' <= word[i] <= 'z':
                str1 += word[i]
                continue
            else:
                ans = self.find_right(word, i + 1, str1 + word[i], ans)
                ans = self.find_right(word, i + 1, str1 + (pypinyin.lazy_pinyin(word[i])[0]), ans)
                if ans != '':
                    break
        return ans

    def get_word(self, txt):
        # 获取匹配到的词语
        matched_word = list()
        right_word = list()
        for i in range(len(txt)):
            node = self.root
            lengthList = self.check_word(txt, i, i, node, [])
            if lengthList:
                lengthList.sort()
                length = lengthList[-1]
                if length > 0:
                    flag = False  # 判断无意义字符是否为数字
                    word = txt[i:i + int(length)]
                    matched_word.append(word)  # 获取匹配到的词
                    for j in word:
                        if j in self.ignore_word:
                            word = word.replace(j, '')
                            if '0' <= j <= '9':
                                flag = True
                        if 'A' <= j <= 'Z':
                            # 去除无意义字符，大写转小写
                            word = word.replace(j, j.lower())
                    str1 = str()
                    for j in word:
                        if j in init.chaizi:
                            str1 += j
                        else:
                            str1 += pypinyin.lazy_pinyin(j)[0]
                    ans_word = self.find_right(str1, 0, '', '')
                    right_word.append(sw[ans_word])
                    if flag and init.is_chinese(sw[ans_word]):  # 中文加数字不算敏感词，剔除
                        matched_word.pop()
                        right_word.pop()
        return matched_word, right_word


if __name__ == '__main__':

    word_path = sys.argv[1]
    org_path = sys.argv[2]
    ans_path = sys.argv[3]

    sw = open(word_path, encoding='utf-8').readlines()
    org = open(org_path, encoding='utf-8').readlines()
    ans_file = open(ans_path, 'w', encoding='utf-8')

    sw = init.new_swd(sw)  # 返回字典 {各类变形敏感词：原敏感词}
    dfa = DFA(sensitive_word=sw)

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

    # for i in ans:
    #    print(i)
    for i in ans:
        ans_file.write(i + '\n')
    ans_file.close()
