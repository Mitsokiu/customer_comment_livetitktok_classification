from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_path ="./models/my_model"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)


# print("Số nhãn:", model.config.num_labels)
# print("Mapping id2label:", model.config.id2label)
# print("Mapping label2id:", model.config.label2id)

# 0: 'Spam / Không liên quan', 1: 'Khen ngợi / Tương tác tích cực',
# 2: 'Hỏi thông tin sản phẩm', 3: 'Khẩn cấp / Cần phản hồi nhanh',
# 4: 'Hỏi vận chuyển / Thanh toán', 5: 'Hỏi giá', 6: 'Phàn nàn / Tiêu cực', 
# 7: 'Chốt đơn / Mua hàng'

def predict(text):
    inputs = tokenizer(text,return_tensors="pt",padding=True,truncation=True )
    with torch.no_grad():
       outputs = model(**inputs)
       pred_id = torch.argmax(outputs.logits, dim=1).item()
    return pred_id
