def get_clean_words(text):
    """Splits text into words, removing commas and trailing dots."""
    text_with_spaces = text.replace(',', ' ')
    raw_words = text_with_spaces.split()
    
    clean_words = []
    for word in raw_words:
        cleaned = word.strip('.')
        if cleaned:
            clean_words.append(cleaned)
    
    return clean_words

def count_small_words(words):
    """Returns the count of words with fewer than 6 characters."""
    small_words_count = 0
    
    for word in words:
        if len(word) < 6:
            small_words_count += 1
    
    return small_words_count

def find_shortest_w_word(words):
    """Finds the shortest word ending with the letter 'w'."""
    w_words = []
    
    for word in words:
        if word.lower().endswith('w'):
            w_words.append(word)
    
    if not w_words:
        return None
    
    shortest_word = w_words[0]
    for word in w_words:
        if len(word) < len(shortest_word):
            shortest_word = word
    
    return shortest_word

def sort_words_by_length(words):
    """Returns a new list of words sorted by their length."""
    sorted_words = sorted(words.copy(), key=len)
    
    return sorted_words