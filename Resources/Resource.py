from base64 import b64decode
from os.path import join as pathJoiner

def load_resource():
    files = ['icofi','lgfi']
    for file in files:
        with open(pathJoiner("Resources", f"{file}.dll"), 'rb') as f:
            data = f.read()
            if 'ico' in file:
                with open(pathJoiner("Resources", f"{file}.ico"), 'wb') as g:
                    g.write(b64decode(data))
            else:
                with open(pathJoiner("Resources", f"{file}.jpeg"), 'wb') as g:
                    g.write(b64decode(data))

if __name__ == '__main__':
    load_resource()