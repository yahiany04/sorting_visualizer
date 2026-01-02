"""
Bubble Sort Algorithm
Team Member: Youssef Mouen
"""

import time

def bubble_sort(array, draw_data, delay_func, is_sorting_func, update_stats_func):
    """
    Bubble Sort: Repeatedly swaps adjacent elements if they're in wrong order.
    Time Complexity: O(n²)
    Space Complexity: O(1)
    Stability: Stable
    """
    n = len(array)
    comparisons = 0
    swaps = 0
    
    for i in range(n):
        if not is_sorting_func(): 
            return
        swapped = False
        for j in range(0, n - i - 1):
            if not is_sorting_func(): 
                return
            
            comparisons += 1
            draw_data([j, j + 1], ['comparing', 'comparing'])
            update_stats_func(comparisons, swaps)
            time.sleep(delay_func())
            
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                swaps += 1
                swapped = True
                
                draw_data([j, j + 1], ['swapping', 'swapping'])
                update_stats_func(comparisons, swaps)
                time.sleep(delay_func())
        
        if not swapped:
            break
