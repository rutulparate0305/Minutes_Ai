from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def summarize_text(text):

    prompt = f"""
Summarize this meeting transcript into bullet points and action items:

{text}
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=200
    )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary