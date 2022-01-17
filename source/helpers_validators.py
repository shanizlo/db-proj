def validate_values_find_word(author, title, verse, line, pos):
    """
        This file validates given inputs with specific error messages, according to the errors found.

        Parameters
        -----------
        author: str

        title: str

        verse: int

        line: int

        pos: int

        Returns
        -----------
        str:
            Returns a string if there was some sort of error with the given inputs - that they weren't in their
            respective types or if the inputs were empty.
        None:
            No tests failed and the input is fine.
    """
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
