from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("finetuned_phish_model")
model = AutoModelForSequenceClassification.from_pretrained("finetuned_phish_model")

#tokenizer = AutoTokenizer.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")
#model = AutoModelForSequenceClassification.from_pretrained("cybersectony/phishing-email-detection-distilbert_v2.4.1")

def predict_email(email_text):
    inputs = tokenizer(
        email_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=1)
    
    probs = predictions[0].tolist()

    labels = {
        "legitimate_email": probs[0],
        "phishing_url": probs[1],
        "legitimate_url": probs[2],
        "phishing_url_alt": probs[3]
    }g

    max_label = max(labels.items(), key=lambda x: x[1])

    return {
        "prediction": max_label[0],
        "confidence": max_label[1],
        "all_probabilities": labels
    }

def eval_results(results):
    prediction = results["prediction"]

    if prediction == "phishing_url":
        return 1
    else:
        return 0

if __name__ == '__main__':
    email = """
   Hello!

Thanks for registering for the upcoming event. You can access your ticket here: http://eventbrite.com/platform/docs/events
Thank you,
Events Team
            """
    result = predict_email(email)
    confidence = result["confidence"]
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print("\nAll probabilities:")
    for label, prob in result['all_probabilities'].items():
        print(f"{label}: {prob:.2%}")
    
    