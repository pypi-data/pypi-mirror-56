import random
import string
def isprime(num):
    if(num<0):
        raise Exception("must be a positive number")
    try:
        if(num==1 or num==0):
            return "not a prime number or a composite number"
        srnum=int(num**0.5+1)
        tem=srnum
        for i in range(srnum):
            if((num%tem) == 0):break
            tem-=1
        if(tem==1):return True
        else:return False
    except:
        raise Exception("unknown error")
def issquare(num):
    try:
        if(abs(num**0.5-int(num**0.5))<10**-10):return True
        else:return False
    except(TypeError):
        return "not an integer"
def fib(num):
    try:
        a, b = 1, 1
        for i in range(num - 1):
            a, b = b, a + b
        return a
    except:
        raise Exception("unknown errror")
class passwd:
    def random_method1(len1):
        a=""
        for i in range(int(len1)):
            a=a+random.choice(string.ascii_letters)
        return a
    def random_method2(len1):
        a=""
        for i in range(int(len1)):
            b=string.ascii_letters+string.digits
            a=a+random.choice(b)
        return a
    def level(string1):
        s=list(string1)
        ll=d=t=ul=0
        list1=r'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        length = len(string1)
        for items in s:
            if(items in string.ascii_lowercase):
                ll+=1
            if(items in string.ascii_uppercase):
                ul+=1
            if(items in string.digits):
                d+=1
            if (items in list1):
                t+=1
        st=passwd.levelstore(ll,ul,d,t,length)
        if (st >= 90): return "very good"
        elif (st >= 80): return "good"
        elif (st >= 70): return "very strong"
        elif (st >= 60): return "strong"
        elif (st >= 50): return "average"
        elif (st >= 25): return "low"
        else:return "too low"
    def levelstore(ll,ul,d,t,length):
        store=0
        if(d==1):store+=10
        elif(d>1):store+=20
        else:pass
        if(t==1):store+=10
        elif(t>1):store+=25
        else:pass
        if(ll==0 and ul==0):pass
        elif(ll!=0 and ul!=0):store+=20
        else:store+=1
        if(length<5):store+=5
        elif(length>4 and length<8):store+=10
        else:store+=20
        if(((ll and ul)and d) and t):store+=5
        elif(((ll or ul) and d) and t):store+=3
        else:store+=2
        return store
if __name__ == '__main__' :
    a = passwd.level("45279775836164")
    print(a)


