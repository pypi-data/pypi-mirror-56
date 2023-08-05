import abc
from typing import List
from regtester.RegExTestItem import RegExTestItem
import regex
import re
from re import RegexFlag    
from typing import Pattern

class RegExTest(abc.ABC):

    def __init__(self) -> None:
        regex_str = self.get_regex()
        flags  = self.get_regex_flags()
        self.compiled_regex:Pattern = regex.compile(fr"{regex_str}",flags)

    @abc.abstractmethod
    def get_regex(self) -> str:
        pass

    @abc.abstractmethod
    def get_regex_flags(self)-> RegexFlag:
        pass
    
    @abc.abstractmethod
    def get_regex_name(self)-> str:
        pass
        
    @abc.abstractmethod
    def get_tests(self)-> List[RegExTestItem]:
        pass

    @abc.abstractmethod
    def exec_regex(self, regex:Pattern, text:str)-> any:
        pass

