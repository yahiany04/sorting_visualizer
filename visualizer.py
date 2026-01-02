"""
Sorting Algorithm Visualizer
============================
A comprehensive visual demonstration tool for various sorting algorithms.

This module provides an interactive GUI application that allows users to:
- Visualize different sorting algorithms in real-time
- Compare algorithm performance through statistics
- Customize visualization parameters (speed, array size, patterns)
- Learn about algorithm complexity and characteristics

Features:
- Multiple sorting algorithms (Bubble, Selection, Insertion, Merge, Quick Sort)
- Real-time visualization with color-coded operations
- Performance statistics (comparisons, swaps, time elapsed)
- Multiple array generation patterns
- Dark/Light theme support
- Keyboard shortcuts for quick control

Author: Team Project
Version: 2.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
from typing import List, Callable, Optional, Dict, Any

# Import sorting algorithm modules
from bubble_sort import bubble_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort


class SortingVisualizer:
    """
    Main application class for the Sorting Algorithm Visualizer.
    
    This class creates and manages the entire GUI application, including:
    - The main window and all UI components
    - Array generation and manipulation
    - Sorting algorithm execution in separate threads
    - Real-time visualization updates
    - Statistics tracking and display
    
    Attributes:
        root (tk.Tk): The main tkinter window
        array (List[int]): The array of values to be sorted
        array_size (int): Current size of the array
        sorting (bool): Flag indicating if sorting is in progress
        speed (float): Delay between visualization steps in seconds
        comparisons (int): Number of comparisons made during sorting
        swaps (int): Number of swaps made during sorting
        start_time (float): Timestamp when sorting started
        dark_mode (bool): Current theme mode (True for dark, False for light)
        array_pattern (str): Current array generation pattern
    """
    
    # ==================== INITIALIZATION ====================
    
    def __init__(self):
        """
        Initialize the Sorting Visualizer application.
        
        Sets up the main window, initializes all variables,
        configures the UI components, and generates the initial array.
        """
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1200x850")
        
        # Initialize state variables
        self.array: List[int] = []
        self.array_size: int = 30
        self.sorting: bool = False
        self.speed: float = 0.1
        self.comparisons: int = 0
        self.swaps: int = 0
        self.start_time: float = 0
        
        # New feature flags
        self.dark_mode: bool = True
        self.array_pattern: str = "Random"
        self.paused: bool = False
        
        # Theme colors - easily customizable color schemes
        self.themes = {
            'dark': {
                'bg_primary': '#1a1a2e',
                'bg_secondary': '#16213e',
                'canvas_bg': '#0f3460',
                'text_primary': '#00d4ff',
                'text_secondary': '#c9d1d9',
                'text_muted': '#8b949e',
                'accent': '#e94560'
            },
            'light': {
                'bg_primary': '#f5f5f5',
                'bg_secondary': '#e0e0e0',
                'canvas_bg': '#ffffff',
                'text_primary': '#1976d2',
                'text_secondary': '#333333',
                'text_muted': '#666666',
                'accent': '#d32f2f'
            }
        }
        
        # Bar colors for visualization states
        self.colors = {
            'normal': '#e94560',      # Default bar color
            'comparing': '#ffd700',    # Yellow - elements being compared
            'swapping': '#00d4ff',     # Cyan - elements being swapped
            'sorted': '#7b2cbf',       # Purple - sorted elements
            'pivot': '#ff6b6b'         # Red - pivot element (for Quick Sort)
        }
        
        # Apply initial theme and setup UI
        self._apply_theme()
        self.setup_ui()
        self._setup_keyboard_shortcuts()
        self.generate_array()
        
    def _apply_theme(self) -> None:
        """
        Apply the current color theme to the main window.
        
        Updates the background color of the root window based on
        whether dark mode is enabled or not.
        """
        theme = self.themes['dark' if self.dark_mode else 'light']
        self.root.configure(bg=theme['bg_primary'])
    
    def _setup_keyboard_shortcuts(self) -> None:
        """
        Configure keyboard shortcuts for quick application control.
        
        Shortcuts:
            Space: Start/Stop sorting
            G: Generate new array
            R: Reset array
            T: Toggle theme (dark/light)
            Escape: Stop sorting
        """
        self.root.bind('<space>', lambda e: self._toggle_sorting())
        self.root.bind('<g>', lambda e: self.generate_array())
        self.root.bind('<G>', lambda e: self.generate_array())
        self.root.bind('<t>', lambda e: self._toggle_theme())
        self.root.bind('<T>', lambda e: self._toggle_theme())
        self.root.bind('<Escape>', lambda e: self.stop_sorting())
    
    def _toggle_sorting(self) -> None:
        """Toggle between starting and stopping the sort operation."""
        if self.sorting:
            self.stop_sorting()
        else:
            self.start_sorting()
    
    def _toggle_theme(self) -> None:
        """
        Toggle between dark and light themes.
        
        Updates all UI components to reflect the new theme colors.
        """
        if self.sorting:
            return  # Don't change theme while sorting
            
        self.dark_mode = not self.dark_mode
        theme = self.themes['dark' if self.dark_mode else 'light']
        
        # Update main window
        self.root.configure(bg=theme['bg_primary'])
        
        # Update canvas
        self.canvas.configure(bg=theme['canvas_bg'])
        
        # Redraw array with new theme
        self.draw_array()
        
        # Update theme button text
        self.theme_btn.config(text="☀️ Light" if self.dark_mode else "🌙 Dark")
        
    # ==================== UI SETUP ====================
        
    def setup_ui(self) -> None:
        """
        Set up the complete user interface.
        
        Creates and arranges all UI components including:
        - Title bar
        - Control panel (algorithm selection, size, speed, pattern)
        - Action buttons (Generate, Start, Stop, Theme)
        - Visualization canvas
        - Information panel (statistics, algorithm info)
        - Team credits footer
        - Keyboard shortcuts help
        """
        theme = self.themes['dark' if self.dark_mode else 'light']
        
        # ---- Title Section ----
        title_frame = tk.Frame(self.root, bg=theme['bg_primary'])
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔢 Sorting Algorithm Visualizer", 
            font=('Arial', 28, 'bold'), 
            fg=theme['text_primary'], 
            bg=theme['bg_primary']
        )
        title_label.pack()
        
        # ---- Main Control Panel ----
        control_frame = tk.Frame(self.root, bg=theme['bg_secondary'], relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm Selection
        algo_frame = tk.Frame(control_frame, bg=theme['bg_secondary'])
        algo_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(
            algo_frame, 
            text="📊 Algorithm:", 
            font=('Arial', 10, 'bold'), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary']
        ).pack()
        
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.algorithm_combo = ttk.Combobox(
            algo_frame, 
            textvariable=self.algorithm_var,
            values=["Bubble Sort", "Selection Sort", "Insertion Sort", 
                   "Merge Sort", "Quick Sort"], 
            state="readonly", 
            width=15
        )
        self.algorithm_combo.pack(pady=5)
        self.algorithm_combo.bind('<<ComboboxSelected>>', self.update_algorithm_info)
        
        # Array Size Control
        size_frame = tk.Frame(control_frame, bg=theme['bg_secondary'])
        size_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(
            size_frame, 
            text="📏 Array Size:", 
            font=('Arial', 10, 'bold'), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary']
        ).pack()
        
        self.size_var = tk.IntVar(value=30)
        size_scale = tk.Scale(
            size_frame, 
            from_=10, 
            to=100, 
            orient='horizontal',
            variable=self.size_var, 
            command=self.on_size_change,
            bg=theme['bg_secondary'], 
            fg=theme['text_secondary'], 
            highlightbackground=theme['bg_secondary']
        )
        size_scale.pack()
        
        # Speed Control
        speed_frame = tk.Frame(control_frame, bg=theme['bg_secondary'])
        speed_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(
            speed_frame, 
            text="⚡ Speed:", 
            font=('Arial', 10, 'bold'), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary']
        ).pack()
        
        self.speed_var = tk.StringVar(value="Medium")
        speed_combo = ttk.Combobox(
            speed_frame, 
            textvariable=self.speed_var,
            values=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"], 
            state="readonly", 
            width=10
        )
        speed_combo.pack(pady=5)
        speed_combo.bind('<<ComboboxSelected>>', self.update_speed)
        
        # NEW FEATURE: Array Pattern Selection
        pattern_frame = tk.Frame(control_frame, bg=theme['bg_secondary'])
        pattern_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(
            pattern_frame, 
            text="🎲 Pattern:", 
            font=('Arial', 10, 'bold'), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary']
        ).pack()
        
        self.pattern_var = tk.StringVar(value="Random")
        pattern_combo = ttk.Combobox(
            pattern_frame, 
            textvariable=self.pattern_var,
            values=["Random", "Nearly Sorted", "Reversed", "Few Unique"], 
            state="readonly", 
            width=12
        )
        pattern_combo.pack(pady=5)
        pattern_combo.bind('<<ComboboxSelected>>', lambda e: self.generate_array())
        
        # ---- Action Buttons ----
        button_frame = tk.Frame(control_frame, bg=theme['bg_secondary'])
        button_frame.pack(side='right', padx=10, pady=10)
        
        # Button style configuration
        btn_config = {
            'bg': '#000000', 
            'fg': 'white',
            'font': ('Arial', 10, 'bold'), 
            'relief': 'flat', 
            'padx': 15, 
            'pady': 8
        }
        
        self.generate_btn = tk.Button(
            button_frame, 
            text="🔄 Generate", 
            command=self.generate_array, 
            **btn_config
        )
        self.generate_btn.pack(side='left', padx=3)
        
        self.sort_btn = tk.Button(
            button_frame, 
            text="▶️ Start", 
            command=self.start_sorting, 
            **btn_config
        )
        self.sort_btn.pack(side='left', padx=3)
        
        self.stop_btn = tk.Button(
            button_frame, 
            text="⏹️ Stop", 
            command=self.stop_sorting, 
            state='disabled',
            **btn_config
        )
        self.stop_btn.pack(side='left', padx=3)
        
        # NEW FEATURE: Theme Toggle Button
        self.theme_btn = tk.Button(
            button_frame, 
            text="☀️ Light", 
            command=self._toggle_theme,
            **btn_config
        )
        self.theme_btn.pack(side='left', padx=3)
        
        # ---- Visualization Canvas ----
        self.canvas = tk.Canvas(self.root, bg=theme['canvas_bg'], height=400)
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # ---- Information Panel ----
        info_frame = tk.Frame(self.root, bg=theme['bg_secondary'], relief='raised', bd=2)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Statistics Panel (Left Side)
        left_info = tk.Frame(info_frame, bg=theme['bg_secondary'])
        left_info.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            left_info, 
            text="📈 Statistics", 
            font=('Arial', 12, 'bold'), 
            fg=theme['accent'], 
            bg=theme['bg_secondary']
        ).pack(anchor='w')
        
        self.stats_label = tk.Label(
            left_info, 
            text="", 
            font=('Arial', 10), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary'], 
            justify='left'
        )
        self.stats_label.pack(anchor='w', pady=5)
        
        # Algorithm Information Panel (Right Side)
        right_info = tk.Frame(info_frame, bg=theme['bg_secondary'])
        right_info.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(
            right_info, 
            text="📚 Algorithm Information", 
            font=('Arial', 12, 'bold'), 
            fg=theme['accent'], 
            bg=theme['bg_secondary']
        ).pack(anchor='w')
        
        self.algo_info_label = tk.Label(
            right_info, 
            text="", 
            font=('Arial', 10), 
            fg=theme['text_secondary'], 
            bg=theme['bg_secondary'], 
            justify='left'
        )
        self.algo_info_label.pack(anchor='w', pady=5)
        
        # ---- Footer Section ----
        footer_frame = tk.Frame(self.root, bg=theme['bg_primary'])
        footer_frame.pack(fill='x', pady=5)
        
        # Team Credits
        credits_text = (
            "Team: Ahmed Hassan (Merge Sort) | Youssef Mouen (Bubble Sort) | "
            "Youssef Naser (Insertion Sort) | Hossam Aqeel (Quick Sort) | Yahia Yasser (Selection Sort)"
        )
        tk.Label(
            footer_frame, 
            text=credits_text, 
            font=('Arial', 9), 
            fg=theme['text_muted'], 
            bg=theme['bg_primary']
        ).pack()
        
        # NEW FEATURE: Keyboard Shortcuts Help
        shortcuts_text = "⌨️ Shortcuts: [Space] Start/Stop | [G] Generate | [T] Theme | [Esc] Stop"
        tk.Label(
            footer_frame, 
            text=shortcuts_text, 
            font=('Arial', 9, 'italic'), 
            fg=theme['text_muted'], 
            bg=theme['bg_primary']
        ).pack(pady=2)
        
        # Initialize displays
        self.update_algorithm_info()
        self.update_stats()
    
    # ==================== ARRAY GENERATION ====================
    
    def generate_array(self) -> None:
        """
        Generate a new array based on the selected pattern.
        
        Patterns available:
        - Random: Completely random values
        - Nearly Sorted: Array with a few elements out of place
        - Reversed: Array in descending order
        - Few Unique: Array with limited unique values (tests stability)
        
        Does nothing if sorting is currently in progress.
        """
        if self.sorting:
            return
            
        self.array_size = self.size_var.get()
        pattern = self.pattern_var.get()
        
        # Generate array based on selected pattern
        if pattern == "Random":
            self.array = [random.randint(10, 390) for _ in range(self.array_size)]
        elif pattern == "Nearly Sorted":
            # Create sorted array then swap a few random pairs
            self.array = list(range(10, 10 + self.array_size * 4, 4))[:self.array_size]
            # Swap ~10% of elements
            for _ in range(max(1, self.array_size // 10)):
                i, j = random.sample(range(self.array_size), 2)
                self.array[i], self.array[j] = self.array[j], self.array[i]
        elif pattern == "Reversed":
            # Descending order - worst case for many algorithms
            self.array = list(range(390, 390 - self.array_size * 4, -4))[:self.array_size]
        elif pattern == "Few Unique":
            # Only 5 unique values - tests algorithm behavior with duplicates
            unique_vals = [50, 150, 200, 300, 350]
            self.array = [random.choice(unique_vals) for _ in range(self.array_size)]
        
        self.reset_stats()
        self.draw_array()
    
    def draw_array(self, colored_indices: Optional[List[int]] = None, 
                   colors: Optional[List[str]] = None) -> None:
        """
        Draw the current array state on the canvas.
        
        Each array element is represented as a vertical bar. The height
        of the bar corresponds to the element's value. Bars can be
        colored differently to indicate operations being performed.
        
        Args:
            colored_indices: List of indices to highlight with special colors
            colors: List of color keys ('comparing', 'swapping', 'sorted', 'pivot')
                   corresponding to each index in colored_indices
        """
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Handle case where canvas hasn't been rendered yet
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.draw_array(colored_indices, colors))
            return
        
        # Calculate bar dimensions
        bar_width = (canvas_width - 20) / len(self.array)
        max_height = canvas_height - 40
        max_value = max(self.array) if self.array else 1
        
        theme = self.themes['dark' if self.dark_mode else 'light']
        
        # Draw each bar
        for i, value in enumerate(self.array):
            # Calculate bar position
            x1 = 10 + i * bar_width
            x2 = x1 + bar_width - 2
            
            # Calculate bar height (proportional to value)
            bar_height = (value / max_value) * max_height
            y1 = canvas_height - 20
            y2 = y1 - bar_height
            
            # Determine bar color based on state
            color = self.colors['normal']
            if colored_indices and i in colored_indices:
                idx_pos = colored_indices.index(i)
                if colors and idx_pos < len(colors):
                    color = self.colors.get(colors[idx_pos], self.colors['normal'])
                else:
                    color = self.colors['comparing']
            
            # Draw the bar rectangle
            self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                fill=color, 
                outline=theme['bg_primary'], 
                width=1
            )
            
            # Draw value label if bar is wide enough
            if bar_width > 20:
                text_y = y2 - 15 if y2 > 30 else y2 + 15
                self.canvas.create_text(
                    (x1 + x2) / 2, text_y, 
                    text=str(value), 
                    font=('Arial', 8, 'bold'), 
                    fill=theme['text_secondary']
                )
        
        self.root.update()
    
    def on_size_change(self, value: str) -> None:
        """
        Handle array size slider change event.
        
        Generates a new array when the size is changed,
        unless sorting is currently in progress.
        
        Args:
            value: The new size value (as string from Scale widget)
        """
        if not self.sorting:
            self.generate_array()
    
    # ==================== SPEED & SETTINGS ====================
    
    def update_speed(self, event=None) -> None:
        """
        Update the animation speed based on user selection.
        
        Maps user-friendly speed names to actual delay values in seconds.
        Lower delay = faster animation.
        
        Args:
            event: Optional event from combobox selection
        """
        speed_map = {
            "Very Slow": 0.5,   # 500ms delay - good for learning
            "Slow": 0.2,        # 200ms delay
            "Medium": 0.1,      # 100ms delay - default
            "Fast": 0.05,       # 50ms delay
            "Very Fast": 0.01   # 10ms delay - for quick comparisons
        }
        self.speed = speed_map.get(self.speed_var.get(), 0.1)
    
    # ==================== ALGORITHM INFORMATION ====================
    
    def update_algorithm_info(self, event=None) -> None:
        """
        Update the algorithm information display panel.
        
        Shows detailed information about the currently selected algorithm
        including description, time/space complexity, and stability.
        
        Args:
            event: Optional event from combobox selection
        """
        # Comprehensive algorithm information database
        algo_info = {
            "Bubble Sort": {
                "description": "Repeatedly swaps adjacent elements if they're in wrong order.\nSimple but inefficient for large datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Stable",
                "best_case": "O(n) - when already sorted"
            },
            "Selection Sort": {
                "description": "Finds minimum element and places it at the beginning.\nPerforms well on small datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Unstable",
                "best_case": "O(n²) - always same"
            },
            "Insertion Sort": {
                "description": "Builds sorted array one element at a time.\nEfficient for small or nearly sorted datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Stable",
                "best_case": "O(n) - when nearly sorted"
            },
            "Merge Sort": {
                "description": "Divide and conquer algorithm that merges sorted subarrays.\nConsistent O(n log n) performance.",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "stability": "Stable",
                "best_case": "O(n log n) - always same"
            },
            "Quick Sort": {
                "description": "Partitions array around pivot and recursively sorts.\nFast average case, but O(n²) worst case.",
                "time_complexity": "O(n log n) avg, O(n²) worst",
                "space_complexity": "O(log n)",
                "stability": "Unstable",
                "best_case": "O(n log n) - balanced partitions"
            }
        }
        
        current_algo = self.algorithm_var.get()
        info = algo_info.get(current_algo, {})
        
        # Format the information text
        info_text = f"📝 {info.get('description', '')}\n"
        info_text += f"⏱️ Time: {info.get('time_complexity', '')} | Best: {info.get('best_case', '')}\n"
        info_text += f"💾 Space: {info.get('space_complexity', '')} | {info.get('stability', '')}"
        
        self.algo_info_label.config(text=info_text)
    
    # ==================== STATISTICS ====================
    
    def update_stats(self) -> None:
        """
        Update the statistics display panel.
        
        Shows current sorting statistics including:
        - Number of comparisons made
        - Number of swaps performed
        - Elapsed time since sorting started
        - Current array size and pattern
        """
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        pattern = self.pattern_var.get() if hasattr(self, 'pattern_var') else "Random"
        
        stats_text = f"🔢 Array Size: {len(self.array)} ({pattern})\n"
        stats_text += f"🔍 Comparisons: {self.comparisons}\n"
        stats_text += f"🔄 Swaps: {self.swaps}\n"
        stats_text += f"⏱️ Time Elapsed: {elapsed_time:.2f}s"
        
        self.stats_label.config(text=stats_text)
    
    def reset_stats(self) -> None:
        """
        Reset all statistics to their initial values.
        
        Called when generating a new array or before starting a new sort.
        """
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.update_stats()
    
    # ==================== SORTING CONTROL ====================
    
    def start_sorting(self) -> None:
        """
        Start the sorting process with the selected algorithm.
        
        Initiates sorting in a separate thread to keep UI responsive.
        Disables control buttons during sorting to prevent conflicts.
        """
        if self.sorting or not self.array:
            return
        
        self.sorting = True
        self.start_time = time.time()
        
        # Update button states
        self.sort_btn.config(state='disabled')
        self.generate_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        algorithm = self.algorithm_var.get()
        
        # Start sorting in a separate thread to keep UI responsive
        sort_thread = threading.Thread(
            target=self.run_sort_algorithm, 
            args=(algorithm,),
            name=f"SortThread-{algorithm}"
        )
        sort_thread.daemon = True  # Thread will close when main program exits
        sort_thread.start()

    def run_sort_algorithm(self, algorithm: str) -> None:
        """
        Execute the selected sorting algorithm.
        
        This method runs in a separate thread. It sets up callback
        functions that the sorting algorithms use to communicate
        with the visualization.
        
        Args:
            algorithm: Name of the sorting algorithm to run
        """
        try:
            # Callback to update visualization (thread-safe)
            def draw_callback(indices: List[int], colors: List[str]) -> None:
                self.root.after(0, lambda: self.draw_array(indices, colors))
            
            # Callback to get current delay setting
            def delay_callback() -> float:
                return self.speed
            
            # Callback to check if sorting should continue
            def is_sorting_callback() -> bool:
                return self.sorting
            
            # Callback to update statistics (thread-safe)
            def update_stats_callback(comps: int, swaps: int) -> None:
                self.comparisons = comps
                self.swaps = swaps
                self.root.after(0, self.update_stats)

            # Execute the selected algorithm
            if algorithm == "Bubble Sort":
                bubble_sort(self.array, draw_callback, delay_callback, 
                           is_sorting_callback, update_stats_callback)
            elif algorithm == "Selection Sort":
                selection_sort(self.array, draw_callback, delay_callback, 
                              is_sorting_callback, update_stats_callback)
            elif algorithm == "Insertion Sort":
                insertion_sort(self.array, draw_callback, delay_callback, 
                              is_sorting_callback, update_stats_callback)
            elif algorithm == "Merge Sort":
                merge_sort(self.array, draw_callback, delay_callback, 
                          is_sorting_callback, update_stats_callback)
            elif algorithm == "Quick Sort":
                quick_sort(self.array, draw_callback, delay_callback, 
                          is_sorting_callback, update_stats_callback)
            
            # Highlight all bars as sorted when complete
            if self.sorting:
                self.root.after(0, lambda: self.draw_array(
                    list(range(len(self.array))), 
                    ['sorted'] * len(self.array)
                ))
                
        except Exception as e:
            # Log errors without crashing the application
            print(f"⚠️ Sorting error: {e}")
        finally:
            # Always cleanup and re-enable controls
            self.sorting = False
            self.root.after(0, self.enable_controls)
    
    def stop_sorting(self) -> None:
        """
        Stop the current sorting operation.
        
        Sets the sorting flag to False, which causes the sorting
        algorithm to exit at its next check point.
        """
        self.sorting = False
        self.enable_controls()
    
    def enable_controls(self) -> None:
        """
        Re-enable all control buttons after sorting completes or stops.
        """
        self.sort_btn.config(state='normal')
        self.generate_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    # ==================== APPLICATION MAIN LOOP ====================
    
    def run(self) -> None:
        """
        Start the tkinter main event loop.
        
        This method blocks until the window is closed.
        """
        self.root.mainloop()
