"""
GUI management classes following SOLID principles.
Handles user interface logic separately from business logic.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

from interfaces import GUIManagerInterface, IconManagerInterface
from exceptions import GUIError


class IconManager(IconManagerInterface):
    """Manages application icon setup for GUI windows."""
    
    def __init__(self, icon_folder: str = "icons"):
        self.icon_folder = icon_folder
        self.png_path = os.path.abspath(os.path.join(icon_folder, "score.png"))
        self.ico_path = os.path.abspath(os.path.join(icon_folder, "score.ico"))
    
    def setup_icon(self, root_window) -> None:
        """Setup application icon for the given window."""
        try:
            self._setup_app_id()
            self._create_ico_if_needed()
            self._set_window_icon(root_window)
        except Exception as e:
            print(f"Warning: Failed to setup icon: {e}")
    
    def _setup_app_id(self) -> None:
        """Setup Windows app ID for taskbar icon."""
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("WordTestPaperGenerator.1.0")
        except Exception:
            pass
    
    def _create_ico_if_needed(self) -> None:
        """Create ICO file from PNG if available and needed."""
        if not PIL_AVAILABLE or not os.path.exists(self.png_path):
            return
        
        try:
            img = Image.open(self.png_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Remove old ICO file and recreate
            if os.path.exists(self.ico_path):
                os.remove(self.ico_path)
            
            # Create ICO with standard sizes
            sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
            img.save(self.ico_path, format='ICO', sizes=sizes)
        except Exception as e:
            print(f"Warning: Failed to create ICO file: {e}")
    
    def _set_window_icon(self, root_window) -> None:
        """Set window icon using available formats."""
        # Try ICO first
        if os.path.exists(self.ico_path):
            try:
                root_window.iconbitmap(self.ico_path)
            except Exception as e:
                print(f"Warning: Failed to set ICO icon: {e}")
        
        # Try PNG as fallback
        if os.path.exists(self.png_path):
            try:
                icon_img = tk.PhotoImage(file=self.png_path)
                root_window.iconphoto(True, icon_img)
                root_window.icon_ref = icon_img  # Keep reference
            except Exception as e:
                print(f"Warning: Failed to set PNG icon: {e}")


class GUIManager(GUIManagerInterface):
    """Manages the graphical user interface for the application."""
    
    def __init__(self, 
                 available_files_callback: Callable[[], list],
                 generate_callback: Callable[[str, bool], None],
                 icon_manager: IconManagerInterface):
        self.available_files_callback = available_files_callback
        self.generate_callback = generate_callback
        self.icon_manager = icon_manager
        self.root: Optional[tk.Tk] = None
        self.folder_var: Optional[tk.StringVar] = None
    
    def run_gui(self) -> None:
        """Run the graphical user interface."""
        try:
            self._create_main_window()
            self._setup_window_properties()
            self._create_widgets()
            self.root.mainloop()
        except Exception as e:
            raise GUIError(f"Failed to run GUI: {e}")
    
    def _create_main_window(self) -> None:
        """Create and configure the main window."""
        self.root = tk.Tk()
        self.root.title("Word Test Paper Generator")
        self.root.geometry("400x300")
        self.root.option_add("*Font", "Arial 16")
    
    def _setup_window_properties(self) -> None:
        """Setup window properties including icon."""
        if self.icon_manager:
            self.icon_manager.setup_icon(self.root)
        self.root.update()
    
    def _create_widgets(self) -> None:
        """Create and arrange GUI widgets."""
        # File selection
        self._create_file_selection_widgets()
        
        # Buttons
        self._create_button_widgets()
    
    def _create_file_selection_widgets(self) -> None:
        """Create file selection dropdown and label."""
        self.folder_var = tk.StringVar()
        
        folder_label = ttk.Label(self.root, text="Select file:")
        folder_label.pack(pady=5)
        
        folder_dropdown = ttk.Combobox(self.root, textvariable=self.folder_var)
        folder_dropdown.pack(pady=5)
        
        # Populate dropdown with available files
        try:
            files = self.available_files_callback()
            folder_dropdown["values"] = files
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load available files: {e}")
    
    def _create_button_widgets(self) -> None:
        """Create action buttons."""
        # Configure button style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 14))
        
        # Generate button
        generate_button = ttk.Button(
            self.root,
            text="Generate File",
            command=lambda: self._handle_generate(print_file=False),
            style="TButton"
        )
        generate_button.pack(side="left", padx=20)
        
        # Generate and print button
        generate_print_button = ttk.Button(
            self.root,
            text="Generate and Print",
            command=lambda: self._handle_generate(print_file=True),
            style="TButton"
        )
        generate_print_button.pack(side="right", padx=20)
    
    def _handle_generate(self, print_file: bool = False) -> None:
        """Handle generate button click."""
        if not self.folder_var:
            messagebox.showerror("Error", "GUI not properly initialized")
            return
        
        selected_file = self.folder_var.get()
        if not selected_file:
            messagebox.showerror("Error", "Please select a file")
            return
        
        try:
            self.generate_callback(selected_file, print_file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate file: {e}")