## run once to download the model
from transformers import pipeline

model_dir = "./qa_model"  ## Local directory where the model will be saved
qa_model = pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")
qa_model.save_pretrained(model_dir)