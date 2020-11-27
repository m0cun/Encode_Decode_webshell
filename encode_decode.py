# python2.7
# -*- coding: utf-8 -*-

import argparse
import chardet
import cgi
import base64
import urllib
from HTMLParser import HTMLParser
from Crypto.Cipher import AES
import re
import zipfile
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

info = '''
    Usage: %prog -s|-f target_string|target_filename
    e.g.1 HTML    encode:\tpython encode_decode.py -s "<div> </div>"
    e.g.2 URL     encode:\tpython encode_decode.py -s http://www.baidu.com
    e.g.3 ASCII   encode:\tpython encode_decode.py -s 97
    e.g.4 Unicode encode:\tpython encode_decode.py -f behinder_jsp.txt 
    e.g.5 Base64  encode:\tpython encode_decode.py -s abcdef
    Warning: Terminal is windows cmd and chcp 936
'''

choice = 12

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:  # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def information():
    print "*" * 73
    print "*\t1st:  HTML     encode\t\t2nd:  HTML     decode\t\t*"
    print "*\t3rd:  URL      encode\t\t4th:  URL      decode\t\t*"
    print "*\t5th:  ASCII    encode\t\t6th:  ASCII    decode\t\t*"
    print "*\t7th:  Unicode  encode\t\t8th:  Unicode  decode\t\t*"
    print "*\t9th:  Base64   encode\t\t10th: Bade64   decode\t\t*"
    print "*\t11th: Behinder JSP decode\t12th: Behinder PHP decode\t*"
    print "*" * 73 + "\n"


def format_output(string):
    print '*' * 73
    print 'The original string is :\n%s' % string
    print '*' * 73


def html_encode_format_output(string):
    print 'The string HTML encode is :'
    print cgi.escape(string)
    print '*' * 73


def html_decode_format_output(string):
    print 'The string HTML decode is :'
    print HTMLParser().unescape(string)
    print '*' * 73


def url_encode_format_output(string):
    print 'The string URL encode is :'
    print urllib.quote(string)
    print '*' * 73


def url_decode_format_output(string):
    print 'The string URL decode is :'
    print urllib.unquote(string)
    print '*' * 73


def ascii_encode_format_output(string):
    print 'The integer ASCII encode is :'
    print chr(int(string))
    print '*' * 73


def ascii_decode_format_output(string):
    print 'The character ASCII decode is :'
    print ord(string)
    print '*' * 73


def unicode_encode_format_output(string):
    print 'The string Unicode encode is :'
    print "chinese or number decode is :"
    print string.decode('gbk').encode('unicode_escape')
    print '*' * 73


def unicode_decode_format_output(string):
    print 'The string Unicode decode is :'
    print string.decode('gbk').decode('unicode_escape')
    print '*' * 73


def base64_encode_format_output(string):
    print 'The string Base64 encode is :'
    print base64.b64encode(string)
    print '*' * 73


def base64_decode_format_output(string):
    print 'The string Base64 decode is :'
    print base64.b64decode(string)
    print '*' * 73

def aes_decode_ECB(data,key):
    try:
        aes = AES.new(str.encode(key),AES.MODE_ECB)
        decrypted_text = aes.decrypt(data)
        # decrypted_text = decrypted_text[:-(decrypted_text[-1])]
    except Exception as e:
        print e
    return decrypted_text

def aes_decode_CBC(data,key):
    try:
        aes = AES.new(str.encode(key),AES.MODE_CBC)
        decrypted_text = aes.decrypt(data)
    except Exception as e:
        print e
    return decrypted_text

def behinder_jsp_decode(string,key):
    data = base64.b64decode(string)
    a = aes_decode_ECB(data,key)
    # a = a[:-(a[-1])]
    print 'The JSP_shell payload  decode is :'
    f1 = open('behinder_out.class','wb')
    f1.write(a)
    f1.close()
    f2 = zipfile.ZipFile("./behinder_out.zip", 'w', zipfile.ZIP_DEFLATED)
    f2.write("behinder_out.class")
    f2.close()
    print "Result in behinder_out.class & behinder_out.zip where curret directory, You can user jd-gui.jar to unzip"
    print '*' * 73

def behinder_php_decode(string,key):
    data = base64.b64decode(string)
    data = aes_decode_CBC(data,key)
    a =  re.findall('64_decode\(\'(.*)\'\)\)',data)
    a = base64.b64decode(a[0])
    print 'The PHP_shell payload  decode is :'
    print a
    print '*' * 73


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-s', type=str, help="The target string or character")
arg_parser.add_argument('-f', type=str, help="The target filename")
args = arg_parser.parse_args()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print info
        sys.exit(0)
        # _EXIT_

    if sys.argv[1] == "-s":
        STRING = sys.argv[2]
    elif sys.argv[1] == "-f":
        with open(sys.argv[2],'rb+') as f:
            STRING = f.read()
            f.close()
    else:
        print information

    while True:
        information()
        try:
            choice = input("Please choose encode or decode type:\t")
            for case in switch(choice):
                if case(1):
                    format_output(STRING)
                    html_encode_format_output(STRING)
                    continue
                if case(2):
                    format_output(STRING)
                    html_decode_format_output(STRING)
                    continue
                if case(3):
                    format_output(STRING)
                    url_encode_format_output(STRING)
                    continue
                if case(4):
                    format_output(STRING)
                    url_decode_format_output(STRING)
                    continue
                if case(5):
                    format_output(STRING)
                    ascii_encode_format_output(STRING)
                    continue
                if case(6):
                    format_output(STRING)
                    ascii_decode_format_output(STRING)
                    continue
                if case(7):
                    format_output(STRING)
                    unicode_encode_format_output(STRING)
                    continue
                if case(8):
                    format_output(STRING)
                    unicode_decode_format_output(STRING)
                    continue
                if case(9):
                    format_output(STRING)
                    base64_encode_format_output(STRING)
                    continue
                if case(10):
                    format_output(STRING)
                    base64_decode_format_output(STRING)
                    continue
                if case(11):
                    format_output(STRING)
                    key = raw_input("Key = \t")
                    behinder_jsp_decode(STRING,key)
                    continue
                if case(12):
                    format_output(STRING)
                    key = raw_input("Key = \t")
                    behinder_php_decode(STRING,key)
                    continue
                if case():  # default, could also just omit condition or 'if True'
                    print "error!"
                    break
        except Exception as e:
            print "input error!\t"
            print e
            exit(0)
        STRING = raw_input("Please input a new string :\t")
