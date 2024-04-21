def create_ascii_dict():
    ascii_dict = {}
    for i in range(128):  # ASCII range
        ascii_dict[chr(i)] = i
    return ascii_dict

# Example usage:
ascii_dict = create_ascii_dict()
print(ascii_dict)