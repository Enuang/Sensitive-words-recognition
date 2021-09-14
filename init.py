import pypinyin
import json

json_path = 'chai_zi.json'
chaizi = list()


def is_chinese(uchar):
    # 判断一个字符是否是汉字
    for i in uchar:
        if u'\u4e00' <= i <= u'\u9fa5':
            continue
        else:
            return False
    return True


def AC(step, length, word, st, result):
    # 递归，建立各类敏感词的变形形式
    if step == length:
        result.append(st)
        return
    else:
        for i in range(len(word[step])):
            if i != 0:
                AC(step + 1, length, word, st + word[step][i], result)
    return result


def new_swd(swd):
    f = open(json_path, 'r', encoding='utf-8')
    split_char = json.load(f)
    f.close()
    for line in swd:
        swd[swd.index(line)] = line.strip('\n')
    sens = list()  # 三元组
    for word in swd:  # eg: word='法轮功'
        if is_chinese(word):  # 汉字
            tmp3 = list()
            tmp_pinyin = pypinyin.lazy_pinyin(word)
            # eg:tmp_pinyin=['fa','lun','gong]
            for i in tmp_pinyin:
                tmp2 = list()  # eg: tmp2=[轮,l,lun,[车,仑]]
                tmp2.append(word[tmp_pinyin.index(i)])  # 添加原文
                tmp2.append(i[0])  # 添加小写字母
                tmp2.append(i)  # 添加拼音
                if word[tmp_pinyin.index(i)] in split_char.keys():
                    tmp_chaizi = split_char[word[tmp_pinyin.index(i)]]
                    tmp2.append(tmp_chaizi)
                    for j in tmp_chaizi:
                        if j not in chaizi:
                            chaizi.append(j)
                tmp3.append(tmp2)
            sens.append(tmp3)
        else:  # 字母
            tmp3 = list()
            for i in word:
                if 'A' <= i <= 'Z':
                    tmp2 = list()
                    tmp2.append(i)  # 原文
                    tmp2.append(i.lower())  # 小写
                    tmp3.append(tmp2)
                elif 'a' <= i <= 'z':
                    tmp2 = list()
                    tmp2.append(i)
                    tmp2.append(i)
                    tmp3.append(tmp2)
            sens.append(tmp3)
    #print(sens)
    sensitive_word = dict()
    for word in sens:
        result = AC(0, len(word), word, '', [])
        #print(result)
        org_word = str()
        for j in word:
            org_word += j[0]
        for i in result:
            sensitive_word[i] = org_word  # {各类变形敏感词：原敏感词}
    #print(sensitive_word)
    return sensitive_word
