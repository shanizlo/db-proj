def validate_values_find_word(author, title, verse, line, pos):
    if author is "":
        return "Please enter song author."
    if title is "":
        return "Please enter song title."
    if verse is "":
        return "Please enter verse number."
    if line is "":
        return "Please enter line number."
    if pos is "":
        return "Please enter word in line number."
    # Validating integers
    try:
        val = int(verse)
    except ValueError:
        return "Verse number should be integer."

    try:
        val = int(line)
    except ValueError:
        return "Line number should be integer."

    try:
        val = int(pos)
    except ValueError:
        return "Word in line number should be integer."

    return None
