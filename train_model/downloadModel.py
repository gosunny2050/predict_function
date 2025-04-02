from transformers import BertTokenizer, BertModel

# 设置模型名称和下载路径
model_name = "bert-base-chinese"
save_directory = "./models/bert-base-chinese"

# 下载并保存 Tokenizer 和模型
tokenizer = BertTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

model = BertModel.from_pretrained(model_name)
model.save_pretrained(save_directory)

