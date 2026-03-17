from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

def generate_answer(context, question):
    model_name = "distilbert-base-uncased-distilled-squad"
    
    # 1. Load the tokenizer (the eyes) and the model (the brain)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForQuestionAnswering.from_pretrained(model_name)

    # 2. Encode the question and context together
    inputs = tokenizer(question, context, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    # 3. Get the model's prediction for where the answer starts and ends
    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # 4. Find the highest probability start and end points
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores) + 1

    # 5. Convert those tokens back into a string
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end]))

    return answer  
