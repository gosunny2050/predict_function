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
#def load_data_from_file_bak(file_path):
    #data = pd.read_csv(file_path)  # 假设文件是 CSV 格式
    #texts = data.iloc[:, 0].tolist()  # 提取第一列作为文本列
    #labels = data.iloc[:, 1].astype(int).tolist()  # 提取第二列作为标签列
    #return texts, labels

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
file_path = 'train_data.csv'  # 替换为你的数据集路径
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

# 加载预训练模型和分词器
#model_name = "bert-base-chinese"
#tokenizer = BertTokenizer.from_pretrained(model_name)
#model = BertForSequenceClassification.from_pretrained(model_name, num_labels=39)  # 39分类任务
# 从本地路径加载分词器和模型
tokenizer = BertTokenizer.from_pretrained("./models/bert-base-chinese")
model = BertForSequenceClassification.from_pretrained("./models/bert-base-chinese", num_labels=39)

# 创建数据集
train_dataset = TextDataset(train_texts, train_labels, tokenizer, max_length=64)  # 设置较小的 max_length 来减少内存使用
val_dataset = TextDataset(val_texts, val_labels, tokenizer, max_length=64)

# 使用 DataLoader 加载数据，减小 batch_size 来减少内存占用
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)  # 减小 batch_size 来防止内存溢出
val_loader = DataLoader(val_dataset, batch_size=32)

# 设置设备为CPU
device = torch.device("cpu")
model.to(device)

# 定义优化器和学习率调度器
optimizer = AdamW(model.parameters(), lr=2e-5)
num_epochs = 5  # 设置较少的 epoch 数来快速测试
num_training_steps = num_epochs * len(train_loader)
lr_scheduler = get_scheduler(
    name="linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps
)

# 训练模型
for epoch in range(num_epochs):
    print(f"Epoch {epoch + 1}/{num_epochs}")
    epoch_progress = tqdm(train_loader, desc=f"Training Epoch {epoch + 1}", leave=False)
    model.train()
    total_loss = 0  # 记录本轮的总损失

    for batch in epoch_progress:
        inputs, labels = batch
        inputs = {k: v.to(device) for k, v in inputs.items()}
        labels = labels.to(device)

        outputs = model(**inputs, labels=labels)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()

        total_loss += loss.item()
        epoch_progress.set_postfix({"Batch Loss": loss.item()})  # 更新进度条上的损失信息

    avg_epoch_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch + 1} finished. Average Loss: {avg_epoch_loss:.4f}")

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

# 保存模型
model.save_pretrained("./saved_bert_model")
tokenizer.save_pretrained("./saved_bert_model")

