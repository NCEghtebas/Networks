"""
translator.py
-------------
Computer Networks SP15
Author: Nick Francisci

Description: A module meant to simplify the concept of the
modular bijection stack. The bijection stack here is effectively
a framework for encoding/decoding a message. Each stack layer is
able to encode on the way down, and decode on the way up. In this
way, custom encode/decode layers can be plugged into the stack.
"""


# ----- Full Bijection Stack Classes
class BJStack:
    """
    A template for a bijection stack which can be used to
    encode or decode messages. To use it, pass it a list
    of stack layers with common interfaces.
    """

    def __init__(self, layers):
        self.layers = layers

    def encode(self, message):
        for layer in self.layers:
            message = layer.descend(message)

        return message

    def decode(self, message):
        for layer in reversed(self.layers):
            message = layer.ascend(message)

        return message


class MorseBJStack(BJStack):
    """
    A no-assembly-required BJ stack for encoding an
    English alphanumeric message into a signal via morse.
    """

    def __init__(self):
        super().__init__([
            MsgLetterLayer(),
            LetterMorseLayer(),
            MorseSignalLayer()])


# ----- Stack Layer Classes
class StackLayer:
    """ A common interface for the stack-layer classes. """
    def __init__(self, function, inverse):
        self.descend = function
        self.ascend = inverse


class MsgLetterLayer(StackLayer):
    """ A stack-layer to transform a string message into
    a character array or visa-versa. """
    def __init__(self):
        super().__init__(msg2letters, letters2msg)


class LetterMorseLayer(StackLayer):
    """
    A stack-layer to transform a character array into
    an array of morse charcters (eg. ['e'] -> ['.']) or
    visa-versa.
    """

    def __init__(self):
        super().__init__(letters2morse, morse2letters)


class MorseSignalLayer(StackLayer):
    """
    A stack-layer to transform a morse character array into
    an array of binary packets (eg. ['.'] -> [(1, 1), (3, 0)])
    or visa-versa.
    """

    def __init__(self):
        super().__init__(morse2signal, signal2morse)


# ----- Message - Letter Functions
def msg2letters(msg):
    return list(msg)


def letters2msg(letters):
    return ''.join(letters)


# ----- Letter - Morse Functions

# Character - Morse Dictionaries
char2morse = {"A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----", ' ': ' '}
morse2char = {'---': 'O', '--.': 'G', '-...': 'B', '-..-': 'X', '.-.': 'R', '--.-': 'Q', '--..': 'Z', '.--': 'W', '..---': '2', '.-': 'A', '..': 'I', '-.-.': 'C', '..-.': 'F', '-.--': 'Y', '-': 'T', '.': 'E', '.-..': 'L', '...': 'S', '..-': 'U', '.----': '1', '-----': '0', '-.-': 'K', '-..': 'D', '----.': '9', '-....': '6', '.---': 'J', '.--.': 'P', '....-': '4', '--': 'M', '-.': 'N', '....': 'H', '---..': '8', '...-': 'V', '--...': '7', '.....': '5', '...--': '3', ' ': ' '}


def letters2morse(letters):
    return [char2morse[letter.upper()] for letter in letters]


def morse2letters(morse):
    return [morse2char[symbol] for symbol in morse]


# ----- Morse - Signal Functions

# Morse - Packet dictionaries
morse2sig = {'-': (3, 1), '.': (1, 1), ' ': (1, 0)}
sig2morse = {(3, 1): '-', (1, 1): '.', (7, 0): ' ', (1, 0): ''}


def morse2signal(morse):
    signal = []
    for char in morse:
        for ditdah in char:
            signal = ellide(signal, morse2sig[ditdah])

            # Add a (1, 0) packet after each dit or dah
            signal = ellide(signal, (1, 0))

        # Add a (2,0) packet between characters
        signal = ellide(signal, (2, 0))

    return signal


def ellide(signal, packet):
    """
    Helper for morse2signal which appends a zero-packet (eg. (1,0))
    to the end of the list or combines it with the previous packet if the
    previous packet was also a zero-packet.
    """

    # if the last packet was a zero packet
    if signal and not signal[-1][1] and not packet[1]:
        # then combine the current packet with the previous packet
        signal[-1] = (signal[-1][0] + packet[0], 0)
    else:
        signal.append(packet)

    return signal


def signal2morse(signal):
    morse = []
    temp_packet = ''

    for packet in signal:

        # Handle spaces
        if packet == (7, 0):
            morse.extend([temp_packet, ' '])
            temp_packet = ''

        # Handle character breaks
        elif packet == (3, 0):
            morse.append(temp_packet)
            temp_packet = ''

        # Translate dits and dahs
        else:
            temp_packet += sig2morse[packet]

    # Don't drop that last packet!
    if temp_packet:
        morse.append(temp_packet)

    return morse


# ----- Encode/Decode Test
if __name__ == "__main__":
    # Pre-Assembled Stack
    stack = MorseBJStack()
    message = "Test string"

    encoded = stack.encode(message)
    decoded = stack.decode(encoded)

    print("Encoding Test (Pre-Assembled): {}".format(encoded))
    print("Decoding Test (Pre-Assembled): {}".format(decoded))

    # Stack A La Carte
    stack = BJStack([MsgLetterLayer(), LetterMorseLayer(), MorseSignalLayer()])

    encoded = stack.encode(message)
    decoded = stack.decode(encoded)

    print("Encoding Test (A La Carte): {}".format(encoded))
    print("Decoding Test (A La Carte): {}".format(decoded))
