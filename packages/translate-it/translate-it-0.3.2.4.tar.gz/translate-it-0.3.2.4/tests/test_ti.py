import pytest

from translate_it.dictionaries.youdao import translate


@pytest.mark.parametrize('keyword,result', (
    ('你好', ['hello;hello; hi; how do you do']),
    ('word', ['n. [语] 单词；话语；消息；诺言；命令',
              'vt. 用言辞表达',
              'n. (Word)人名；(英)沃德']),
    ('fill up', ['填补；装满；堵塞'])
))
def test_translate_it(keyword, result):
    rel_result = translate(keyword)
    assert 'contents' in rel_result.keys()
    assert 'examples' in rel_result.keys()
    assert 'additionals' in rel_result.keys()

    assert rel_result.get('contents') == result
