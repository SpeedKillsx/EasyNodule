import re



def isValid(email):
    regex = re.compile(r"^\w+@\w+\.\w+$")
    if re.fullmatch(regex, email):
        return 1
    else:
        return 0

print("amayas88@com.fr est : ", isValid("amayas88@com.fr"))
print("amayaslabchri88@gmail.fr est : ", isValid("amayaslabchri88@gmail.fr"))
print("amayas88.@com.fr est : ", isValid("amayas88.@com.fr"))
print("amayas88@.fr est : ", isValid("amayas88@.fr"))
print("amayas88_5@com.fr est : ", isValid("amayas88_5@com.fr"))
print("amayaslabchri88@.gmail.fr est : ", isValid("amayaslabchri88@.gmail.fr"))
print("amayas.labchr@.ent.usthb.fr est : ", isValid("amayas.labchr@.ent.usthb.fr"))