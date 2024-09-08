from django import template

register = template.Library()


@register.filter(name="split_with_decreasing_chunks")
def split_with_decreasing_chunks(text, initial_size=17):
    """Splits the text into progressively smaller chunks of words."""
    words = text.split()
    chunks = []
    current_size = initial_size  # Start with the initial size

    i = 0
    while i < len(words):
        # Append the chunk of the current size to the list
        chunks.append(' '.join(words[i:i + current_size]))
        i += current_size  # Move the index by the current size
        current_size = max(current_size - 3, 1)  # Decrease size by 3, with a minimum of 1 word per line

    return chunks
