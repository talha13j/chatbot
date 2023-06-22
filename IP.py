import socket
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
str1 = get_ip_address()
str2 = ''
i = 0
for x in range(len(str1)):
    if str1[x] == '.':
        str2 += str1[x]
        i += 1
    elif i == 3:
        break
    else:
        str2 += str1[x]

print(str2)