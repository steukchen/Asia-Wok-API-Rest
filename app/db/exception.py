
class ExceptionRepository(Exception):
    def __init__(self,message:str,code:int = 400, *args):
        self.message = message
        self.code = code
        super().__init__(*args)