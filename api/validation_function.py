#import pandas as pd
import csv
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification, AdamW, get_scheduler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import random
from tqdm.auto import tqdm

# 设置随机种子以确保结果一致
def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

set_seed(42)


# 从CSV文件加载数据
def load_data_from_file(file_path):
    texts = []
    labels = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        #next(csvreader)  # 跳过表头（如果有）
        for row in csvreader:
            # 假设第一列是文本，第二列是标签
            texts.append(row[0])
            try:
                labels.append(int(row[1]))  # 确保标签是整数
            except ValueError:
                labels.append(-1)  # 如果标签无法转换为整数，使用 -1（或者其他值）作为标记
    return texts, labels
# 加载文本和标签
#file_path = 'train_data.csv'  # 替换为你的数据集路径
file_path = 'validation.csv'
texts, labels = load_data_from_file(file_path)

# 切分训练集和验证集
train_texts, val_texts, train_labels, val_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# 定义自定义数据集
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        
        # 分词和编码
        encoding = self.tokenizer(text, truncation=True, padding='max_length', max_length=self.max_length, return_tensors='pt')
        
        # 返回input_ids, attention_mask 和 label
        return {key: val.squeeze(0) for key, val in encoding.items()}, torch.tensor(label, dtype=torch.long)

# 从本地路径加载分词器和模型
tokenizer = BertTokenizer.from_pretrained("saved_bert_model")
model = BertForSequenceClassification.from_pretrained("saved_bert_model", num_labels=40)

# 创建数据集
train_dataset = TextDataset(train_texts, train_labels, tokenizer, max_length=64)  # 设置较小的 max_length 来减少内存使用
val_dataset = TextDataset(val_texts, val_labels, tokenizer, max_length=64)

# 使用 DataLoader 加载数据，减小 batch_size 来减少内存占用
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)  # 减小 batch_size 来防止内存溢出
val_loader = DataLoader(val_dataset, batch_size=32)

# 设置设备为CPU
device = torch.device("cpu")
model.to(device)


# 验证模型
model.eval()
val_labels_list = []
val_preds_list = []

with torch.no_grad():
    for batch in val_loader:
        inputs, labels = batch
        inputs = {k: v.to(device) for k, v in inputs.items()}
        labels = labels.to(device)

        outputs = model(**inputs)
        logits = outputs.logits

        predictions = torch.argmax(logits, dim=-1)
        val_preds_list.extend(predictions.cpu().numpy())
        val_labels_list.extend(labels.cpu().numpy())

# 计算验证集上的准确率
accuracy = accuracy_score(val_labels_list, val_preds_list)
print(f"Validation Accuracy: {accuracy:.4f}")


