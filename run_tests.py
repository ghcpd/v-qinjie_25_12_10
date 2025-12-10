"""
Test runner for user_display module.
Ensures environment is set up and runs all tests with performance metrics.
"""

import sys
import subprocess
import os

def run_tests():
    """Run the complete test suite."""
    print("=" * 80)
    print("User Display Module - Test Runner")
    print("=" * 80)
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tests_dir = os.path.join(current_dir, "tests")
    test_file = os.path.join(tests_dir, "test_all.py")
    
    if not os.path.exists(test_file):
        print(f"ERROR: Test file not found: {test_file}")
        return False
    
    print(f"\nRunning tests from: {test_file}\n")
    
    # Run tests using Python
    result = subprocess.run(
        [sys.executable, test_file],
        cwd=current_dir,
        capture_output=False
    )
    
    return result.returncode == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
