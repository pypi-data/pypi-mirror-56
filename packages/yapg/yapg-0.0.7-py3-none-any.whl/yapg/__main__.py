#!/usr/bin/env python

"""
Simple password generator
"""

from argparse import ArgumentParser
from secrets import choice
from math import log10
from statistics import mean
from string import ascii_letters
from sys import exit as sysexit
from zxcvbn import zxcvbn

DIGITS_TRANSFORMS = {
    'o': '0',
    'i': '1',
    'l': '1',
    'e': '3',
    'a': '4',
    's': '5',
    't': '7'
}
SPECIALS_TRANSFORMS = {'p': '%', 'a': '@', 'e': '€', 'l': 'ł', 's': '$'}
DEFAULT_LENGTH = 12
DEFAULT_WORDS = 3
DEFAULT_COMPLEXITY = 18
DEFAUT_DICTIONARY = 'dictionary.txt'


def transform(word: str) -> str:
    """
    Executes simple transforms to the word to add complexity and return it.
    """
    letters = list(word)
    for i in range(len(letters) - 1, 0, -1):
        if letters[i] in ascii_letters:
            letters[i] = letters[i].upper()
            break
    for i, letter in enumerate(letters):
        if letter.lower() in DIGITS_TRANSFORMS:
            letters[i] = DIGITS_TRANSFORMS[letter.lower()]
            break
    for i, letter in enumerate(letters):
        if letter.lower() in SPECIALS_TRANSFORMS:
            letters[i] = SPECIALS_TRANSFORMS[letter.lower()]
            break
    return ''.join(letters)


def generate_password(length: int = DEFAULT_LENGTH,
                      words: int = DEFAULT_WORDS,
                      complexity: int = DEFAULT_COMPLEXITY,
                      dictionary: str = DEFAUT_DICTIONARY) -> str:
    """
    Generates a password of minimum length length,
    of minimum number of words words,
    using random words from dictionary.
    The complexity is the order of magnitude
    of the number of possible passwords.
    """
    try:
        with open(dictionary) as dictionary_file:
            wordlist = [line.strip() for line in dictionary_file]
    except OSError as error:
        print(error)
        sysexit(0)
    lengths = [len(word) for word in wordlist]
    mean_length = mean(lengths)
    while log10(len(wordlist)**words) < complexity or (length - words +
                                                       1)/words > mean_length:
        words += 1
    password = ' '
    while len(password) < length or zxcvbn(
            password)['guesses_log10'] < complexity:
        password = ' '.join(
            [transform(choice(wordlist)) for i in range(words)])
    return password


def main() -> None:
    """
    Main body of the module
    """
    parser = ArgumentParser(description="Simple password generator")
    parser.add_argument("-l",
                        "--length",
                        type=int,
                        default=DEFAULT_LENGTH,
                        help="The minimum length of the generated password, \
        defaults to {} characters. If the length is set arbitrarily high, \
        the number of words will be increased."
                        .format(DEFAULT_LENGTH))
    parser.add_argument(
        "-w",
        "--words",
        type=int,
        default=DEFAULT_WORDS,
        help="The minimum number of words in the generated password, \
        defaults to {} words.\
        Warning: if the dictionary is too small, the password \
        will be longer to respect the complexity requirement!\
        Also, the number of words will be increased to comply\
        with the required length if necessary".format(DEFAULT_WORDS))
    parser.add_argument(
        "-c",
        "--complexity",
        type=int,
        default=DEFAULT_COMPLEXITY,
        help="The minimum order of magnitude of guesses required to \
        find the password, defaults to {0} (meaning that one would need to \
        guess at least 10^{0} times to find the password, which would \
        take about one year and a half to break if an attacker tries \
        a hundred billion words per second) \
        Warning: if the dictionary is too small, the password \
        will be longer to respect the complexity requirement!".format(
            DEFAULT_COMPLEXITY))
    parser.add_argument("-d",
                        "--dictionary",
                        type=str,
                        default=DEFAUT_DICTIONARY,
                        help="The path to the dictionary file to use \
        for the construction of the password. \
        The number of words in the dictionary is very important! \
        More words = higher number of possible passwords = more complexity.\
        This means we do not have to increase the password length to\
        respect the complexity requirement.\
        Defaults to {}".format(DEFAUT_DICTIONARY))
    args = parser.parse_args()
    print(
        generate_password(args.length, args.words, args.complexity,
                          args.dictionary))


if __name__ == "__main__":
    main()
