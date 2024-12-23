from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

#model_name = "deepset/xlm-roberta-large-squad2"
class QA_model:

    def __init__(self, model_name, tokenizer):
        self.nlp = pipeline('question-answering', model=model_name, tokenizer=tokenizer)

    def get_time(self, context):
        """
        Get free time and busy time in passage.
        Args:
            context (str): is the passage want to get time.
        Returns:
            Return free time and busy time.
        """
        # Get free time
        QA_free = {
            'question' : "When is available time during for scheduling meeting in free time?",
            'context' : context 
        }
        res_free = self.nlp(QA_free)

        # Get busy time
        QA_busy = {
            'question' : "When is unavailable time during for scheduling meeting in free time?",
            'context' : context 
        }
        res_busy = self.nlp(QA_busy)
        print(res_free , res_busy)
        return processing_time(res_free, res_busy)

    def get_day(self, text, time):
        """
        Get day for time.
        Args:
            text (str): is the passage want to get time.
            time (str): is a unit time
        Returns:
            Time (str): day of time.
        """
        QA = {
            'question' : f"What time period does time {time} belong to?",
            'context' : text 
        }   
        res = self.nlp(QA)
        return(res.get('answer'))


def processing_time(res_free, res_busy):
    """
    Extract real time user avaiable or not.
    Args:
        res_free (respone of pipline): respone of pipline for free time in parse.
        res_busy : respone of pipline for busy time in parse.
    Return:
        Free time, Busy time
    """

    # Check score confident
    if res_free['score'] < 0.01 or res_busy['score'] < 0.01:
        if res_free['score'] < 0.01 and res_busy['score'] < 0.01:
            return None, None 
        elif res_free['score'] < 0.01:
            return None, res_busy['answer']
        else:
            return res_free['answer'], None

    # Case of answer
    if res_free['answer'] not in res_busy['answer'] and res_busy['answer'] not in res_free['answer']:
        return res_free['answer'], res_busy['answer']
    
    if res_free['score'] >= res_busy['score'] :
        return res_free['answer'], None
    else:
        return None, res_busy['answer']


if __name__ == '__main__':
    model_name = "deepset/xlm-roberta-large-squad2"
    model = QA_model(model_name, model_name)
    context = "I'm avaiable every morning from 9 to 11 AM, except on Wednesday."
    free, busy = model.get_time(context)
    print( f"Free time: {free}, busy time: {busy}")

    #
    context = "I'm avaiable everymorning and every night from 2 to 10:11 am. and im can go meetting at Tuesday"
    day  = model.get_day(context, "2 to 10:11 am")
    print( f"Free time: {day}")
    
    context = "i am avaiable Monday 2 to 10:11 am, Tuesday 1 to 10 pm."
    day  = model.get_day(context, "2 to 10:11 am")
    print( f"Free time: {day}")