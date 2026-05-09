# sys1.py
import sys

sum = 0
args = sys.argv[1:]
for i in args:
    sum =sum +int(i)

print(sum)

# args = sys.argv[0:]
# for i in args:
    # print(i)