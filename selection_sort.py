"""
Selection Sort Algorithm
Team Member: Yahia Yasser
"""

import time


def selection_sort(array, draw_data, delay_func, is_sorting_func, update_stats_func):
    """
    Selection Sort: Finds the minimum element and places it at the beginning.
    Time Complexity: O(n²)
    Space Complexity: O(1)
    Stability: Unstable
    """
    n = len(array)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        if not is_sorting_func():
            return

        min_idx = i
        min_val = array[i]
        
        for j in range(i + 1, n):
            if not is_sorting_func():
                return

            comparisons += 1
            draw_data([min_idx, j], ['pivot', 'comparing'])
            update_stats_func(comparisons, swaps)
            time.sleep(delay_func())

            if array[j] < min_val:
                min_idx = j
                min_val = array[j]

        if min_idx != i:
            array[i], array[min_idx] = min_val, array[i]
            swaps += 1
            draw_data([i, min_idx], ['swapping', 'swapping'])
            update_stats_func(comparisons, swaps)
            time.sleep(delay_func())
