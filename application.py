"""
Main application class that coordinates all components.
Follows dependency injection and single responsibility principles.
"""
import os
from typing import Optional

from interfaces import (
    ConfigLoaderInterface, DocumentGeneratorInterface,
    FileManagerInterface, DataShufflerInterface, GUIManagerInterface
)
from services import ConfigLoader, DocumentGenerator, FileManager, DataShuffler
from gui_manager import GUIManager, IconManager
from models import TestPaperConfig, GeneratedFiles
from exceptions import TestPaperGeneratorError


class TestPaperApplication:
    """Main application class that orchestrates all components."""
    
    def __init__(self,
                 config_loader: Optional[ConfigLoaderInterface] = None,
                 file_manager: Optional[FileManagerInterface] = None,
                 data_shuffler: Optional[DataShufflerInterface] = None,
                 document_generator: Optional[DocumentGeneratorInterface] = None,
                 gui_manager: Optional[GUIManagerInterface] = None):
        """Initialize application with dependency injection."""
        
        # Use dependency injection or create default implementations
        self.file_manager = file_manager or FileManager()
        self.config_loader = config_loader or ConfigLoader()
        self.data_shuffler = data_shuffler or DataShuffler()
        self.document_generator = document_generator or DocumentGenerator(self.file_manager)
        
        # GUI manager is created on demand
        self._gui_manager = gui_manager
    
    def generate_test_paper(self, input_filename: str, print_file: bool = False) -> GeneratedFiles:
        """Generate test paper from input configuration file."""
        try:
            # Load and validate configuration
            test_data = self.config_loader.load_config(input_filename)
            
            # Shuffle data for randomization
            shuffled_data = self.data_shuffler.shuffle_data(test_data)
            
            # Create configuration
            config = TestPaperConfig(input_filename=input_filename)
            
            # Generate documents
            generated_files = self.document_generator.generate_test_paper(shuffled_data, config)
            
            # Handle printing if requested
            if print_file:
                self._handle_printing(generated_files.test_file_path)
            
            return generated_files
            
        except Exception as e:
            if isinstance(e, TestPaperGeneratorError):
                raise
            else:
                raise TestPaperGeneratorError(f"Unexpected error: {e}")
    
    def run_gui_mode(self) -> None:
        """Run the application in GUI mode."""
        if not self._gui_manager:
            icon_manager = IconManager()
            self._gui_manager = GUIManager(
                available_files_callback=self.config_loader.get_available_files,
                generate_callback=self._gui_generate_callback,
                icon_manager=icon_manager
            )
        
        self._gui_manager.run_gui()
    
    def get_available_files(self) -> list:
        """Get list of available configuration files."""
        return self.config_loader.get_available_files()
    
    def _gui_generate_callback(self, filename: str, print_file: bool) -> None:
        """Callback function for GUI file generation."""
        generated_files = self.generate_test_paper(filename, print_file)
        print(f"Generated files:")
        print(f"  Test: {generated_files.test_file_path}")
        print(f"  Answer: {generated_files.answer_file_path}")
    
    def _handle_printing(self, filepath: str) -> None:
        """Handle file printing for Windows."""
        try:
            os.startfile(filepath, "print")
        except Exception as e:
            print(f"Warning: Failed to print file: {e}")