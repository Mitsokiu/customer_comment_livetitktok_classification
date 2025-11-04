Comment Classification Model
1) Overview

Notebook xây dựng mô hình phân loại comment tiếng Việt từ livestream / social commerce.
Mục tiêu: tự động nhận diện loại comment để phục vụ automation trong hệ thống bán hàng.

2) Dataset

file nguồn: livestream_comments_1000.csv

dữ liệu gồm 2 cột chính: comment và labels

dạng comment ngắn, tự nhiên, nhiều biến thể ngôn ngữ

preprocessing đã áp dụng:

lowercase

remove url

remove digit

remove punctuation

strip whitespace

3) Model Approach

sử dụng HuggingFace Transformer model (pretrained base model)

fine-tune classification head trên dataset tiếng Việt

training end-to-end với HF Trainer

Lý do chọn approach này: mô hình pretrained hiểu ngữ cảnh tiếng Việt tốt hơn các phương pháp TF-IDF truyền thống.

4) Training Process

chia train / validation

optimize bằng cross entropy

lưu id2label và label2id để dùng cho inference sau này

5) Evaluation Result (Epoch 3)
Metric	Value
Loss	1.11398
Accuracy	0.955
F1 Macro	0.9551
F1 Weighted	0.95537
Runtime	196.11 sec
6) Notebook Structure

Load & Clean Data

EDA đơn giản

Load Tokenizer + Model HF

Train Model

Evaluate

Save mapping label

Inference kiểm tra với câu thực tế
