"""
Exception classes for the Word Test Paper Generator.
Provides specific exception types for better error handling.
"""


class TestPaperGeneratorError(Exception):
    """Base exception for all test paper generator errors."""
    pass


class ConfigurationError(TestPaperGeneratorError):
    """Raised when there's an error in configuration loading or validation."""
    pass


class FileNotFoundError(TestPaperGeneratorError):
    """Raised when a required file is not found."""
    pass


class ValidationError(TestPaperGeneratorError):
    """Raised when data validation fails."""
    pass


class DocumentGenerationError(TestPaperGeneratorError):
    """Raised when document generation fails."""
    pass


class GUIError(TestPaperGeneratorError):
    """Raised when GUI operations fail."""
    pass