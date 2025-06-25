import pandas as pd
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW
import torch

class EmailDataset(Dataset):
    def __init__(self, csv_file, tokenizer, label2id):
        self.data = pd.read_csv(csv_file)
        self.tokenizer = tokenizer
        self.label2id = label2id

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data.iloc[idx]['text']
        label = self.label2id[self.data.iloc[idx]['label']]
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=256,
            return_tensors='pt'
        )
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item['labels'] = torch.tensor(label)
        return item
    

label2id = {
    "legitimate_email": 0,
    "phishing_url": 1,
    "legitimate_url": 2,
    "phishing_url_alt": 3
}

tokenizer = AutoTokenizer.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")
model = AutoModelForSequenceClassification.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")

dataset = EmailDataset("emails_dataset.csv", tokenizer, label2id)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

device = torch.device("cpu")
model.to(device)
model.train()

optimizer = AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch}")

model.save_pretrained("finetuned_phish_model")
tokenizer.save_pretrained("finetuned_phish_model")