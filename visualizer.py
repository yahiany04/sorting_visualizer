import tkinter as tk
from tkinter import ttk
import random
import time
import threading
from bubble_sort import bubble_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

class SortingVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize variables
        self.array = []
        self.array_size = 30
        self.sorting = False
        self.speed = 0.1
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        
        # Colors
        self.colors = {
            'normal': '#e94560',
            'comparing': '#ffd700',
            'swapping': '#00d4ff',
            'sorted': '#7b2cbf',
            'pivot': '#ff6b6b'
        }
        
        self.setup_ui()
        self.generate_array()
        
    def setup_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(title_frame, text="Sorting Algorithm Visualizer", 
                              font=('Arial', 28, 'bold'), fg='#00d4ff', bg='#1a1a2e')
        title_label.pack()
        
        # Control Panel
        control_frame = tk.Frame(self.root, bg='#16213e', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Algorithm Selection
        algo_frame = tk.Frame(control_frame, bg='#16213e')
        algo_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(algo_frame, text="Algorithm:", font=('Arial', 10, 'bold'), 
                fg='#c9d1d9', bg='#16213e').pack()
        
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        self.algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                           values=["Bubble Sort", "Selection Sort", "Insertion Sort", 
                                                  "Merge Sort", "Quick Sort"], state="readonly", width=15)
        self.algorithm_combo.pack(pady=5)
        self.algorithm_combo.bind('<<ComboboxSelected>>', self.update_algorithm_info)
        
        # Array Size
        size_frame = tk.Frame(control_frame, bg='#16213e')
        size_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(size_frame, text="Array Size:", font=('Arial', 10, 'bold'), 
                fg='#c9d1d9', bg='#16213e').pack()
        
        self.size_var = tk.IntVar(value=30)
        size_scale = tk.Scale(size_frame, from_=10, to=100, orient='horizontal',
                             variable=self.size_var, command=self.on_size_change,
                             bg='#16213e', fg='#c9d1d9', highlightbackground='#16213e')
        size_scale.pack()
        
        # Speed Control
        speed_frame = tk.Frame(control_frame, bg='#16213e')
        speed_frame.pack(side='left', padx=10, pady=10)
        
        tk.Label(speed_frame, text="Speed:", font=('Arial', 10, 'bold'), 
                fg='#c9d1d9', bg='#16213e').pack()
        
        self.speed_var = tk.StringVar(value="Medium")
        speed_combo = ttk.Combobox(speed_frame, textvariable=self.speed_var,
                                  values=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"], 
                                  state="readonly", width=10)
        speed_combo.pack(pady=5)
        speed_combo.bind('<<ComboboxSelected>>', self.update_speed)
        
        # Buttons
        button_frame = tk.Frame(control_frame, bg='#16213e')
        button_frame.pack(side='bottom', padx=10, pady=10)
        
        self.generate_btn = tk.Button(button_frame, text="Generate Array", 
                                     command=self.generate_array, bg='#000000', fg='white',
                                     font=('Arial', 10, 'bold'), relief='flat', padx=20, pady=8)
        self.generate_btn.pack(side='left', padx=5)
        
        self.sort_btn = tk.Button(button_frame, text="Start Sort", 
                                 command=self.start_sorting, bg='#000000', fg='white',
                                 font=('Arial', 10, 'bold'), relief='flat', padx=20, pady=8)
        self.sort_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop", 
                                 command=self.stop_sorting, bg='#000000', fg='white',
                                 font=('Arial', 10, 'bold'), relief='flat', padx=20, pady=8, state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(self.root, bg='#0f3460', height=400)
        self.canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Information Panel
        info_frame = tk.Frame(self.root, bg='#16213e', relief='raised', bd=2)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Statistics (now on left)
        left_info = tk.Frame(info_frame, bg='#16213e')
        left_info.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(left_info, text="Statistics", font=('Arial', 12, 'bold'), 
                fg='#e94560', bg='#16213e').pack(anchor='w')
        
        self.stats_label = tk.Label(left_info, text="", font=('Arial', 10), 
                                   fg='#c9d1d9', bg='#16213e', justify='left')
        self.stats_label.pack(anchor='w', pady=5)
        
        # Algorithm Info (now on right)
        right_info = tk.Frame(info_frame, bg='#16213e')
        right_info.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(right_info, text="Algorithm Information", font=('Arial', 12, 'bold'), 
                fg='#e94560', bg='#16213e').pack(anchor='w')
        
        self.algo_info_label = tk.Label(right_info, text="", font=('Arial', 10), 
                                       fg='#c9d1d9', bg='#16213e', justify='left')
        self.algo_info_label.pack(anchor='w', pady=5)
        
        # Team Credits
        credits_frame = tk.Frame(self.root, bg='#1a1a2e')
        credits_frame.pack(fill='x', pady=5)
        
        credits_text = ("Team: Ahmed Hassan (Merge Sort) | Youssef Mouen (Bubble Sort) | "
                       "Youssef Naser (Insertion Sort) | Hossam Aqeel (Quick Sort) | Yahia Yasser (Selection Sort)")
        tk.Label(credits_frame, text=credits_text, font=('Arial', 10), 
                fg='#8b949e', bg='#1a1a2e').pack()
        
        self.update_algorithm_info()
        self.update_stats()
    
    def generate_array(self):
        if self.sorting:
            return
            
        self.array_size = self.size_var.get()
        self.array = [random.randint(10, 390) for _ in range(self.array_size)]
        self.reset_stats()
        self.draw_array()
    
    def draw_array(self, colored_indices=None, colors=None):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            self.root.after(100, lambda: self.draw_array(colored_indices, colors))
            return
        
        bar_width = (canvas_width - 20) / len(self.array)
        max_height = canvas_height - 40
        max_value = max(self.array) if self.array else 1
        
        for i, value in enumerate(self.array):
            x1 = 10 + i * bar_width
            x2 = x1 + bar_width - 2
            
            bar_height = (value / max_value) * max_height
            y1 = canvas_height - 20
            y2 = y1 - bar_height
            
            # Determine color
            color = self.colors['normal']
            if colored_indices and i in colored_indices:
                if colors and i < len(colors):
                    color = self.colors.get(colors[i], self.colors['normal'])
                else:
                    color = self.colors['comparing']
            
            # Draw bar
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#1a1a2e', width=1)
            
            # Draw value if bar is wide enough
            if bar_width > 20:
                text_y = y2 - 15 if y2 > 30 else y2 + 15
                self.canvas.create_text((x1 + x2) / 2, text_y, text=str(value), 
                                      font=('Arial', 8, 'bold'), fill='#c9d1d9')
        
        self.root.update()
    
    def on_size_change(self, value):
        if not self.sorting:
            self.generate_array()
    
    def update_speed(self, event=None):
        speed_map = {
            "Very Slow": 0.5,
            "Slow": 0.2,
            "Medium": 0.1,
            "Fast": 0.05,
            "Very Fast": 0.01
        }
        self.speed = speed_map.get(self.speed_var.get(), 0.1)
    
    def update_algorithm_info(self, event=None):
        algo_info = {
            "Bubble Sort": {
                "description": "Repeatedly swaps adjacent elements if they're in wrong order.\nSimple but inefficient for large datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Stable"
            },
            "Selection Sort": {
                "description": "Finds minimum element and places it at the beginning.\nPerforms well on small datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Unstable"
            },
            "Insertion Sort": {
                "description": "Builds sorted array one element at a time.\nEfficient for small or nearly sorted datasets.",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stability": "Stable"
            },
            "Merge Sort": {
                "description": "Divide and conquer algorithm that merges sorted subarrays.\nConsistent O(n log n) performance.",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "stability": "Stable"
            },
            "Quick Sort": {
                "description": "Partitions array around pivot and recursively sorts.\nFast average case, but O(n²) worst case.",
                "time_complexity": "O(n log n) avg, O(n²) worst",
                "space_complexity": "O(log n)",
                "stability": "Unstable"
            }
        }
        
        current_algo = self.algorithm_var.get()
        info = algo_info.get(current_algo, {})
        
        info_text = f"Description: {info.get('description', '')}\n"
        info_text += f"Time Complexity: {info.get('time_complexity', '')}\n"
        info_text += f"Space Complexity: {info.get('space_complexity', '')}\n"
        info_text += f"Stability: {info.get('stability', '')}"
        
        self.algo_info_label.config(text=info_text)
    
    def update_stats(self):
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        stats_text = f"Comparisons: {self.comparisons}\n"
        stats_text += f"Swaps: {self.swaps}\n"
        stats_text += f"Time Elapsed: {elapsed_time:.2f}s\n"
        stats_text += f"Array Size: {len(self.array)}"
        
        self.stats_label.config(text=stats_text)
    
    def reset_stats(self):
        self.comparisons = 0
        self.swaps = 0
        self.start_time = 0
        self.update_stats()
    
    def start_sorting(self):
        if self.sorting or not self.array:
            return
        
        self.sorting = True
        self.start_time = time.time()
        self.sort_btn.config(state='disabled')
        self.generate_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        algorithm = self.algorithm_var.get()
        
        # Start sorting in a separate thread
        sort_thread = threading.Thread(target=self.run_sort_algorithm, args=(algorithm,))
        sort_thread.daemon = True
        sort_thread.start()

    def run_sort_algorithm(self, algorithm):
        try:
            # Callbacks for algorithms
            def draw_callback(indices, colors):
                self.root.after(0, lambda: self.draw_array(indices, colors))
            
            def delay_callback():
                return self.speed
            
            def is_sorting_callback():
                return self.sorting
            
            def update_stats_callback(comps, swaps):
                self.comparisons = comps
                self.swaps = swaps
                self.root.after(0, self.update_stats)

            if algorithm == "Bubble Sort":
                bubble_sort(self.array, draw_callback, delay_callback, is_sorting_callback, update_stats_callback)
            elif algorithm == "Selection Sort":
                selection_sort(self.array, draw_callback, delay_callback, is_sorting_callback, update_stats_callback)
            elif algorithm == "Insertion Sort":
                insertion_sort(self.array, draw_callback, delay_callback, is_sorting_callback, update_stats_callback)
            elif algorithm == "Merge Sort":
                merge_sort(self.array, draw_callback, delay_callback, is_sorting_callback, update_stats_callback)
            elif algorithm == "Quick Sort":
                quick_sort(self.array, draw_callback, delay_callback, is_sorting_callback, update_stats_callback)
            
            # Highlight sorted array
            if self.sorting:
                self.root.after(0, lambda: self.draw_array(list(range(len(self.array))), 
                                                          ['sorted'] * len(self.array)))
        except Exception as e:
            print(f"Sorting error: {e}")
        finally:
            self.sorting = False
            self.root.after(0, self.enable_controls)
    
    def stop_sorting(self):
        self.sorting = False
        self.enable_controls()
    
    def enable_controls(self):
        self.sort_btn.config(state='normal')
        self.generate_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
    
    def run(self):
        self.root.mainloop()
