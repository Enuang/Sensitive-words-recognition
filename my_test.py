import unittest

import init
import main


class MyTestCase(unittest.TestCase):
    def test_swd(self):
        word=['秋天']
        ans = dict({'qt': '秋天', 'qtian': '秋天', 'qiut': '秋天', 'qiutian': '秋天', '禾火t': '秋天', '禾火tian': '秋天'})
        result = init.new_swd(word)
        self.assertEqual(result,ans)

    def test_get_word(self):
        word=['全球总决赛','规模']
        org=['我们决定在冰岛雷克雅未克举办2021全!球总^jue赛。\n',
             '这场今年最大gu!i&模，最顶级的电子竞技全$王_求z决sai将于10月5日正式开幕\n',
             '并于11月6日举行顶级 规%m_ 的冠亚军决赛。']
        ans=['Line1: <全球总决赛> 全!球总^jue赛', 'Line2: <规模> gu!i&模', 'Line2: <全球总决赛> 全$王_求z决sai', 'Line3: <规模> 规%m']
        sw=init.new_swd(word)
        dfa=main.DFA(sensitive_word=sw)
        result = list()
        for i in org:
            match, right = dfa.get_word(i)
            if match and right:
                num = org.index(i)
                for j in match:
                    ind = match.index(j)
                    result.append('Line' + str(num + 1) + ': ' + '<' + right[ind] + '> ' + match[ind])
        self.assertEqual(result, ans)

if __name__ == '__main__':
    unittest.main()
