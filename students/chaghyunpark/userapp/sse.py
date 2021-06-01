import bcrypt

data = bcrypt.hashpw('123', bcrypt.gensalt())
print(data)