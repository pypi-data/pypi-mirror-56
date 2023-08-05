from regtester.RegExTest import RegExTest
from regtester.RegExTestItem import RegExTestItem
from regtester.TestItemResult import TestItemResult
from regtester.TestResponse import TestResponse
import os
import argparse
import sys
import importlib
from typing import List
from colorama import init, deinit
from colorama import Fore, Back, Style
from pathlib import Path
class RegExTester:

    def __init__(self,path:str):
        init() #useful for window
        self.tests:RegExTest = []
        self.current_regex_test : RegExTest = None
        self.find_regex_tests(path)
        results = self.all_regex_test()
        self.show_results(results)
    def find_regex_tests(self,path:str) -> List[RegExTest]:
        # folder with the tests classes has to contain a __init__.py file
        if(os.path.isfile(path)):
            sys.path.append(str(Path(path).parent.resolve()))
            class_name = path.split("/")[-1].replace(".py","")
            module = eval(f"importlib.import_module('{class_name}')")
            class_instance =  getattr(module, class_name)()
            assert isinstance(class_instance, RegExTest), f"The class {class_name} doesn't herit the base class RegExTest"
            self.tests.append(class_instance)
        elif(os.path.isdir(path)):
            sys.path.append(path)
            for filename in os.listdir(path):
                if filename.endswith("Test.py"): 
                    class_name = filename.replace(".py","")
                    class_module = eval(f"importlib.import_module('{class_name}')")
                    class_instance =  getattr(class_module, class_name)()
                    assert isinstance(class_instance, RegExTest), f"The class {class_name} doesn't herit the base class RegExTest"
                    self.tests.append(class_instance)
            self.info(f"{len(self.tests)} Test classes were found")
        else:
            raise ValueError('The path is neither a valid folder or a valid file')

    def test_one(self,item:RegExTestItem) -> TestItemResult:
        result = self.current_regex_test.exec_regex(
            self.current_regex_test.compiled_regex,
            item.text
        )
        return TestItemResult(
            text = item.text,
            expected_result = item.expected_result,
            actual_result = result,
            success = result == item.expected_result
        )

    def test_all_examples(self,reg_test:RegExTest) -> TestResponse:
        self.current_regex_test = reg_test
        items:List[RegExTestItem] = reg_test.get_tests()
        test_item_results = [self.test_one(item) for item in items]
        successes = [item for item in test_item_results if item.success]
        failures = [item for item in test_item_results if not item.success]
        return TestResponse(
            all_good=len(failures) == 0,
            regex_name = self.current_regex_test.get_regex_name(),
            success_count = len(successes),
            failure_count = len(failures),
            total = len(items),
            successes=successes,
            failures=failures,
        )

    def all_regex_test(self) -> List[TestResponse]:
            return [self.test_all_examples(reg_test) for reg_test in self.tests]

    @staticmethod
    def ok_message(text:str):
        print(Style.BRIGHT + Back.GREEN + Fore.WHITE)
        print(text)
        print(Style.RESET_ALL)

    @staticmethod
    def error_message(text:str):
        print(Style.BRIGHT + Back.RED + Fore.WHITE)
        print(text)
        print(Style.RESET_ALL)

    @staticmethod
    def info(text:str):
        print(Style.BRIGHT + Back.CYAN + Fore.WHITE)
        print(text)
        print(Style.RESET_ALL)
    def show_results(self,results:List[TestResponse]) -> None:
        for test_response in results:
            print("...........................................................")
            if(test_response.all_good):
                self.ok_message(f"{test_response.regex_name} => OK  ({test_response.success_count}/{test_response.total})")
            else:
                self.error_message(f"{test_response.regex_name} => Failures  ({test_response.failure_count}/{test_response.total})")
                for item in test_response.failures:
                    self.error_message(f"text => {item.text}\nexpected => {item.expected_result} \ngot => {item.actual_result}")

        all_test = sum([test_response.total for test_response in results])
        test_passed = sum([test_response.success_count for test_response in results])
        test_failed = sum([test_response.failure_count for test_response in results])
        self.info(f"Total tests : {all_test}, Successes  {test_passed}, Failures :  {test_failed}")
        deinit()

def main():
    parser = argparse.ArgumentParser(description = "A RegEx Tester") 
    parser.add_argument("test_path", metavar = "test_path", type = str,  
                     help = "the path is used toe xecute tests, it can be a folder containing a __init__.py file or a file")
    args = parser.parse_args() 
    RegExTester(args.test_path)

def test():
    RegExTester(f"{str(Path(__file__).parent)}/test_samples")
if __name__ == "__main__":
    test()
