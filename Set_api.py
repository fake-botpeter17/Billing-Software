from pickle import dump,load

def Set_api():
    key = input("Enter the new API Key: ")
    with open("Resources\\sak.dat", 'wb') as file:
        #return load(file).decode("utf-32")
        data = key.encode("utf-32")
        dump(data, file)
    print("Set successfully!!")

def view_API():
    with open("Resources\\sak.dat", 'rb') as file:
        return load(file).decode("utf-32")
    
if __name__ == '__main__':
    print(view_API())
    #Set_api()