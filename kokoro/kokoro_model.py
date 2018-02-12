"""
単語のベクトル化
"""

from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import re

"""
データの読み込み、余分な部分の切り取り
"""
binarydata = open("kokoro.txt", "rb").read()
text = binarydata.decode("shift_jis")
text = re.split(r'\-{5,}', text)[2]
text = re.split(r'底本:', text)[0]
text = text.strip()

"""
トークン化
行ごとに取り出してトークンに切り分ける
名詞、形容詞、動詞、記号のみ取り出す
つなぎなおしてデータを生成
"""

t = Tokenizer()
result = []
lines = text.split("\r\n")


for line in lines:
    s = line
    s = s.replace('|', '')
    s = re.sub(r"《.+?》", '', s)
    s = re.sub(r"［＃.+?］", '', s)
    tokens = t.tokenize(s)
    r = []
    for token in tokens:
        if token.base_form == "*":
            w = token.surface
        else:
            w = token.base_form
        ps = token.part_of_speech
        hinshi = ps.split(',')[0]
        if hinshi in ['名詞', '形容詞', '動詞', '記号']:
            r.append(w)
    rl = (" ".join(r)).strip()
    result.append(rl)
    print(rl)

wakachigaki_file = "kokoro.wakachi"
with open(wakachigaki_file, "w", encoding="utf-8") as fp:
    fp.write("\n".join(result))

"""
ベクトル化して保存
"""
data = word2vec.LineSentence(wakachigaki_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
model.save("kokoro.model")
print("completed")

