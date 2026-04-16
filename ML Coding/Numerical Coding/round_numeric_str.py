def round_string(s: str) -> str:
    """
    Time Complexity: O(n) where n is length of input string
    Space Complexity: O(1) as we only use constant extra space
    """
    dot_index = s.find('.')
    if dot_index == -1:
        return s
        
    integer_part = s[:dot_index]
    if not integer_part:
        integer_part = '0'  
    elif integer_part == '-':
        integer_part = '-0'
        
    decimal_part = s[dot_index + 1:]
    if not decimal_part:
        return integer_part
        
    decimal_part = decimal_part + '0'
    round_up = decimal_part[0] >= '5'
    
    if not round_up:
        return integer_part
        
    if integer_part[0] == '-':
        sign = '-'
        digits = integer_part[1:]
    else:
        sign = ''
        digits = integer_part
        
    if not digits or digits == '0':
        return sign + '1'
        
    digits = list(digits)
    i = len(digits) - 1
    while i >= 0 and digits[i] == '9':
        digits[i] = '0'
        i -= 1
    if i < 0:
        return sign + '1' + ''.join(digits)
    digits[i] = chr(ord(digits[i]) + 1)
    return sign + ''.join(digits)

