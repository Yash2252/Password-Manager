def strtel():
    import re
    v=input("Enter the password:")
    if(bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})',v))==True):
        print("The password is strong")
    elif(bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})',v))==True):
        print("The password is weak")
    else:
        print("Password is less than 8 characters")