#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#=======================================================================
#
# sha512.py
# ---------
# Simple, pure Python model of the SHA-512 hash function. Used as a
# reference for the HW implementation. The code follows the structure
# of the HW implementation as much as possible.
#
#
# Author: Joachim Strömbergson
# Copyright (c) 2013 Secworks Sweden AB
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Python module imports.
#-------------------------------------------------------------------
import sys


#-------------------------------------------------------------------
# Constants.
#-------------------------------------------------------------------
# Hash modes supported.
MODE_SHA_512_224 = 0
MODE_SHA_512_256 = 1
MODE_SHA_284     = 2
MODE_SHA_512     = 3


#-------------------------------------------------------------------
# ChaCha()
#-------------------------------------------------------------------
class SHA512():
    def __init__(self, verbose = 0):
        self.verbose = verbose
        self.H = [0] * 8
        self.t1 = 0
        self.t2 = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.w = 0
        self.W = [0] * 16
        self.k = 0
        self.K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
                  0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
                  0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
                  0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
                  0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
                  0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
                  0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
                  0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
                  0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]
        
        
    def init(self, mode):
        if mode == MODE_SHA_512_224:
            self.H = [0x8c3d37c819544da2, 0x73e1996689dcd4d6,
                      0x1dfab7ae32ff9c82, 0x679dd514582f9fcf,
                      0x0f6d2b697bd44da8, 0x77e36f7304c48942,
                      0x3f9d85a86a1d36c8, 0x1112e6ad91d692a1]

        elif mode == MODE_SHA_512_256:
            self.H = [0x22312194fc2bf72c, 0x9f555fa3c84c64c2, 
                      0x2393b86b6f53b151, 0x963877195940eabd, 
                      0x96283ee2a88effe3, 0xbe5e1e2553863992, 
                      0x2b0199fc2c85b8aa, 0x0eb72ddc81c52ca2]
                      
        elif mode == MODE_SHA_384:
            self.H = [0xcbbb9d5dc1059ed8, 0x629a292a367cd507,
                      0x9159015a3070dd17, 0x152fecd8f70e5939, 
                      0x67332667ffc00b31, 0x8eb44a8768581511, 
                      0xdb0c2e0d64f98fa7, 0x47b5481dbefa4fa4]

        elif mode == MODE_SHA_512:
            self.H = [0x6a09e667f3bcc908, 0xbb67ae8584caa73b,
                      0x3c6ef372fe94f82b, 0xa54ff53a5f1d36f1, 
                      0x510e527fade682d1, 0x9b05688c2b3e6c1f, 
                      0x1f83d9abfb41bd6b, 0x5be0cd19137e2179]

        else:
            print "Unknown mode!"
        

    def next(self, block):
        self._W_schedule(block)
        self._copy_digest()
        if self.verbose:
            print("State after init:")
            self._print_state(0)

        for i in range(64):
            self._sha512_round(i)
            if self.verbose:
                self._print_state(i)

        self._update_digest()


    def get_digest(self):
        return self.H


    def _copy_digest(self):
        self.a = self.H[0] 
        self.b = self.H[1] 
        self.c = self.H[2] 
        self.d = self.H[3] 
        self.e = self.H[4] 
        self.f = self.H[5] 
        self.g = self.H[6] 
        self.h = self.H[7]
    
    
    def _update_digest(self):
        self.H[0] = (self.H[0] + self.a) & 0xffffffff 
        self.H[1] = (self.H[1] + self.b) & 0xffffffff 
        self.H[2] = (self.H[2] + self.c) & 0xffffffff 
        self.H[3] = (self.H[3] + self.d) & 0xffffffff 
        self.H[4] = (self.H[4] + self.e) & 0xffffffff 
        self.H[5] = (self.H[5] + self.f) & 0xffffffff 
        self.H[6] = (self.H[6] + self.g) & 0xffffffff 
        self.H[7] = (self.H[7] + self.h) & 0xffffffff 


    def _print_state(self, round):
        print("State at round 0x%02x:" % round)
        print("t1 = 0x%08x, t2 = 0x%08x" % (self.t1, self.t2))
        print("k  = 0x%08x, w  = 0x%08x" % (self.k, self.w))
        print("a  = 0x%08x, b  = 0x%08x" % (self.a, self.b))
        print("c  = 0x%08x, d  = 0x%08x" % (self.c, self.d))
        print("e  = 0x%08x, f  = 0x%08x" % (self.e, self.f))
        print("g  = 0x%08x, h  = 0x%08x" % (self.g, self.h))
        print("")


    def _sha512_round(self, round):
        self.k = self.K[round]
        self.w = self._next_w(round)
        self.t1 = self._T1(self.e, self.f, self.g, self.h, self.k, self.w)
        self.t2 = self._T2(self.a, self.b, self.c)
        self.h = self.g
        self.g = self.f
        self.f = self.e
        self.e = (self.d + self.t1) & 0xffffffff
        self.d = self.c
        self.c = self.b
        self.b = self.a
        self.a = (self.t1 + self.t2) & 0xffffffff


    def _next_w(self, round):
        if (round < 16):
            return self.W[round]

        else:
            tmp_w = (self._delta1(self.W[14]) +
                     self.W[9] + 
                     self._delta0(self.W[1]) +
                     self.W[0]) & 0xffffffff
            for i in range(15):
                self.W[i] = self.W[(i+1)]
            self.W[15] = tmp_w
            return tmp_w


    def _W_schedule(self, block):
        for i in range(16):
            self.W[i] = block[i]


    def _Ch(self, x, y, z):
        return (x & y) ^ (~x & z)


    def _Maj(self, x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    def _sigma0(self, x):
        return (self._rotr32(x, 2) ^ self._rotr32(x, 13) ^ self._rotr32(x, 22))


    def _sigma1(self, x):
        return (self._rotr32(x, 6) ^ self._rotr32(x, 11) ^ self._rotr32(x, 25))


    def _delta0(self, x):
        return (self._rotr32(x, 7) ^ self._rotr32(x, 18) ^ self._shr32(x, 3))


    def _delta1(self, x):
        return (self._rotr32(x, 17) ^ self._rotr32(x, 19) ^ self._shr32(x, 10))
    

    def _T1(self, e, f, g, h, k, w):
        return (h + self._sigma1(e) + self._Ch(e, f, g) + k + w) & 0xffffffff


    def _T2(self, a, b, c):
        return (self._sigma0(a) + self._Maj(a, b, c)) & 0xffffffff


    def _rotr32(self, n, r):
        return ((n >> r) | (n << (32 - r))) & 0xffffffff

    
    def _shr32(self, n, r):
        return (n >> r)


def compare_digests(digest, expected):
    if (digest != expected):
        print("Error:")
        print("Got:")
        print(digest)
        print("Expected:")
        print(expected)
    else:
        print("Test case ok.")
        
    
#-------------------------------------------------------------------
# main()
#
# If executed tests the ChaCha class using known test vectors.
#-------------------------------------------------------------------
def main():
    print("Testing the SHA-512 Python model.")
    print("---------------------------------")
    print

    my_sha512 = SHA512(verbose=1);

    # TC1: NIST testcase with message "abc"
    TC1_block = [0x61626380, 0x00000000, 0x00000000, 0x00000000, 
                 0x00000000, 0x00000000, 0x00000000, 0x00000000,
                 0x00000000, 0x00000000, 0x00000000, 0x00000000,
                 0x00000000, 0x00000000, 0x00000000, 0x00000018]
    
    TC1_expected = [0xBA7816BF, 0x8F01CFEA, 0x414140DE, 0x5DAE2223,
                    0xB00361A3, 0x96177A9C, 0xB410FF61, 0xF20015AD]
    
    my_sha512.init()
    my_sha512.next(TC1_block)
    my_digest = my_sha512.get_digest()
    compare_digests(my_digest, TC1_expected)

    

#-------------------------------------------------------------------
# __name__
# Python thingy which allows the file to be run standalone as
# well as parsed from within a Python interpreter.
#-------------------------------------------------------------------
if __name__=="__main__": 
    # Run the main function.
    sys.exit(main())

#=======================================================================
# EOF sha512.py
#=======================================================================