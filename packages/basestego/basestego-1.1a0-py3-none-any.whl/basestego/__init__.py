import base64


BASE64_ALPHABET = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")


def get_allowed_bits(byte_seq: bytes) -> int:
    """Returns the count of bits in which we can hide an information.

    Arguments:
        byte_seq – byte sequence.
    """

    if len(byte_seq) % 3 == 0:
        return 0
    else:
        return (3 - len(byte_seq) % 3) * 2


def b64encode(byte_seq: bytes, number: int, slow_mode: bool = False) -> str:
    """Returns string in base64, contains the hidden number.

    Arguments:
        byte_seq – byte sequence that will be encoded,
        number – integer number for a hiding,
        slow_mode – working mode. Fast mode uses base64 module
            from Python library. Slow mode uses own implementation
            of base64 algorithm.
    """

    # How much bits/blocks we can write into the string
    # In case of blocks it equals to the count of equal signs
    bits_can_write = get_allowed_bits(byte_seq)
    blocks_can_write = bits_can_write // 2

    # Attempt to write more bits than allowed
    if bits_can_write < len(bin(number)[2:]):
        raise ValueError("Can't write {} bits in the string.".format(len(bin(number)[2:])))

    # Fast mode
    if not slow_mode:
        return _b64encode_fast(byte_seq, number)

    # List of bits we should hide
    bits_to_write = list(bin(number)[2:].zfill(bits_can_write))

    # List of blocks by 8 bits
    blocks8_list = [bin(byte)[2:].zfill(8) for byte in byte_seq]

    # Extending by useless blocks
    blocks8_list.extend(["00000000"] * blocks_can_write)

    # Convert from 8 bit blocks to 6 bit blocks
    binary_string = "".join(blocks8_list)
    blocks6_list = [binary_string[i:i + 6] for i in range(0, len(binary_string), 6)]

    # Modify block
    modify_block_idx = len(blocks6_list) - blocks_can_write - 1
    block_to_modify = list(blocks6_list[modify_block_idx])
    block_to_modify[-bits_can_write:] = bits_to_write
    blocks6_list[modify_block_idx] = "".join(block_to_modify)

    # Building base64 string
    encoded_list = [BASE64_ALPHABET[int(i, 2)] if int(i, 2) != 0 else "=" for i in blocks6_list]

    return "".join(encoded_list)


def _b64encode_fast(byte_seq: bytes, number: int) -> str:
    # Default base64 encoding (with number = 0)
    encoded_list = list(base64.b64encode(byte_seq).decode())

    # Bits are hidden in the last symbol before equal signs ("=")
    count_equals = encoded_list.count("=")
    last_symbol = encoded_list[-count_equals - 1]
    idx = BASE64_ALPHABET.index(last_symbol)

    # Hiding bits
    new_symbol = BASE64_ALPHABET[idx + number]
    encoded_list[-count_equals - 1] = new_symbol

    return "".join(encoded_list)


def b64decode(encoded_string: str) -> int:
    """Returns integer number, hidden in encoded_string (encoded in base64).

    Arguments:
        encoded_string – string, encoded in base64.
    """

    if "=" not in encoded_string:
        raise ValueError("There is no hidden bits.")

    # Bits are hidden in the last symbol before equal signs ("=")
    count_equals = encoded_string.count("=")
    count_hidden_bits = count_equals * 2
    last_symbol = encoded_string[-count_equals - 1]
    idx = BASE64_ALPHABET.index(last_symbol)

    return int(bin(idx)[2:][-count_hidden_bits:], 2)
