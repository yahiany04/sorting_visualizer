"""
Insertion Sort Algorithm
Team Member: Yousef Naser
"""

import time

def insertion_sort(array, draw_data, delay_func, is_sorting_func, update_stats_func):
    """
    Insertion Sort: Builds sorted array one element at a time.
    Time Complexity: O(n²)
    Space Complexity: O(1)
    Stability: Stable
    """
    comparisons = 0
    swaps = 0
    
    for i in range(1, len(array)):
        if not is_sorting_func(): 
            return
        
        key = array[i]
        j = i - 1
        
        draw_data([i], ['comparing'])
        time.sleep(delay_func())
        
        while j >= 0 and array[j] > key:
            if not is_sorting_func(): 
                return
            comparisons += 1
            array[j + 1] = array[j]
            swaps += 1
            
            draw_data([j, j + 1], ['swapping', 'swapping'])
            update_stats_func(comparisons, swaps)
            time.sleep(delay_func())
            j -= 1
            
        if is_sorting_func():
            array[j + 1] = key
