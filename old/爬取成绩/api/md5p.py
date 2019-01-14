import hashlib
def GetUltraP(origin_p):
    temp = str(origin_p)
    m = hashlib.md5()
    m.update(temp.encode('utf-8'))
    return m.hexdigest()

if __name__ == '__main__':
    a = GetUltraP(1709404067)
    print(a)