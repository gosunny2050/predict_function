# -*- coding: utf-8 -*-
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 1. 加载预训练的BERT模型和分词器
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=39)  # 假设有39个分类

# 检查是否有GPU，并将模型加载到设备（CPU或GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 2. 定义要分类的输入句子
sentence = "我想要预定一张去北京的机票。"  # 这里输入你需要识别的句子

# 3. 对输入句子进行分词并转化为模型可接受的格式
inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)

# 将输入数据移到对应的设备（CPU或GPU）
inputs = {key: value.to(device) for key, value in inputs.items()}

# 4. 进行模型推理（分类）
model.eval()  # 切换到评估模式
with torch.no_grad():
    outputs = model(**inputs)

# 5. 获取分类结果
logits = outputs.logits  # 模型输出的logits
predicted_label = torch.argmax(logits, dim=1).item()  # 获取预测的标签索引

# 输出结果
print(f"Predicted label: {predicted_label}")

