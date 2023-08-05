from regtester.RegExTestItem import RegExTestItem
from regtester.RegExTest import RegExTest
import regex
import re
from re import RegexFlag
from typing import Pattern, List

class ArtNumberTest(RegExTest):

    def get_regex(self) -> str:
        return r"""
        # USE THIS WITH r WHEN CREATING THE STRING IN PYTHON
        ^\s*Article\s((?:p|P)remier)
        |Art\.\s?(\d+)
        |^\s*Article\s(\d+)|^\s*Article\s([A-Za-z]+\.\d+)
        """

    def get_regex_flags(self)-> RegexFlag:
        return re.DOTALL|re.M|re.VERBOSE
    
    def get_regex_name(self)-> str:
        return "extract_article_number"
        
    def get_tests(self)-> List[RegExTestItem]:
        return [
            RegExTestItem(
                text= "Article 2: le projet TELEDAC est doté des organes suivants:\npilotage, un comité technique et une équipe de projet.\n\nun comité de\n\n2\n",
                expected_result="2"
            ),
             RegExTestItem(
                text= "Article premier: le projet TELEDAC est doté des organes suivants:\npilotage, un comité technique et une équipe de projet.\n\nun comité de\n\n2\n",
                expected_result="1"
            )
        ]

    def exec_regex(self, regex:Pattern, text:str) -> any:
        article_numbers = regex.findall(text)
        assert len(article_numbers) > 0
        article_numbers = article_numbers[0] # get the one and only tuple
        article_number =  list(filter(lambda x:x!="",article_numbers))[0] # only one element in the tuple can be non empty
        return "1" if article_number=="premier" else article_number


