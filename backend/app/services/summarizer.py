from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model once globally (efficient)
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def summarize_text(text):
    """
    Converts transcript into structured meeting minutes
    using third-person professional tone
    """

    if not text.strip():
        return "No transcript available."

    prompt = f"""
Convert the following conversation into structured meeting minutes.

Format:
Summary:
Key Discussion Points:
Decisions Taken:
Action Items:

Rules:
- Use formal third-person tone
- Do NOT use I or you
- If speaker names are missing use Speaker 1, Speaker 2
- Extract only important discussion content

Conversation:
{text}
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    )

    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=300,
        temperature=0.3,
        top_p=0.9,
        repetition_penalty=1.2
    )

    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary.strip()


def extract_speakers(text):
    """
    Extract speaker names if present
    Otherwise return default speaker labels
    """

    speakers = set()

    for line in text.split("\n"):
        if ":" in line:
            speaker = line.split(":")[0].strip()

            if len(speaker) < 30:
                speakers.add(speaker)

    if not speakers:
        return ["Speaker 1", "Speaker 2"]

    return list(speakers)


def extract_action_items(text):
    """
    Detect possible action items from transcript
    using extended keyword matching
    """

    keywords = [
        "action",
        "todo",
        "follow up",
        "deadline",
        "assign",
        "submit",
        "prepare",
        "complete",
        "finish",
        "send",
        "update",
        "review"
    ]

    actions = []

    for line in text.split("\n"):
        for keyword in keywords:
            if keyword in line.lower():
                actions.append(line.strip())
                break

    if not actions:
        return ["No explicit action items detected"]

    return actions