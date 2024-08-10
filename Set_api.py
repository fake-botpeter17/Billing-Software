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
    ch =1
    while ch!=3:
        ch = int(input("What do you want to do?\n\t1. Set new API Key\n\t2. View current API Key\n\t3. Exit\nYour Choice:\t"))
        match(ch):
            case 1:
                Set_api()
            case 2:
                print(view_API())
            case 3:
                print("Exiting...")
            case _:
                print("Invalid choice!!")