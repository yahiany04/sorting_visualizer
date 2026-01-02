"""
Quick Sort Algorithm
Team Member: Hossam Aqeel
"""

import time

def quick_sort(array, draw_data, delay_func, is_sorting_func, update_stats_func):
    """
    Quick Sort: Partitions array around pivot and recursively sorts.
    Time Complexity: O(n log n) average, O(n²) worst case
    Space Complexity: O(log n)
    Stability: Unstable
    """
    comparisons = 0
    swaps = 0
    
    def quick_sort_recursive(low, high, comps, swps):
        if low < high and is_sorting_func():
            pi, c, s = partition(low, high, comps, swps)
            c1, s1 = quick_sort_recursive(low, pi - 1, c, s)
            return quick_sort_recursive(pi + 1, high, c1, s1)
        return comps, swps

    def partition(low, high, comps, swps):
        if not is_sorting_func(): 
            return low, comps, swps
        
        pivot = array[high]
        i = low - 1
        
        for j in range(low, high):
            if not is_sorting_func(): 
                return i, comps, swps
            
            comps += 1
            draw_data([j, high], ['comparing', 'pivot'])
            update_stats_func(comps, swps)
            time.sleep(delay_func())
            
            if array[j] < pivot:
                i += 1
                if i != j:
                    array[i], array[j] = array[j], array[i]
                    swps += 1
                    
                    draw_data([i, j], ['swapping', 'swapping'])
                    update_stats_func(comps, swps)
                    time.sleep(delay_func())
        
        if is_sorting_func():
            array[i + 1], array[high] = array[high], array[i + 1]
            swps += 1
            
            draw_data([i + 1, high], ['swapping', 'swapping'])
            update_stats_func(comps, swps)
            time.sleep(delay_func())
        
        return i + 1, comps, swps

    quick_sort_recursive(0, len(array) - 1, comparisons, swaps)
