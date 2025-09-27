"""
Data models for the Word Test Paper Generator.
These classes represent the data structures used throughout the application.
"""
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class TestItem:
    """Represents a single test item (either explain or statement type)."""
    text: str
    word: str
    
    def validate(self) -> bool:
        """Validate that the word exists in the text for statement items."""
        return bool(self.text and self.word)


@dataclass
class TestData:
    """Contains all test data loaded from configuration."""
    explain_items: List[TestItem]
    statement_items: List[TestItem]
    
    def validate(self) -> bool:
        """Validate all test items."""
        # Validate explain items
        for item in self.explain_items:
            if not item.validate():
                return False
        
        # Validate statement items (word must be in text)
        for item in self.statement_items:
            if not item.validate() or item.word not in item.text:
                return False
        
        return True
    
    def get_total_items(self) -> int:
        """Get total number of test items."""
        return len(self.explain_items) + len(self.statement_items)


@dataclass
class TestPaperConfig:
    """Configuration for test paper generation."""
    input_filename: str
    font_name: str = "Comic Sans MS"
    font_size: int = 12
    margin_inches: float = 1 / 2.54  # 1 cm converted to inches
    headings: List[str] = None
    
    def __post_init__(self):
        if self.headings is None:
            self.headings = ["1st", "2nd"]


@dataclass
class GeneratedFiles:
    """Information about generated test files."""
    test_file_path: str
    answer_file_path: str
    base_filename: str