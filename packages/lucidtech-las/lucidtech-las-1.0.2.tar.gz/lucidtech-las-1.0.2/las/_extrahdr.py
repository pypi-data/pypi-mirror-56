from os import PathLike


def extra_what(file, h=None):
    """Code mostly copied from imghdr.what"""
    tests = []

    def test_pdf(h, f):
        if b'PDF' in h[0:10]:
            return 'pdf'

    tests.append(test_pdf)

    f = None
    try:
        if h is None:
            if isinstance(file, (str, PathLike)):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f:
            f.close()
    return None
