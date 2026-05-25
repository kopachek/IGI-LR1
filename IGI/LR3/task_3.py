def analyze_text_symbols(input_string):
    """Counts the number of spaces and apostrophes in the given string."""
    spaces_count = 0
    apostrophes_count = 0
    
    for char in input_string:
        if char == ' ':
            spaces_count += 1
        elif char == "'":
            apostrophes_count += 1
            
    return spaces_count, apostrophes_count