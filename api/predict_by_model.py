# text_classifier.py
import torch
from transformers import BertTokenizer, BertForSequenceClassification

def classify_text(sentence: str, model_name: str = "saved_bert_model", threshold: float = 0.5) -> int:
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=40)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)
    max_prob, predicted_label = torch.max(probs, dim=1)
    
    if max_prob.item() >= threshold:
        return predicted_label.item()
    else:
        return 39

