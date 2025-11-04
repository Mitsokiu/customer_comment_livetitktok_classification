Comment Classification Model
1) Overview

Notebook  xây dựng mô hình phân loại comment tiếng Việt từ livestream / social commerce. 
Mục tiêu: tự động nhận diện loại comment để phục vụ automation trong hệ thống bán hàng .

2) Dataset

nguồn: file livestream_comments_1000.csv

dữ liệu dạng text 2 cột chính: comment / labels

dữ liệu có nhiều dạng comment ngắn, tự nhiên

đã tiến hành bước tiền xử lý: lower case, remove url, remove digit, remove punctuation, strip whitespace

3) Model Approach

dùng HuggingFace Transformer model (pretrained base model)

fine tune classification head trên tập comment tiếng Việt

training trực tiếp end2end trên HF Trainer

Lợi điểm: model hiểu ngữ cảnh VN tốt hơn TF-IDF.

4) Training Process

chia train / validation

tối ưu cross entropy classification

lưu mapping id2label / label2id từ model để phục vụ inference API

5) | Metric      | Value      |
| ----------- | ---------- |
| Loss        | 1.11398    |
| Accuracy    | 0.955      |
| F1 Macro    | 0.9551     |
| F1 Weighted | 0.95537    |
| Runtime     | 196.11 sec |


6) Notebook Structure

Load & Clean dữ liệu

EDA simple

Tokenizer + Model load HF

Train / Evaluate model

Save mapping id2label

Inference test với 1 câu thực tế
