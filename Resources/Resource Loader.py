from base64 import b64decode

files = ['icofi','lgfi']
for file in files:
    with open(f"Resources\\{file}.dll", 'rb') as f:
        data = f.read()
        if 'ico' in file:
            with open(f"Resources\\{file}.ico", 'wb') as g:
                g.write(b64decode(data))
        else:
            with open(f"Resources\\{file}.jpeg", 'wb') as g:
                g.write(b64decode(data))