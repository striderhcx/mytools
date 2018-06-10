#coding: utf8  
import sys  
from Crypto.Cipher import AES  
from binascii import b2a_hex, a2b_hex
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

def gen_rsa_key():
    random_generator = Random.new().read  # 伪随机数生成器
    rsa = RSA.generate(1024, random_generator)  # rsa算法生成实例
    private_pem = rsa.exportKey()
    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'wb') as f:
        f.write(public_pem)
    
    with open('master-private.pem', 'wb') as f:
        f.write(private_pem)
    return private_pem, public_pem


def rsa_encrypt(key_file, message):
    with open(key_file, "r") as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # 导入读取到的公钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
        cipher_text = base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))  # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
        return cipher_text

def rsa_decrypt(key_file, cipher_text):
    with open(key_file, "r") as f:
        key = f.read()
        rsakey = RSA.importKey(key)  # 导入读取到的公钥
        cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
        text = cipher.decrypt(base64.b64decode(cipher_text), "ERROR")  # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
        return text.decode()
    

   
class AesCrypt():  
    def __init__(self, key):  
        self.key = key
        self.mode = AES.MODE_CBC  

    def encrypt(self, text):
        """
    	加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
	 
        这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
	""" 
        cryptor = AES.new(self.key, self.mode, self.key)
        text = text.encode("utf-8")
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (b'\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext).decode("ASCII")  #  因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题,所以这里统一把加密后的字符串转化为16进制字符串 
       
    def decrypt(self, text): 
        """
        解密后，去掉补足的空格用strip() 去掉
        """
        cryptor = AES.new(self.key, self.mode, self.key)  
        plain_text = cryptor.decrypt(a2b_hex(text))  
        return plain_text.rstrip(b'\0').decode("utf-8")

def test_aes():
    ac = AesCrypt('keyskeyskeyskeys')      #初始化密钥  
    e = ac.encrypt("my book is free")  
    d = ac.decrypt(e)                       
    print(e, len(e), d)  
    e = ac.encrypt("我是一个粉刷匠1231繁體testひらがな")  
    d = ac.decrypt(e)                    
    print (e, len(e), d) 
    
    e = ac.encrypt("甲铁城的卡巴内瑞") 
    d = ac.decrypt(e) 
    print(e, len(e),d)
    e = ac.encrypt("AES加密python3测试") 
    d = ac.decrypt(e) 
    print(e, len(e), d)

def test_rsa():
    print(gen_rsa_key())
    message = "hello 甲铁城的卡巴内瑞"
    en_msg = rsa_encrypt('master-public.pem', message)
    print("en_msg:{}".format(en_msg))
    de_msg = rsa_decrypt('master-private.pem', en_msg)
    print(de_msg)
    
   
if __name__ == '__main__':
    test_aes()
    test_rsa()  
     	 
