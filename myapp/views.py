
from django.shortcuts import render
from django.http import HttpResponse
from math import e, sin, cos, tan


def index(req):
    return render(req, 'myapp/index.html')

def test(req):
    return render(req, 'myapp/test.html')


def p32(req):
    if req.method == 'POST':
        d = float(req.POST.get('x'))

        nb = bin(int(d))
        lung = d - int(d)

        bilung = ''

        count = 0
        while(lung != 0):
            lung *= 2
            bilung = bilung+str(int(lung))
            lung -= int(lung)
            count += 1
            if count == 17:
                break

        nb = nb[2:]
        e = len(nb)-1

        s = '0' if d >= 0 else '1'
        e += 127
        bie = bin(e)

        nbbilung = nb+bilung
        bie = bie[2:]
        nbbilung = nbbilung[1:]
        bx = s+bie+nbbilung
        b = bx + '0'*(32-len(bx))

        s = b[0]
        e = b[1:9]
        f = b[9:33]

        return render(req, 'myapp/p32.html', {'s': s, 'e': e, 'f': f, 'd': d})
    else:
        return render(req, 'myapp/p32.html')


def p64(req):
    if req.method == 'POST':
        d = float(req.POST.get('x'))
        nb = bin(int(d))
        lung = d - int(d)

        bilung = ''

        count = 0
        while(lung != 0):
            lung *= 2
            bilung = bilung+str(int(lung))
            lung -= int(lung)
            count += 1
            if count == 44:
                break

        nb = nb[2:]
        e = len(nb)-1

        s = '0' if d >= 0 else '1'
        e += 1023
        bie = bin(e)

        nbbilung = nb+bilung
        bie = bie[2:]
        nbbilung = nbbilung[1:]
        bx = s+bie+nbbilung
        b = bx + '0'*(64-len(bx))

        s = b[0]
        e = b[1:12]
        f = b[12:65]

        return render(req, 'myapp/p64.html', {'s': s, 'e': e, 'f': f, 'd': d})
    else:
        return render(req, 'myapp/p64.html')


def solve(A, b):
    import numpy as np
    a, b = np.array(A), np.array(b)
    n = len(A[0])
    x = np.array([0]*n)

    for k in range(0, n-1):
        # 1
        for j in range(k+1, n):
            if a[j, k] != 0.0:
                lam = a[j][k]/a[k][k]
                a[j, k:n] = a[j, k:n] - lam*a[k, k:n]
                b[j] = b[j] - lam*b[k]
# 2
    for k in range(n-1, -1, -1):
        x[k] = (b[k] - np.dot(a[k, k+1:n], x[k+1:n]))/a[k, k]
    return x.flatten()
# แก้ระบบสมการเชิงเส้น $Ax = b$
    # pass


def datasolve(req):
    if req.method == 'POST':
        matrix_y = []
        matrix_x = []
        data = req.POST.get('data')
        #x = data.split(',')
        data2 = data.split('\n')
        for i in data2:
            y = [float(i.split('=')[-1])]
            matrix_y.append(y)
            x = (i.split('=')[0]).split(',')
            matrix_x.append(list(map(float, x)))

        results = solve(matrix_x, matrix_y)
        mylist = zip(matrix_x, matrix_y)
    try:
        return render(req, 'myapp/solve.html', {'mylist': mylist, 'results': results})
    except:
        return render(req, 'myapp/solve.html')


def f(x, fx):
    return eval(fx)


def d2(x, dx):
    return eval(dx)


def sign(x):
    return 1 if x > 0 else -1


def diff(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        x = eval(req.POST.get('x'))
        h = eval(req.POST.get('h'))

        re1 = (f(x+h, fx) - f(x-h, fx))/(2*h)
        re2 = (f(x+h, fx) - 2*f(x, fx)+f(x-h, fx))/(h**2)
        re3 = (f(x+2*h, fx) - 2*f(x+h, fx) + 2 *
               f(x-h, fx) - f(x-2*h, fx))/2*h**3
        re4 = (f(x+2*h, fx) - 4*f(x+h, fx) + 6*f(x, fx) -
               4*f(x-h, fx) + f(x-2*h, fx)) / h**4

        print(f'fu={function} fx={fx} x={x} h={h} re1={re1}')
        return render(req, 'myapp/diff.html', {'re1': re1, 're2': re2, 're3': re3, 're4': re4})
    return render(req, 'myapp/diff.html')


def integrat(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(f, function)
        if function == 'trapezoidal':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(1, n)])

            x = sum(I)*h/2

            return render(req, 'myapp/integrat.html', {'x': x})
        elif function == 'simson':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(2, n, 2)])
            I.extend([4*f(a+i*h, fx) for i in range(1, n, 2)])
            x = sum(I)*h/3
            return render(req, 'myapp/integrat.html', {'x': x})
    return render(req, 'myapp/integrat.html')


def rootfinding(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(function, fx)
        if function == 'incremental':
            epsilon = 10**-2
            step = 10**-4
            x = -3
            n = 0
            while abs(f(x, fx)-0) > epsilon:
                x += step
                n += 1
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'bisection':
            x = 0
            a = -2
            b = 1
            eps = 10**-3
            count = 0
            while True:
                count += 1
                m = (a+b)/2
                if abs(f(m, fx)-0) < eps:
                    print(f'หาค่าต่ำสุดเจอแล้วx = {m}')
                    print(f'จำนวนครั้ง{count}')
                    x = m
                    break
                else:
                    if sign(f(a, fx)) == sign(f(m, fx)):
                        a = m
                        print(f'ขยับ a ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
                    else:
                        b = m
                        print(f'ขยับ b ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'newton':
            dxx = req.POST.get('dx')
            x = 0
            a = -1.5
            b = 1
            epsilon = 10**-4
            x = (a+b)/2
            n = 0
            dx = 1000000000000000
            while abs(dx) > epsilon:
                dx = -f(x, fx)/d2(x, dxx)
                x = dx
                n += 1
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'secant':
            x = -1
            n = 20
            h = 0.0000001
            for i in range(n):
                Qx = (f(x+h, fx) - f(x, fx)) / h
                dx = - f(x, fx)/Qx
                x = x+dx
            return render(req, 'myapp/Rootfinding.html', {'x': x})
    return render(req, 'myapp/Rootfinding.html')


def diff(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        x = eval(req.POST.get('x'))
        h = eval(req.POST.get('h'))

        re1 = (f(x+h, fx) - f(x-h, fx))/(2*h)
        re2 = (f(x+h, fx) - 2*f(x, fx)+f(x-h, fx))/(h**2)
        re3 = (f(x+2*h, fx) - 2*f(x+h, fx) + 2 *
               f(x-h, fx) - f(x-2*h, fx))/2*h**3
        re4 = (f(x+2*h, fx) - 4*f(x+h, fx) + 6*f(x, fx) -
               4*f(x-h, fx) + f(x-2*h, fx)) / h**4
        print(f'fu={function} fx={fx} x={x} h={h} re1={re1}')
        return render(req, 'myapp/Diff.html', {'re1': re1, 're2': re2, 're3': re3, 're4': re4})
    return render(req, 'myapp/Diff.html')


def integrat(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(f, function)
        if function == 'trapezoidal':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(1, n)])

            x = sum(I)*h/2

            return render(req, 'myapp/Integrat.html', {'x': x})
        elif function == 'simson':
            a = 1
            b = 2
            n = 12

            h = (b - a)/n
            I = [f(a, fx), f(b, fx)]
            I.extend([2*f(a+i*h, fx) for i in range(2, n, 2)])
            I.extend([4*f(a+i*h, fx) for i in range(1, n, 2)])
            x = sum(I)*h/3
            return render(req, 'myapp/Integrat.html', {'x': x})
    return render(req, 'myapp/Integrat.html')


def rootfinding(req):
    if req.method == 'POST':
        function = req.POST.get('function')
        fx = req.POST.get('fx')
        print(function, fx)
        if function == 'incremental':
            epsilon = 10**-2
            step = 10**-4
            x = -3
            n = 0
            while abs(f(x, fx)-0) > epsilon:
                x += step
                n += 1
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'bisection':
            x = 0
            a = -2
            b = 1
            eps = 10**-3
            count = 0
            while True:
                count += 1
                m = (a+b)/2
                if abs(f(m, fx)-0) < eps:
                    print(f'หาค่าต่ำสุดเจอแล้วx = {m}')
                    print(f'จำนวนครั้ง{count}')
                    x = m
                    break
                else:
                    if sign(f(a, fx)) == sign(f(m, fx)):
                        a = m
                        print(f'ขยับ a ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
                    else:
                        b = m
                        print(f'ขยับ b ช่วงค่าใหม่ที่ต้องค้นหาคือ ({a}, {b})')
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'newton':
            dxx = req.POST.get('dx')
            x = 0
            a = -1.5
            b = 1
            epsilon = 10**-4
            x = (a+b)/2
            n = 0
            dx = 1000000000000000
            while abs(dx) > epsilon:
                dx = -f(x, fx)/d2(x, dxx)
                x = dx
                n += 1
            return render(req, 'myapp/Rootfinding.html', {'x': x})
        elif function == 'secant':
            x = -1
            n = 20
            h = 0.0000001
            for i in range(n):
                Qx = (f(x+h, fx) - f(x, fx)) / h
                dx = - f(x, fx)/Qx
                x = x+dx
            return render(req, 'myapp/Rootfinding.html', {'x': x})
    return render(req, 'myapp/Rootfinding.html')

# Create your views here.
