# encoding=utf8

toneDict = {
        u'ā': 'a',
        u'á': 'a',
        u'ǎ': 'a',
        u'à': 'a',
        u'ō': 'o',
        u'ó': 'o',
        u'ǒ': 'o',
        u'ò': 'o',
        u'ē': 'e',
        u'é': 'e',
        u'ě': 'e',
        u'è': 'e',
        u'ī': 'i',
        u'í': 'i',
        u'ǐ': 'i',
        u'ì': 'i',
        u'ū': 'u',
        u'ú': 'u',
        u'ǔ': 'u',
        u'ù': 'u',
        u'ǖ': 'v',
        u'ǘ': 'v',
        u'ǚ': 'v',
        u'ǜ': 'v',
        u'ü': 'v',
        u'ń': 'n',
        u'ň': 'n',
        u'ǹ': 'n',
        u'ẑ': 'z',
        u'ĉ': 'c',
        u'ŝ': 's',
        u'ɡ': 'g',
        u'ɑ': 'a'}
class RemovePinyinTones:
    @staticmethod
    def remove(py):
        """
        替换拼音声调
        :param py:
        :return:
        """
        ret = ''
        for p in py:
            ret += toneDict.get(p, p)
        if ret not in ['lv', 'nv']:
            ret = ret.replace('v', 'u')
        return ret

