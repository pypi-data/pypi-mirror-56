from config import Config

class CustomAnalyzer:
    def get_custom_analyzer(self):
        return {
            'char_filter': Config.CHAR_FILTER,
            'tokenizer': Config.TOKENIZER,
            'filter': Config.TOKEN_FILTER,
        } 