import binascii, struct
import xxhash

def hashFNV(name):
    while True:
        s = name.encode("utf-8")
        
        fnv_offset = 0xcbf29ce484222325
        fnv_prime = 0x100000001b3
        h = fnv_offset
        for c in s:
            h ^= c
            h = (h * fnv_prime) & 0xFFFFFFFFFFFFFFFF
        
        finalValue = h.to_bytes(8, 'little').hex()
    
        return(finalValue)