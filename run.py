"""
Refactored main application entry point.
Clean, maintainable code following SOLID principles.
"""
import argparse
import sys
from application import TestPaperApplication
from exceptions import TestPaperGeneratorError


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Word Test Paper Generator - Generate randomized test papers from JSON configurations"
    )
    parser.add_argument(
        "-i", "--input", 
        type=str, 
        help="Input JSON configuration file name (in cfg folder)"
    )
    parser.add_argument(
        "--gui", 
        action="store_true", 
        help="Launch GUI mode for interactive use"
    )
    return parser.parse_args()


def run_command_line_mode(app: TestPaperApplication, input_filename: str):
    """Run the application in command line mode."""
    try:
        generated_files = app.generate_test_paper(input_filename)
        print("Files generated successfully:")
        print(f"  Test paper: {generated_files.test_file_path}")
        print(f"  Answer sheet: {generated_files.answer_file_path}")
        return True
    except TestPaperGeneratorError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def run_gui_mode(app: TestPaperApplication):
    """Run the application in GUI mode."""
    try:
        app.run_gui_mode()
        return True
    except TestPaperGeneratorError as e:
        print(f"GUI Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected GUI error: {e}")
        return False


def main():
    """Main application entry point."""
    args = parse_arguments()
    
    # Create application instance
    app = TestPaperApplication()
    
    # Determine mode and run
    if args.gui:
        success = run_gui_mode(app)
    elif args.input:
        success = run_command_line_mode(app, args.input)
    else:
        print("Error: Please provide an input file with -i or use --gui for GUI mode")
        print("Use -h for help")
        success = False
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()