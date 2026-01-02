import sys
import os

# Add current directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualizer import SortingVisualizer

if __name__ == "__main__":
    app = SortingVisualizer()
    app.run()
