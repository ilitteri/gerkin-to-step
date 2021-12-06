from __future__ import annotations
from abc import abstractmethod
from typing import Dict, List
from io import TextIOWrapper


class Statement:
    name = None

    @classmethod
    def for_line(self, line: str, outfile: TextIOWrapper) -> Statement:
        for subclass in self.__subclasses__():
            if subclass.is_for(line):
                return subclass(line, outfile)


    @classmethod
    def is_for(self, line: str) -> bool:
        return line.strip().startswith(self.name) 


    @abstractmethod
    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]):
        pass


    def get_pattern(self, line: str) -> str:
        return line.strip().split(self.name)[1][1:]


    def _write_statement_block(self, patterns: list) -> None:
        if not (self.pattern in patterns):
            patterns.append(self.pattern)
            self.outfile.write(f'{self.name}("{self.pattern}", function() {"{"}\n')
            self.write_end_of_block()


    def write_end_of_block(self) -> None:
        self.outfile.write(f'\t// Write code here that turns the phrase above into concrete actions\n')
        self.outfile.write(f'\treturn "pending";\n')
        self.outfile.write(f'{"}"});\n\n')


class Given(Statement):
    name = "Given"

    def __init__(self, line: str, outfile: TextIOWrapper) -> None:
        self.outfile = outfile
        self.line = line
        self.pattern = self.get_pattern(line)


    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]) -> None:
        antecessors.append(self.name)
        self._write_statement_block(previous_patterns[self.name])


class When(Statement):
    name = "When"

    def __init__(self, line: str, outfile: TextIOWrapper) -> None:
        self.outfile = outfile
        self.line = line
        self.pattern = self.get_pattern(line)


    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]) -> None:
        antecessors.append(self.name)
        self._write_statement_block(previous_patterns[self.name])


class Then(Statement):
    name = "Then"

    def __init__(self, line: str, outfile: TextIOWrapper) -> None:
        self.outfile = outfile
        self.line = line
        self.pattern = self.get_pattern(line)


    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]) -> None:
        antecessors.append(self.name)
        self._write_statement_block(previous_patterns[self.name])


class And(Statement):
    name = "And"

    def __init__(self, line: str, outfile: TextIOWrapper) -> None:
        self.outfile = outfile
        self.line = line
        self.pattern = self.get_pattern(line)


    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]) -> None:
        given_patterns, then_patterns = previous_patterns["Given"], previous_patterns["Then"]
        if not (self.pattern in given_patterns): 
            given_patterns.append(self.pattern)
        elif not (self.pattern in then_patterns):
            then_patterns.append(self.pattern)
        self.outfile.write(f'{antecessors[-1]}("{self.pattern}", function() {"{"}\n')
        self.write_end_of_block()


class NotAStatement(Statement):
    name = ""

    def __init__(self, line: str, outfile: TextIOWrapper):
        self.outfile = outfile
        self.line = line


    def write_statement_block(self, antecessors: List[str], previous_patterns: Dict[str, List[str]]):
        pass
