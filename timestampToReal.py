def timestampToReal(arr):
    l = len(arr);
    t = 0;
    for i in range(l-1):
        t += (arr[i]-2**7)*2**(7*(l-1-i));

    t += arr[l-1];

    ppHex = "[" + str(hex(arr[0]));
    for i in range(l-1):
        ppHex += ", " + str(hex(arr[i]));
    ppHex += "]:"
    print ppHex, t

    pp = "[" + str(arr[0]);
    for i in range(l-1):
        pp += ", " + str(arr[i]);
    pp += "]:"
    print pp    
    
    
a = [0x82, 0x80, 0x7F];
timestampToReal(a)