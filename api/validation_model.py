import torch
from transformers import BertTokenizer, BertForSequenceClassification

# 1. 加载预训练的BERT模型和分词器
model_name = 'saved_bert_model'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=40)  # 假设有39个分类

# 检查是否有GPU，并将模型加载到设备（CPU或GPU）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 设定阈值
threshold = 0.5  # 分类阈值

# 2. 定义一个分类函数
def classify_sentence(sentence):
    # 对输入句子进行分词并转化为模型可接受的格式
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # 进行模型推理（分类）
    model.eval()  # 切换到评估模式
    with torch.no_grad():
        outputs = model(**inputs)

    # 获取分类结果
    logits = outputs.logits  # 模型输出的logits
    probs = torch.softmax(logits, dim=1)  # 转换为概率
    max_prob, predicted_label = torch.max(probs, dim=1)  # 获取最大概率和对应的标签

    if max_prob.item() >= threshold:
        return predicted_label.item(), max_prob.item()
    else:
        return None, None  # 信心低时返回None

# 3. 从文件读取输入，并保存输出
input_file = "validation.txt"  # 输入文件路径
output_file = "output_predictions.txt"  # 输出文件路径

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        sentence = line.strip()  # 去除前后空白字符
        if not sentence:
            continue  # 跳过空行

        # 调用分类函数
        label, confidence = classify_sentence(sentence)
        
        if label is not None:
            result = f"Sentence: {sentence}\nPredicted Label: {label}, Confidence: {confidence:.4f}\n\n"
        else:
            result = f"Sentence: {sentence}\nPrediction confidence is too low.\n\n"
        
        # 输出结果到终端
        print(result)
        # 写入输出文件
        outfile.write(result)

