import jwt

header = {'typ':'JWT', 'alg':'HS256'}
payload = {'account': 'account'}
token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256', headers=header)

t = jwt.decode(token,'SECRET_KEY', algorithms=['HS256'])
print(t)