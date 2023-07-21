def strtel():
    import re
    v=input("Enter the password:")
    if(bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})',v))==True):
        print("The password is strong")
    elif(bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})',v))==True):
        print("The password is weak")
    else:
        print("Password is less than 8 characters")
        
import hashlib

newpass = input("Enter the keyword: ")
webname = input("Enter the website name")
webname = webname.upper()

editpass = newpass.replace("a", "@").replace("k", "l<").replace("o","()")

print("Password is: ", newpass)
print("Edited password is: ", editpass)

temp = editpass[0:2]
sumnum = 0
for i in range(0,2):
    temp2 = ord(temp[i])
    sumnum = temp2 + sumnum

webname = webname[0:3]        
    
editpass = editpass + str(sumnum) + str(webname)

print("\n The required password is: ",editpass)

finalhash = hashlib.sha256(editpass.encode())

print("The hash password is: ", finalhash.hexdigest())
print("The short hash password is: ", finalhash.hexdigest()[0:15])
