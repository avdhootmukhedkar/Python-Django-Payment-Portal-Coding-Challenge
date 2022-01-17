"""
Problem Overview: String Compression
Implement a string compression using python. For example, aaaabbbccddddddee would become a4b3c2d6e2. If the length of the string is not reduced, return the original string.
Requirements
Implement a compress function which accepts an input string and returns a compressed string. Code must be implemented using python 3.6 and must follow strictly pep8 rules.
Provide comments regarding the implementation.
Test Cases
assert compress(‘bbcceeee’) == ‘b2c2e4’
assert compress(‘aaabbbcccaaa’) == ‘a3b3c3a3’
assert compress(‘a’) = a
Explanation
Explain time complexity of the compression written.
"""


def compress(string):
    """
    This function compresses string with RunLength Compression algorithm.
    """

    index = 0
    compressed = ""
    len_str = len(string)
    while index < len_str:
        count = 1
        while (index < len_str - 1) and (string[index] == string[index + 1]):
            count += 1
            index += 1
        if count == 1:
            compressed += str(string[index])
        else:
            compressed += str(string[index]) + str(count)
        index += 1
    return compressed


if "__main__" == __name__:
    print("Test 1: bbcceee =", compress("bbcceeee"))
    assert compress("bbcceeee") == "b2c2e4"
    print("Test 2: aaabbbcccaaa =", compress("aaabbbcccaaa"))
    assert compress("aaabbbcccaaa") == "a3b3c3a3"
    print("Test 3: a =", compress("a"))
    assert compress("a") == "a"

"""
Explain time complexity of the compression written.

Even though two while loops are utilized in compress function string is traversed only once.
Since each character is compared with the next character only once, the time complexity is O(n).

Time Complexity: O(n)

"""
