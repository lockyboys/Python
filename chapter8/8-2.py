import re
p = re.compile('ab*')
print(p)

import re
p = re.compile('[a-z]+')
'''
이제 이 패턴 객체로 앞에 나온 메서드를 사용하는 간단한 예를 살펴보자.

match
match 메서드는 문자열의 처음부터 정규식과 매치되는지 조사한다. 즉, 패턴이 문자열의 시작 위치(인덱스 0)에서 바로 매치되어야 한다. 앞 패턴에 match 메서드를 수행해 보자.
'''
m = p.search("3 python")
print(m)
# <re.Match object; span=(0, 6), match='python'>
# "python" 문자열은 [a-z]+ 정규식에 부합되므로 match 객체가 반환된다.

m = p.match("3 python")
print(m)
# None

result = p.findall("life is too short")
print(result)

result = p.finditer("life is too short")
print(result)
# <callable_iterator object at 0x01F5E390>
for r in result:
    print(r)

import re
p = re.compile('[ a-z]+')

# m = p.match("python") # search
m = p.match("  pytho n")
print(m.group())
# 'python'
print(m.start())
# 0
print(m.end())
# 6
print(m.span())
# (0, 6)