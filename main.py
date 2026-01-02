#!/usr/bin/env python3
"""
Sorting Algorithm Visualizer - Main Entry Point
================================================

This is the main entry point for the Sorting Algorithm Visualizer application.
Run this file to start the interactive GUI that demonstrates various sorting
algorithms with real-time visualization.

Features:
---------
- 5 sorting algorithms: Bubble, Selection, Insertion, Merge, Quick Sort
- Real-time visualization with color-coded operations
- Performance statistics (comparisons, swaps, time)
- Multiple array patterns (Random, Nearly Sorted, Reversed, Few Unique)
- Dark/Light theme support
- Keyboard shortcuts for quick control

Usage:
------
    python main.py

Requirements:
-------------
- Python 3.6+
- tkinter (usually included with Python)

Authors:
--------
Team Project:
- Ahmed Hassan (Merge Sort)
- Youssef Mouen (Bubble Sort)  
- Youssef Naser (Insertion Sort)
- Hossam Aqeel (Quick Sort)
- Yahia Yasser (Selection Sort)

Version: 2.0.0
"""

import sys
import os

# Add current directory to path so imports work correctly
# This ensures the module can find the sorting algorithm files
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualizer import SortingVisualizer


def main() -> None:
    """
    Main function to initialize and run the Sorting Visualizer.
    
    Creates an instance of the SortingVisualizer class and starts
    the tkinter main event loop.
    """
    print("🚀 Starting Sorting Algorithm Visualizer...")
    print("=" * 50)
    print("Keyboard Shortcuts:")
    print("  [Space] - Start/Stop sorting")
    print("  [G]     - Generate new array")
    print("  [T]     - Toggle theme (dark/light)")
    print("  [Esc]   - Stop sorting")
    print("=" * 50)
    
    app = SortingVisualizer()
    app.run()


if __name__ == "__main__":
    main()
