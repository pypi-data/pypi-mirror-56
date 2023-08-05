from dataclasses import dataclass
from typing import List

from regtester.TestItemResult  import TestItemResult
@dataclass
class TestResponse:
    all_good: bool
    regex_name: str
    success_count:int
    failure_count:int
    total:int
    successes : List[TestItemResult] 
    failures : List[TestItemResult]
