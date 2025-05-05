from pickle import dump,load
from os.path import join as pathJoiner

def Set_api(api_key: str) -> None:
    with open(pathJoiner("Resources", "sak.dat"), 'wb') as file:
        #return load(file).decode("utf-32")
        data = api_key.encode("utf-32")
        dump(data, file)
    print("Set successfully!!")

def view_API() -> None:
    with open(pathJoiner("Resources", "sak.dat"), 'rb') as file:
        return load(file).decode("utf-32")
    
if __name__ == '__main__':
    ch =1
    while ch!=3:
        ch = int(input("What do you want to do?\n\t1. Set new API Key\n\t2. View current API Key\n\t3. Exit\nYour Choice:\t"))
        match(ch):
            case 1:
                try:
                    api_key = input("Enter the new API key: ")
                    if not api_key:
                        raise ValueError("API key cannot be empty")
                    Set_api(api_key)
                except ValueError as e:
                    print(e)
            case 2:
                print(view_API())
            case 3:
                print("Exiting...")
            case _:
                print("Invalid choice!!")