import os


class File:
    @staticmethod
    def read(filename):
        f = open(filename, 'r')
        c = f.read()
        f.close()
        return c

    @staticmethod
    def write(filename, text, is_append = False):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename), 0o777)
        if is_append:
            f = open(filename, 'a')
        else:
            f = open(filename, 'w')
        f.write(str(text))
        f.close()
