"""
Merge Sort Algorithm
Team Member: Ahmed Hassan
"""

import time

def merge_sort(array, draw_data, delay_func, is_sorting_func, update_stats_func):
    """
    Merge Sort: Divide and conquer algorithm that merges sorted subarrays.
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    Stability: Stable
    """
    comparisons = 0
    swaps = 0
    
    def merge_sort_recursive(left, right, comps, swps):
        if left < right and is_sorting_func():
            mid = (left + right) // 2
            
            c1, s1 = merge_sort_recursive(left, mid, comps, swps)
            c2, s2 = merge_sort_recursive(mid + 1, right, c1, s1)
            return merge(left, mid, right, c2, s2)
        return comps, swps

    def merge(left, mid, right, comps, swps):
        if not is_sorting_func(): 
            return comps, swps
        
        left_arr = array[left:mid + 1]
        right_arr = array[mid + 1:right + 1]
        
        i = j = 0
        k = left
        
        while i < len(left_arr) and j < len(right_arr) and is_sorting_func():
            comps += 1
            
            draw_data([k], ['comparing'])
            update_stats_func(comps, swps)
            time.sleep(delay_func())
            
            if left_arr[i] <= right_arr[j]:
                array[k] = left_arr[i]
                i += 1
            else:
                array[k] = right_arr[j]
                j += 1
            
            swps += 1
            k += 1
        
        while i < len(left_arr) and is_sorting_func():
            array[k] = left_arr[i]
            i += 1
            k += 1
            swps += 1
            time.sleep(delay_func())
            
        while j < len(right_arr) and is_sorting_func():
            array[k] = right_arr[j]
            j += 1
            k += 1
            swps += 1
            time.sleep(delay_func())
            
        return comps, swps

    merge_sort_recursive(0, len(array) - 1, comparisons, swaps)
