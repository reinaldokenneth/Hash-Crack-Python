import itertools
import math
import string
import multiprocessing
import hashlib
import traceback
import sys
import os

def hashstring(string,algo):
    return hashlib.new(algo,string.encode('utf-8')).hexdigest()

def gen_prod(prefix,charset,length):
    for string in itertools.product(charset,repeat=length):
        yield prefix+"".join(string)

def string_generator(prefix,hash,suffix_length,length,charset,hashalgo):
    if length <= suffix_length:
        assert prefix == ""
        for possible in gen_prod("",charset,length):
            if hashstring(possible,hashalgo)==hash:
                return possible
    else:
        assert len(prefix)+suffix_length==length
        for possible in gen_prod(prefix,charset,suffix_length):
            if hashstring(possible,hashalgo)==hash:
                return possible
    return None

def run_string_generator(*args):
    try:
        return string_generator(*args)
    except:
        raise
    Exception("".join(traceback.format_exception(*sys.exc_info())))

def hashing(pool,hash,charset,length,hashstring,spc=100000000):
    n=len(charset)
    suffix_len = int(math.ceil(math.log(spc)/math.log(n))-1)
    max_short_len = min(suffix_len,length)
    for length in range(1,max_short_len+1):
        result = pool.apply_async(run_string_generator,args=("",hash,suffix_len,length,charset,hashstring))
        if result.get()!=None:
            print('Plaintext ->',result.get())
            os._exit(1)
    for length in range(max_short_len+1,length+1):
        for prefix in gen_prod("",charset,length-suffix_len):
            result = pool.apply_async(run_string_generator,args=(prefix,hash,suffix_len,length,charset,hashstring))
            if result.get()!=None:
                print('Plaintext ->',result.get())
                os._exit(1)
    return "Plaintext not found.."

def parallel(hash,charset,length,hashstring="md5",spc=1000000,cores=None): #change cores used in cores
    pool = multiprocessing.Pool(cores)
    result = hashing(pool,hash,charset,length,hashstring,spc)
    pool.close()
    pool.join()
    return result

if __name__ == "__main__":
    print("Python MD5 BruteForce")
    #input hash
    code = input('Input hash [32 digit] -> ')
    print('please wait..')
    #process hash
    print(parallel(code,string.ascii_lowercase+string.digits,10,spc=100000000))