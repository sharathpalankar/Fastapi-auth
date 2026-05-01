inp="abcabcbb"

def lengthOfLongestSubstring(s: str) -> int:
    char_index_map = set()
    left = 0
    max_length = 0
    start_index = 0

    for right in range(len(s)):
        while s[right] in char_index_map:
            char_index_map.remove(s[left])
            left += 1
        char_index_map.add(s[right])

        if right - left + 1 > max_length:
            max_length = right - left + 1
            start_index = left 

        

        max_length = max(max_length, right - left + 1)

    return max_length
   