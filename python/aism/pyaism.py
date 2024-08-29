from typing import Optional

from .aism import RustAism, RustInstance


class Aism(RustAism):
    def __init__(self, *, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)

    def give(self, data: str):
        return self.give(data)


class Instance:
    ri: RustInstance

    def __init__(self, ri: RustInstance):
        self.ri = ri

    def instruct(self, instruction: str) -> str:
        return self.ri.instruct(instruction)

    def translate(self, language: str) -> str:
        return self.ri.translate(language)

    def is_sensitive(self) -> bool:
        return self.ri.is_sensitive()

    def mentioned(self, keyword: str) -> bool:
        return self.ri.mentioned(keyword)
