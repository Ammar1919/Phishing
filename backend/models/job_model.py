from setfit import SetFitModel
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

model = SetFitModel.from_pretrained("Tomiwajin/setfit_email_classifier")

def predict_job(text):
    preds = model(text)
    if preds in ["not-job-related", "not-job-status-update"]:
        return None
    preds = {"prediction": str(preds)}
    return preds

if __name__ == "__main__":
    print(predict_job("Hello Ammar, Thank you for your application. We have received your application for the Young Talents Days. We will review your application for Project Engineer Intern F/M shortly, and get back to you as soon as possible. Best regards"))