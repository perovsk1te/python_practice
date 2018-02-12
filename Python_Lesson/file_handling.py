"""
ファイルの操作
'w'書き換え
'a'書き加える
'r'読み込み
"""

f = open('test.txt', 'w')
f.write('test')
print('I', 'm', 'Print', file=f, sep='#', end='!')
f.close()

"""
with 勝手にclose()してくれる
"""

with open('test.txt', 'w') as f:
    f.write('test')

"""
line 行ごと
chunk 指定文字数ごと
"""
with open('test.txt', 'r') as f:
    #print(f.read)
    while True:
        chunk = 2
        line = f.read(line)
        chunk = f.read(chunk)
        print(line, end='')
        if not line:
            break


