def get_Api(testing: bool = False) -> str:
    """Returns the API URL for the server"""
    if testing:
        return "http://127.0.0.1:5000"
    from pickle import load

    with open("Resources\\sak.dat", "rb") as file:
        return load(file).decode("utf-32")