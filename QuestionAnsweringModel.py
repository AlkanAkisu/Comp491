import torch
from transformers import BertForQuestionAnswering

from transformers import BertTokenizer


def predict_answer(question, context):
    '''
    Predicts an answer for the given question from the context
    Question: String
    Context: String 
    Returns predicted answer as String
    '''
    
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    input_ids = torch.tensor(tokenizer.encode(question,
                                              context,
                                              truncation=True, add_special_tokens=True)).int()
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    sep_idx = 0
    for c in tokens:
        if c == '[SEP]':
            break
        sep_idx += 1
    num_seg_a = sep_idx + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = ([0] * num_seg_a + [1] * num_seg_b)
    segment_ids = torch.tensor(segment_ids).to(torch.int32)
    assert len(segment_ids) == len(input_ids)
    output = model(input_ids.unsqueeze(0), token_type_ids=segment_ids)
    answer_start = torch.argmax(output.start_logits)
    answer_end = torch.argmax(output.end_logits)
    if answer_end >= answer_start:
        answer = tokens[answer_start]
        for i in range(answer_start + 1, answer_end + 1):
            if tokens[i][0:2] == "##":
                answer += tokens[i][2:]
            else:
                answer += " " + tokens[i]
    if answer.startswith("[CLS]"):
        answer = "Unable to find the answer to your question."
    #print("\nQuestion:\n{}".format(question.capitalize()))
    #print("\nAnswer:\n{}.".format(answer.capitalize()))

    return answer.capitalize()


predict_answer('Where is cafe nero?','Cafe Nero Working Hours Weekdays : 07:30 – 20:00    Weekends : 09:00 – 17:00    Location : College of Admin. Sciences & Economics & Winter Garden    Cafe Nero Working Hours Weekdays : 07:30 – 20:00    Weekends : 09:00 – 17:00    Location : Semahat – Nusret Arsel Science and Technology Building / Courtyard Floor    Divan in Bakery Working Hours Weekdays : 07:00 – 18:00    Weekends : Closed    Location : Student Center -1. Floor    Divan Sports Cafe Working Hours Weekdays : 11:00 – 18:00    Weekends : Closed    Location : Student Center Entrance Floor    Divan Suzy\'s Cafe Working Hours Weekdays : 07:00 – 18:00    Weekends : Closed    Location : Student Center Entrance Floor    Enginar Working Hours Weekdays : 08:30 – 02:00    Weekends : 08:30 – 02:00    Location : S Dorm Building    Espresso Lab Working Hours Weekdays : 08:00 – 20:00    Weekend : Closed    Location : Semahat – Nusret Arsel Science and Technology Building / Courtyard    Highborn Cafe Working Hours Weekdays : 08:00 – 20:00    Saturday : 10:00 – 15:00    Sunday : Closed    Location : Social Sciences building    Küçük Ev Working Hours Weekdays : 08:00 – 21:00    Weekends : 11:00 – 21:00    Location : Student Center 1. Floor    Lokma Campus Working Hours Weekdays : 07:30 – 21:00    Weekends : 07:30 – 21:00    Location : Student Center -1. Floor    Mio Cafe Working Hours Weekdays : 07:30 – 21:00    Saturdays : Closed    Sundays : 11:00 – 21:00    Location : Student Center -1. Floor    Mozilla Cafe Working Hours Weekdays : 07:30 – 22:00    Weekends : 07:30 – 22:00    Location : West Campus    Pişti Working Hours Weekdays : 11:00 – 21:45    Weekends : Closed    Location : In front of Sports Center    Pişti Avlu Working Hours Weekdays : 08:00 – 20:00    Weekends : Closed    Location : Engineering Courtyard    Planet Cafeteria Working Hours Weekdays : 08:00 – 20:00    Weekends : Closed    Location : Faculty of Social Sciences & Humanities    Hardal Working Hours Weekdays : 24 Hours Open    Weekends : 24 Hours Open    Location : S Dorm Building    Vitaminhane Working Hours Weekdays : 11:00 – 17:00    Weekends : Closed    Location : Student Center -1. Floor    Yemekhane Working Hours Weekdays    Breakfast : 07:00 – 10:00    Lunch : 11:30 – 14:30    Dinner : 17:00 – 20:00    Weekends    Breakfast : 08:00 – 10:30    Lunch : 11:30 – 14:00    Dinner : 16:30 – 18:30    Location : Student Center -2. Floor')

