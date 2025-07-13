class StringExtention:
    @staticmethod
    def to_pascal_case(s: str) -> str:
        return ''.join(word.capitalize() for word in s.split('_'))