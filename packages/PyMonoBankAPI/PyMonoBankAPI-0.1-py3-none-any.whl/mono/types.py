from requests import get

def snakeize_s(string):
    answer = ''
    for char in str(string):
        if char.isupper():
            answer += f'_{char.lower()}'
        else:
            answer += char
    return answer

def snakeize_dict(dict_):
    answer = {}
    for key in dict_:
        nkey = snakeize_s(key)
        answer[nkey] = dict_[key]
    return answer

class MonoCard:
    def __init__(self, json, user):
        self.__dict__ = snakeize_dict( json)
        self.id = self.__dict__['id'] #This string for pylint
        self.__user = user

    def as_dict(self):
        answer = self.__dict__.copy()
        del answer['_MonoCard__user']
        return answer
        
    def get_statement(self, from_time, to=''):
        url = f'/personal/statement/{self.id}/{from_time}/{to}'
        return [StatementItem(i) for i in self.__user._get(url)]

class ClientInfo:
    def __init__(self, json):
        self.accounts = []  #This string for pylint    
        self.__dict__ = snakeize_dict( json)
    
    def as_dict(self):
        dict_ = self.__dict__.copy()
        for key in dict_:
            if isinstance(dict_[key], list):
                dict_[key] = [i.as_dict() for i in dict_[key]]
            elif isinstance(dict_[key],dict):
                    dict_[key] = dict_[key].as_dict()
        return dict_

class StatementItem:
    def __init__(self, json):
        self.__dict__ = snakeize_dict( json)

    def as_dict(self):
        return self.__dict__.copy()