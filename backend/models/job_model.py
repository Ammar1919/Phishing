from setfit import SetFitModel
import warnings
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

model = SetFitModel.from_pretrained("Tomiwajin/setfit_email_classifier")

def eval_results(text):
    preds = model(text)
    if preds in ["not-job-related", "not-job-status-update"]:
        return None
    return preds

if __name__ == "__main__":
    print(eval_results("Hello Ammar, Thank you for your application. We have received your application for the Young Talents Days. We will review your application for Project Engineer Intern F/M shortly, and get back to you as soon as possible. Best regards"))