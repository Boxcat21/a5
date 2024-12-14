def brute (g, n, gx, gy):
    print ("Intercepted base of", g)
    print ("Intercepted modulus of", n)
    print ("Intercepted one pub key as", gx)
    print ("Intercepted other pub key as", gy)

    for y in range(0, n - 1):
        if pow(g, y, n) == gy:
            print("Sneakily found shared secret of ", pow(gx, y, n))
            break

brute(328230196, 998244353, 785078719, 551926271)