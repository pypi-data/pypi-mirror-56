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

if __name__ == '__main__' :
    a = passwd.random_method2(10)
    print(a)


