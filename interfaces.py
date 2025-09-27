"""
Abstract interfaces for the Word Test Paper Generator.
These interfaces define contracts for different components following SOLID principles.
"""
from abc import ABC, abstractmethod
from typing import List
from models import TestData, TestPaperConfig, GeneratedFiles


class ConfigLoaderInterface(ABC):
    """Interface for loading test configuration data."""
    
    @abstractmethod
    def load_config(self, filename: str) -> TestData:
        """Load test data from configuration file."""
        pass
    
    @abstractmethod
    def get_available_files(self) -> List[str]:
        """Get list of available configuration files."""
        pass


class DocumentGeneratorInterface(ABC):
    """Interface for generating test documents."""
    
    @abstractmethod
    def generate_test_paper(self, test_data: TestData, config: TestPaperConfig) -> GeneratedFiles:
        """Generate test paper and answer sheet."""
        pass


class FileManagerInterface(ABC):
    """Interface for file operations."""
    
    @abstractmethod
    def get_unique_filename(self, base_filename: str, extension: str = ".docx") -> str:
        """Get a unique filename to avoid conflicts."""
        pass
    
    @abstractmethod
    def ensure_output_directory(self) -> None:
        """Ensure output directory exists."""
        pass


class DataShufflerInterface(ABC):
    """Interface for shuffling test data."""
    
    @abstractmethod
    def shuffle_data(self, test_data: TestData) -> TestData:
        """Shuffle the test data items randomly."""
        pass


class GUIManagerInterface(ABC):
    """Interface for GUI management."""
    
    @abstractmethod
    def run_gui(self) -> None:
        """Run the graphical user interface."""
        pass


class IconManagerInterface(ABC):
    """Interface for managing application icons."""
    
    @abstractmethod
    def setup_icon(self, root_window) -> None:
        """Setup application icon for the window."""
        pass