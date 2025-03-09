import nltk
def split_text_into_fragments(text, max_length):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    
    # Initialize variables
    fragments = []
    current_fragment = []
    current_length = 0

    # Iterate through sentences
    for sentence in sentences:
        # Calculate the length of the sentence
        sentence_length = len(sentence)
        
        # If adding the sentence exceeds the maximum length, start a new fragment
        if current_length + sentence_length > max_length:
            current_fragment = " ".join([i.strip() for i in current_fragment])
            fragments.append(current_fragment)
            current_fragment = []
            current_length = 0
        
        # Add the sentence to the current fragment
        current_fragment.append(sentence)
        current_length += sentence_length

    # Add the remaining fragment if any
    if current_fragment:
        current_fragment = " ".join([i.strip() for i in current_fragment])
        fragments.append(current_fragment)

    return fragments
