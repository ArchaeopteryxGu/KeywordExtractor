# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:57:34 2025

@author: Archaeopteryx
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:17:11 2024

@author: Archaeopteryx
"""
import torch
from ltp import LTP
from ltp import StnSplit
import re
import os
import pandas as pd
#import string

ltp = LTP(input("请输入模型路径："))  # 替换为实际的LTP模型路径

if torch.cuda.is_available():
    ltp.to("cuda")

folder_path = input("请指定目标文件夹路径：")
files = os.listdir(folder_path)

selected_sentences = []

keyword = input("请输入关键字：")
POS = input("请问希望筛选的关键词词性是（输入None代表不指定关键词词性）：")


for file in files:
    with open(folder_path + file, "r", encoding="UTF-8") as text_file:
        para = text_file.read().replace("\r", "").replace("\n", "")
        check = re.compile("[^\u4e00-\u9fa5^\
        ！？。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】\
        〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏.^\.^0-9]")
        content = re.sub(check,'',para)
        sentences = StnSplit().split(content)

        # 定义关键词
        pattern = re.compile(r"{}".format(re.escape(keyword)), flags=re.IGNORECASE)
        
        # 提取句子中包含关键词的部分
        for sent in sentences:
            if pattern.search(sent):
                # 使用LTP进行分词和标注
                output = ltp.pipeline([sent], tasks=["cws", "pos"])
                
                if output.cws and len(output.cws[0]) > 0:
                    for idx, word in enumerate(output.cws[0]):
                        if pattern.search(word):
                                # 获取词性信息
                            word_pos = output.pos[0][idx]
                            if POS == "None":
                                selected_sentences.append({
                                        'sentence': sent,
                                        'keyword': [word],
                                        'keyword_idx': [idx],
                                        'keyword_pos': word_pos  # 新增的字段，存储关键词的词性
                                    })
                            else:
                                if word_pos == POS:
                                    selected_sentences.append({
                                            'sentence': sent,
                                            'keyword': [word],
                                            'keyword_idx': [idx],
                                            'keyword_pos': word_pos  # 新增的字段，存储关键词的词性
                                        })
              
selected_sentences = pd.DataFrame(selected_sentences)
result = selected_sentences

# 替换以下路径为实际需要处理的文件路径和保存位置
save_file = input("将文件保存在：")

result.to_excel(save_file,sheet_name='Output',index=False)

#with open(save_file, 'w', encoding='utf-8') as f:
    #import json
    #json.dump(result, f, ensure_ascii=False, indent=2)