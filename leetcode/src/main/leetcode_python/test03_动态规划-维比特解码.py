# -*- coding: utf-8 -*-
# 从毕业之后一直到现在，我就没有更新我的知乎啦，主要是因为转行啦，现在在某公司做与自然语言处理有关的开发工作，之后的笔记大概率也都是与之有关，如果也有做与之有关工作的小伙伴，希望可以一起来交流学习呀，之前大部分小伙伴可能都是由于GEE而关注的，如果还有小伙伴遇到了GEE的问题，如果我还记得我还是会尽量解答的哈

# 以下通过一个分词的例子主要记录一下维比特解码 - crf我写不出来，维比特解码我总可以写出来吧

import numpy as np

# 转移概率，单纯用了等概率 >> b分词开始, e分词结束, m分词的中间,s仅仅单字分开

zy = {'be': 0.5,  # be 开始可以到结束
      'bm': 0.5,  # bm 开始到中间
      'eb': 0.5,  # em 结束可以到开始
      'es': 0.5,  # es 结束可以到仅仅单字
      'me': 0.5,  # me 中间可以到结束
      'mm': 0.5,  # mm 中间可以到中间
      'sb': 0.5,  # sb 仅仅单字到开始
      'ss': 0.5   # ss 仅仅单字到单字
      }

zy = {i: np.log(zy[i]) for i in zy.keys()}


def viterbi(nodes):
    paths = {'b': nodes[0]['b'], 's': nodes[0]['s']}
    for l in range(1, len(nodes)):
        paths_ = paths.copy()
        paths = {}
        for i in nodes[l].keys():
            nows = {}
            for j in paths_.keys():
                if j[-1] + i in zy.keys():
                    nows[j + i] = paths_[j] + nodes[l][i] + zy[j[-1] + i]
            k = np.argmax(list(nows.values()))
            paths[list(nows.keys())[k]] = list(nows.values())[k]
    return list(paths.keys())[np.argmax(list(paths.values()))]


''' # 搜索路径
{'b': -0.015575318, 's': -6.057363} # 开始只能是b和s开头
{'ss': -12.232245180559945, 'sb': -10.078559880559945, 'bm': -6.001635898559945, 'be': -0.7548268105599453} # 只能由b,s转移过来
{'bes': -1.8031197911198906, 'beb': -3.1734596911198905, 'bmm': -13.754842079119891, 'bme': -8.81519967911989} # 
{'bess': -2.793391871679836, 'besb': -3.930443871679836, 'bebm': -10.070449871679836, 'bebe': -7.958071871679836}
{'besss': -10.28113575223978, 'bessb': -3.5089358942397815, 'besbm': -9.212326652239781, 'besbe': -9.146066052239782}
{'besbes': -15.647376232799727, 'besbeb': -12.655429032799727, 'bessbm': -7.489156074799727, 'bessbe': -4.307664504799726}
{'bessbes': -5.027113643359672, 'bessbeb': -13.851752685359672, 'bessbmm': -18.539550255359668, 'bessbme': -11.840306155359672}
{'bessbess': -6.4368791839196176, 'bessbesb': -6.391419973919618, 'bessbebm': -22.522033665919615, 'bessbebe': -23.422544865919615}
{'bessbesss': -7.691225734479563, 'bessbessb': -13.506323364479563, 'bessbesbm': -13.615205854479564, 'bessbesbe': -7.937145494479563}
{'bessbessss': -9.722234715039509, 'bessbesssb': -8.695739685039507, 'bessbessbm': -19.816604145039506, 'bessbessbe': -20.702765945039506}
{'bessbesssss': -15.996908695599453, 'bessbessssb': -11.647404195599455, 'bessbesssbm': -9.937732865599452, 'bessbesssbe': -11.454922365599453} # 取最大的分数对应的路径
'''


s = '人们常说生活是一部教科书'  # "分词的文本"

# lstm >> Dense 预测得到的每个字的label的分数
nodes = [{'s': -6.057363, 'b': -0.015575318, 'm': -5.010491, 'e': -5.04824},
         {'s': -5.481735, 'b': -3.3280497, 'm': -5.2929134, 'e': -0.046104312},
         {'s': -0.3551458, 'b': -1.7254857, 'm': -7.060059, 'e': -2.1204166},
         {'s': -0.2971249, 'b': -1.4341769, 'm': -6.203843, 'e': -4.091465},
         {'s': -6.7945967, 'b': -0.022396842, 'm': -4.5887356, 'e': -4.522475},
         {'s': -5.808163, 'b': -2.8162158, 'm': -3.287073, 'e': -0.10558143},
         {'s': -0.026301958, 'b': -8.850941, 'm': -10.357247, 'e': -3.6580029},
         {'s': -0.71661836, 'b': -0.67115915, 'm': -7.9771338, 'e': -8.877645},
         {'s': -0.56119937, 'b': -6.376297, 'm': -6.5306387, 'e': -0.85257834},
         {'s': -1.3378618, 'b': -0.31136677, 'm': -5.6171336, 'e': -6.5032954},
         {'s': -5.5815268, 'b': -1.2320223, 'm': -0.548846, 'e': -2.0660355},
         {'s': -4.801048, 'b': -6.7394543, 'm': -2.2255623, 'e': -0.12511909}]

# 解码
t = viterbi(nodes)
print(t)  # bessbesssbme

# 规则进行分词得到结果
words = []
for i in range(len(s)):
    if t[i] in ['s', 'b']:
        words.append(s[i])
    else:
        words[-1] += s[i]
print(words)  # ['人们', '常', '说', '生活', '是', '一', '部', '教科书']

