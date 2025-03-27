import _pickle as cPickle
import zlib

def compress_obj(obj):
    """
    Compresses any python object and stores as a byte array (which supports byte-array comparison).
    Stolen from https://stackoverflow.com/questions/19500530/compress-python-object-in-memory.

    Parameters
    ----------
    obj: Any
        The object to compress.

    Returns
    -------
    bytes
        The compressed object
    """
    return zlib.compress(cPickle.dumps(obj))

def decompress_obj(compressed_obj):
    """
    Decompresses a compressed object that was compressed using the method above.
    Stolen from https://stackoverflow.com/questions/19500530/compress-python-object-in-memory.

    Usage:
    >>> obj = {'something': 1}
    >>> compressed_obj = compress_obj(obj)
    >>> decompressed_obj = decompress_obj(compressed_obj)
    >>> obj == decompressed_obj

    True

    Parameters
    ----------
    compressed_obj: bytes
        The compressed object to decompress.

    Returns
    -------
    Any
        The decompressed object.
    """
    return cPickle.loads(zlib.decompress(compressed_obj))