import pypinyin


def is_chinese(uchar):
    # 判断一个unicode是否是汉字
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def AC(step, length, word, st, result):
    if step == length:
        result.append(st)
        return
    else:
        for i in word[step]:
            AC(step + 1, length, word, st + i, result)
    return result


def new_swd(swd):
    for line in swd:
        swd[swd.index(line)] = line.strip('\n')
    sens = list()
    for word in swd:
        if is_chinese(word):
            tmp = pypinyin.lazy_pinyin(word)
            tmp3 = list()
            for i in tmp:
                tmp2 = list()
                tmp2.append(word[tmp.index(i)]) #添加原文
                tmp2.append(i[0]) #添加小写字母
                tmp2.append(i[0].upper()) #添加大写字母
                tmp2.append(i) #添加拼音
                tmp3.append(tmp2)
            sens.append(tmp3)
        else:
            tmp3 = list()
            for i in word:
                if 'A' <= i <= 'Z':
                    tmp2 = list()
                    tmp2.append(i)
                    tmp2.append(i.lower())
                    tmp3.append(tmp2)
                elif 'a' <= i <= 'z':
                    tmp2 = list()
                    tmp2.append(i)
                    tmp2.append(i.upper())
                    tmp3.append(tmp2)
            sens.append(tmp3)

    sensitive_word = dict()
    for word in sens:
        result = AC(0, len(word), word, '', [])
        #print(result)
        for i in result:
            sensitive_word[i] = result[0]
    return sensitive_word

