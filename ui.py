"""" used for user interaction / user experience related helper functions """

def warn(msg: str) -> None:
    """prints warning message into console / terminal when wrong user input

    Args:
        msg (str): information to be displayed as warning
    
    Returns:  
        None

    """

    print("WARNING: "+str(msg))