from dataclasses import dataclass

@dataclass
class TestItemResult:
    text: str
    expected_result: any
    actual_result:any
    success:bool
