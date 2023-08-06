def primenumberinrange(d=None,b=None):
    '''
    This function returns all prime numbers in a region:
    d -> number of starts (default is 1, int)
    b -> the last number of the ending number (default is 1, int)
'''
    if (not ((type(b)==int and b>0 or b==None) and (type(d)==int and d>0 or d==None))): 
        raise TypeError('Must enter a positive integer or use the default value.')
    if b==None:
        b=1
    c=[]
    if b>d:
        for a in range(d,b):
            f=2
            while a//f*f!=a and a>f:
                f+=1
            if a!=1 and a==f:
                c+=[a]
    else:
        for a in range(b,d):
            f=2
            while a//f*f!=a and a>f:
                f+=1
            if a!=1 and a==f:
                c+=[a]
        c=c[::-1]
    return c
                

def isprimenumber(a):
    '''
    This function returns whether a is a prime number:
    a -> the number to be detected, int
'''
    if not (type(a)==int and a>0):
        raise TypeError('Must enter a positive integer.')
    f=2
    while a//f*f!=a and not(f>a):
        f+=1
    return (a!=1 and a==f)
def decompositionfactor(a):
    '''
This function can decompose a positive integer a by a prime factor:
    a-> a positive integer that needs to be decomposed,int
'''
    if type(a)!=int:
        raise TypeError('Must enter a number.')
    b,c,d=[],1,1
    while a!=1:
        c+=1
        if isprimenumber(c):
            while a//c*c==a:
                a/=c
                b+=[c]
                d*=c
    return b
def binaryconversion(number,newradix=2,a=['0','1','2','3','4','5','6','7','8','9',
                           'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                           'O','P','Q','R','S','T','U','V','W','X','Y','Z'],append=None,
         join=','):
    '''
This is a function for converting a numeric hex:
number -> Is N_arynumber or decimal number type, you can use N_arynumber(number, hexadecimal (default is 10), the list of characters or strings used (default is 0~9&A~Z), connector (default is ',') ,is_positive(kw,bool,default is True))
newradix -> The number of the number to convert to, the default is 2
a, append, join -> The character to be converted into a number, starting from 1, the default is 1~9&A~Z, input 'a' to append to the default list, and 'm' to use decimal digits in digits ( Of course, it is very possible to use join (the default is ', ') to separate digits)
    '''
    x=1
    if type(number)!=N_arynumber:
        raise TypeError('The type of number in binaryconversion() must be \'N_arynumber\', not %s.'%str(type(number))[7:-1])
    if type(newradix)!=int:
        raise TypeError('The type of newradix in binaryconversion() must be \'int\', not %s.'%str(type(newradix))[7:-1])
    if type(a)!=list and type(a)!=str:
        raise TypeError('The type of a in binaryconversion() must be \'list\' or \'str\', not %s.'%str(type(a))[7:-1])
    if type(append)!=list and append!=None:
        raise TypeError('The type of a in binaryconversion() must be \'list\' or \'NoneType\', not %s.'%str(type(a))[7:-1])
    if type(newradix)!=int:
        raise TypeError('The type of newradix in binaryconversion() must be \'int\', not %s.'%str(type(join))[7:-1])
    if '.' in number.number:
        x=N_arynumber(10**(len(number.number)-number.number.index('.')-1),number.Decimal)
        number=N_arynumber(number.number.replace('.', ''),number.Decimal,number.a,number.join)
    originalconnector=number.join
    originalradix=number.Decimal
    原a=number.a
    is_positive=number.is_positive()
    if not is_positive:
        number=N_arynumber(number.number[1:],originalradix,number.a,number.join)
    if a=='a':
        a=['0','1','2','3','4','5','6','7','8','9',
           'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
           'O','P','Q','R','S','T','U','V','W','X','Y','Z']+append
    if a=='m':
        a=[]
        if originalradix>newradix:
            z=originalradix
        else:
            z=newradix
        for i in range(0,z):
            a+=[str(i)]
    try:
        if originalconnector in number:
            number=number.split(originalconnector)
    except:
        pass 
    if originalradix!=10:
        新number=0
        for i in range(len(number.number)):
            新number+=int(number.number[-(i+1)])*(originalradix**i)
        number=新number
    if x != 1:
            number=N_arynumber(int(number)/int(x))
    if newradix==10:
        if type(number)==int:
            if is_positive:
                return N_arynumber(list(str(number)),newradix,a,join)
            else:
                return N_arynumber('-'+list(str(number)),newradix,a,join)
        else:
            return number
    else:
        number=int(number)
        新number=[]
        while number>=newradix:
            新number+=[str(number%newradix)]
            number//=newradix
        新number+=[str(number%newradix)]
        if is_positive:
            number=N_arynumber(新number[::-1],newradix,a,join)
        else:
            number=N_arynumber(['-']+新number[::-1],newradix,a,join)
    return number
class N_arynumber:
    '''
This category supports a+b, ab, a*b, a/b, a//b, a%b, a==b, a<b, a>b, a<=b, a>=b, a!=b, and support mixed with int type.
You can use self.number, self.strnumber, self.Decimal, self.a , self.join, self.is_positive to see the specific value.(see the description of binaryconversion for information on self)
Keyword parameters introduction:
    special_choice->Select 'a' or 'm' or None,
    'a': add on the default a (0~9&A~Z)
    'm': use decimal as the number on the digit
    '''
    def __init__(self,number,Decimal=10,a=['0','1','2','3','4','5','6','7','8','9',
                           'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                           'O','P','Q','R','S','T','U','V','W','X','Y','Z'],join='',**kw):
        if type(number)!=str and type(number)!=list and type(number)!=int:
            raise TypeError('The type of number in N_arynumber() must be \'str\' or \'list\' or \'int\', not %s.'%str(type(number))[7:-1])
        if type(Decimal)!=int:
            raise TypeError('The type of Decimal in N_arynumber() must be \'int\', not %s.'%str(type(Decimal))[7:-1])
        if a==None:
            a=['0','1','2','3','4','5','6','7','8','9',
               'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
               'O','P','Q','R','S','T','U','V','W','X','Y','Z']
        if type(a)!=list and a!=None:
            raise TypeError('The type of a in N_arynumber() must be \'list\', not %s.'%str(type(a))[7:-1])
        if type(join)!=str:
            raise TypeError('The type of join in N_arynumber() must be \'str\', not %s.'%str(type(join))[7:-1])
        if 'special_choice'in kw:
            if len(kw)>1:
                raise TypeError('"%s" is an invalid keyword argument for N_arynumber()'%list(kw)[1])
            if kw['special_choice']=='a':
                a=['0','1','2','3','4','5','6','7','8','9',
                   'A','B','C','D','E','F','G','H','I','J','K','L','M','N',
                   'O','P','Q','R','S','T','U','V','W','X','Y','Z']+a
            if kw['special_choice']=='m':
                a=[]
                for i in range(len(number)):
                    a+=[str(i)]
        else:
            if len(kw)>0:
                raise TypeError('"%s" is an invalid keyword argument for N_arynumber()'%list(kw)[0])
        if type(number)==int:
            number=list(str(number))
        if type(number)==str:
            if join!='':
                number=number.split(join)
            else:
                number=list(number)
            nself=number
            number=[]
            for i in range(len(nself)):
                if nself[i]=='-':
                    number+=['-']
                else:
                    number+=[a.index(nself[i])]
        self.number=number
        self.Decimal=Decimal
        self.a=a
        self.join=join
        b=[]
        for i in number:
            b+=[a[i]]
        self.strnumber=join.join(b)
    def is_positive(self):
        return self.number[0]!='-'
    def __add__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)+int(b)),a.Decimal,a.a,None,a.join)
    def __radd__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)+int(b)),a.Decimal,a.a,None,a.join)
    def __sub__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)-int(b)),a.Decimal,a.a,None,a.join)
    def __rsub__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)-int(b)),a.Decimal,a.a,None,a.join)
    def __mul__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)*int(b)),a.Decimal,a.a,None,a.join)
    def __rmul__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)*int(b)),a.Decimal,a.a,None,a.join)
    def __eq__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)==int(b)
    def __req__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)==int(b)
    def __ne__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)!=int(b)
    def __rne__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)!=int(b)
    def __int__(a):
        try:
            hh=binaryconversion(a,10).number
        except AttributeError:
            hh=str(binaryconversion(a,10))
        for i in range(len(hh)):
            hh[i]=str(hh[i])
        try:
            return int(''.join(hh))
        except ValueError:
            return 0
    def __float__(self):
        try:
            hh=binaryconversion(a,10).number
        except AttributeError:
            hh=str(binaryconversion(a,10))
        for i in range(len(hh)):
            hh[i]=str(hh[i])
        return float(int(''.join(hh)))
    def __lt__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)<int(b)
    def __rlt__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)<int(b)
    def __gt__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)>int(b)
    def __rgt__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)>int(b)
    def __le__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)<=int(b)
    def __rle__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)<=int(b)
    def __ge__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return int(a)>=int(b)
    def __rge__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return int(a)>=int(b)
    def __truediv__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)/int(b)),a.Decimal,a.a,None,a.join)
    def __rtruediv__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)/int(b)),a.Decimal,a.a,None,a.join)
    def __mod__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)%int(b)),a.Decimal,a.a,None,a.join)
    def __rmod__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)%int(b)),a.Decimal,a.a,None,a.join)
    def __floordiv__(a,b):
        if type(b)==int:
            b=N_arynumber(b)
        return binaryconversion(N_arynumber(int(a)%int(b)),a.Decimal,a.a,None,a.join)
    def __rfloordiv__(b,a):
        if type(a)==int:
            a=N_arynumber(a)
        return binaryconversion(N_arynumber(int(a)%int(b)),a.Decimal,a.a,None,a.join)
    def __str__(a):
        is_=a.is_positive()
        b=a.number
        if not is_:
            b=b[1:]
        c=[]
        for i in b:
            c+=[a.a[i]]
        新number=a.join.join(c)
        if not is_:
            新number='-'+新number
        return 'N_arynumber('+repr(新number)+','+str(a.Decimal)+','+str(a.a)+','+"'"+a.join+"'"+')'
    def __repr__(a):
        is_=a.is_positive()
        b=a.number
        if not is_:
            b=b[1:]
        c=[]
        for i in b:
            c+=[a.a[i]]
        新number=a.join.join(c)
        if not is_:
            新number='-'+新number
        return 'N_arynumber('+repr(新number)+','+str(a.Decimal)+','+str(a.a)+','+"'"+a.join+"'"+')'
    def __pos__(self):
        return self
    def __neg__(self):
        if self.is_positive():
            return N_arynumber(['-']+self.number,self.Decimal,self.a,self.join)
        else:
            return N_arynumber(self.number[1:],self.Decimal,self.a,self.join)
def comparison_list(a,b):
    '''
Compare lists a and b to output the same part.
    '''
    if type(a)!=type(b)!=list:
        raise TypeError('You must enter list.')
    c=[]
    for i in a:
        if i in b:
            del b[b.index(i)]
            c+=[i]
    return c
def gcd(*number):
    '''
Output the greatest common divisor of several numbers.
'''
    for i in number:
        if type(i)!=int:
            raise TypeError('You must enter int.')
    number2=[]
    for i in number:
        number2.append(decompositionfactor(i))
    i=number2[0]
    for i2 in number2[1:]:
        i=comparison_list(i,i2)
    i2=1
    for i3 in i:
        i2*=i3
    return i2
def lcm(*number):
    '''
Output the least common multiple of several numbers.
'''
    for i in number:
        if type(i)!=int:
            raise TypeError('You must enter int.')
    number2=[]
    for i in number:
        number2.append(decompositionfactor(i))
    i=number2[0]
    for i2 in number2[1:]:
        i=comparison_list(i,i2)
    i2=1
    for i3 in i:
        i2*=i3
    i3=1
    for i in number:
        i3*=i
    return int(i3/i2)
class Fraction:
    def __init__(self,molecule,Denominator):
        if type(Denominator)==float:
            while int(Denominator)!=Denominator:
                Denominator*=10
                molecule*=10
            Denominator=int(Denominator)
        if type(molecule)==float:
            while int(molecule)!=molecule:
                Denominator*=10
                molecule*=10
            molecule=int(molecule)
        if type(molecule)!=Fraction and type(Denominator)!=Fraction:
            a=gcd(Denominator,molecule)
            Denominator/=a
            molecule/=a
        if type(Denominator)!=Fraction:
            self.Denominator=int(Denominator)
        else:
            if Denominator.molecule==1:
                self.Denominator=Denominator.Denominator
            else:
                self.Denominator=Denominator
        if type(molecule)!=Fraction:
            self.molecule=int(molecule)
        else:
            self.molecule=molecule
        if Denominator==1:
            self=molecule
    def __repr__(self):
        a=(str(self.molecule)+'/'+str(self.Denominator)).split('/')
        while '1' in a[1:]:
            del a[1+a[1:].index('1')]
        return '/'.join(a)
    def __str__(self):
        a=(str(self.molecule)+'/'+str(self.Denominator)).split('/')
        while 1 in a[1:]:
            del a[1+a[1:].index(1)]
        return '/'.join(a)
    def __float__(self):
        return self.molecule/self.Denominator
    def __add__(a,b):
        if type(b)==int or type(b)==float:
            b=Fraction(1,b)
        Denominator=lcm(a.Denominator,b.Denominator)
        molecule=int(a.molecule*(lcm(a.Denominator,b.Denominator)/a.Denominator)+b.molecule*(lcm(a.Denominator,b.Denominator)/b.Denominator))
        return Fraction(Denominator,molecule)
    def __radd__(b,a):
        if type(a)==int or type(a)==float:
            b=Fraction(1,b)
        Denominator=lcm(a.Denominator,b.Denominator)
        molecule=int(a.molecule*(lcm(a.Denominator,b.Denominator)/a.Denominator)+b.molecule*(lcm(a.Denominator,b.Denominator)/b.Denominator))
        return Fraction(Denominator,molecule)
    def __sub__(a,b):
        if type(b)==int or type(b)==float:
            b=Fraction(1,b)
        Denominator=lcm(a.Denominator,b.Denominator)
        molecule=int(a.molecule*(lcm(a.Denominator,b.Denominator)/a.Denominator)-b.molecule*(lcm(a.Denominator,b.Denominator)/b.Denominator))
        return Fraction(Denominator,molecule)
    def __rsub__(b,a):
        if type(a)==int or type(a)==float:
            b=Fraction(1,b)
        Denominator=lcm(a.Denominator,b.Denominator)
        molecule=int(a.molecule*(lcm(a.Denominator,b.Denominator)/a.Denominator)-b.molecule*(lcm(a.Denominator,b.Denominator)/b.Denominator))
        return Fraction(Denominator,molecule)
    def __mul__(a,b):
        if type(b)==Fraction:
            return a*b.molecule/b.Denominator
        else:
            return Fraction(a.Denominator,a.molecule*b)
    def __rmul__(b,a):
        if type(a)==Fraction:
            return a*b.molecule/b.Denominator
        else:
            return Fraction(a.Denominator,a.molecule*b)
    def __truediv__(a,b):
        if type(b)==Fraction:
            return a/b.molecule*b.Denominator
        elif type(a.molecule/b)==int:
            return Fraction(a.Denominator,a.molecule/b)
        else:
            return Fraction(a.Denominator,Fraction(b,a.molecule))
    def __rtruediv__(a,b):
        if type(b)==Fraction:
            return a/b.molecule*b.Denominator
        elif type(a.molecule/b)==int:
            return Fraction(a.Denominator,a.molecule/b)
        else:
            return Fraction(a.Denominator,Fraction(b,a.molecule))
    def __lt__(a,b):
        return float(a)<float(b)
    def __rlt__(b,a):
        return float(a)<float(b)
    def __gt__(a,b):
        return float(a)>float(b)
    def __rgt__(b,a):
        return float(a)>float(b)
    def __le__(a,b):
        return float(a)<=float(b)
    def __rle__(b,a):
        return float(a)<=float(b)
    def __ge__(a,b):
        return float(a)>=float(b)
    def __rge__(b,a):
        return float(a)>=float(b)
    def __eq__(a,b):
        return float(a)==float(b)
    def __req__(b,a):
        return float(a)==float(b)
    def __ne__(a,b):
        return float(a)!=float(b)
    def __rne__(b,a):
        return float(a)!=float(b)
    
def 列竖式程序(_1,_2,运算程序):
    if 运算程序=='+':
        _1=str(_1).split('.')
        _2=str(_2).split('.')
        while len(_1[0])>len(_2[0]):
            _2[0]=' '+_2[0]
        while len(_1[0])<len(_2[0]):
            _1[0]=' '+_1[0]
        __1=' '.join(list('.'.join(_1)))
        __2=' '.join(list('.'.join(_2)))
        print('  '+__1)
        print('+ '+__2)
        a=[]
        if len(_1)<2:
            _1+=['0']
        if len(_2)<2:
            _2+=['0']
        if len(_1[1])>len(_2[1]):
            _2[1]=_2[1].ljust(len(_1[1]),'0')
        if len(_1[1])<len(_2[1]):
            _1[1]=_1[1].ljust(len(_1[1]),'0')
        for i in range(-1,-len(_1[1]),-1):
            e=0
            if float(_1[1][i].replace(' ','0'))+float(_2[1][i].replace(' ','0'))+e>=10:
                a+=['1']
                e=1
            else:
                e=0
                a+=[' ']
        a+=[' ']
        if len(_1[0])>len(_2[0]):
            _2[0]=_2[0].rjust(len(_2[0]),'0')
        if len(_1[0])<len(_2[0]):
            _1[0]=_1[0].rjust(len(_1[0]),'0')
        for i in range(-1,-len(_1[0]),-1):
            try:
                e
            except UnboundLocalError:
                e=0
            if float(_1[0][i].replace(' ','0'))+float(_2[0][i].replace(' ','0'))+e>=10:
                a+=['1']
                e=1
            else:
                a+=[' ']
                e=0
        print('   '+' '.join(a[::-1]))
        if len(''.join(__1))> len(''.join(__2)):
            print((len(''.join(__1))+2)*'-')
        else:
            print((len(''.join(__2))+2)*'-')
        _1add2=str(float('.'.join(_1))+float('.'.join(_2))).split('.')
        if len(_1add2[0])==len(_1[0]):
            _1add2[0]=' '+_1add2[0]
        print(' '.join(list('.'.join(_1add2))))
            
