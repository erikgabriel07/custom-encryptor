import os
from argparse import ArgumentParser
from dotenv import load_dotenv


if not load_dotenv():
    print('File \'.env\' not found! Please create a file ' \
           'named \'.env\' and write SECRET_KEY="Your secret key"')
    raise SystemExit(1)
    
    
def transform(values: list, key):
    result = []
    
    for i in values:
        result.append(i.decode('utf-8'))
        
    result = ''.join(result)
    
    result = ''.join([key[i % len(key)] for i in range(len(result))])
    
    return result
    


class CustomCryptography:
    __SECRET_KEY_ = os.getenv('SECRET_KEY')
    
    
    @classmethod
    def encrypt(cls, plaintext: str, rot: int):
        key = transform(plaintext, cls.__SECRET_KEY_)
        
        cipher = []
        for text in plaintext:
            ciphered = ''
            text = text.decode('utf-8')
            for i in range(len(text)):
                new_value = ord(text[i]) + ord(key[i]) + rot
                if 31 < ord(text[i]) < 127:
                    new_value = 32 + (new_value - 32) % 95
                elif 127 < ord(text[i]) < 256:
                    new_value = 128 + (new_value - 128) % 224
                ciphered += str(chr(new_value))
            cipher.append(ciphered.encode() + b'\n')
        
        return cipher
    
    @classmethod
    def decrypt(cls, cipher: str, rot: int):
        key = transform(cipher, cls.__SECRET_KEY_)
        
        plaintext = []
        for symbol in cipher:
            decoded = ''
            symbol = symbol.decode('utf-8')
            for i in range(len(symbol) - 2):
                new_value = ord(symbol[i]) - ord(key[i]) - rot
                if 31 < ord(symbol[i]) < 127:
                    new_value = 32 + (new_value - 32) % 95
                elif 127 < ord(symbol[i]) < 256:
                    new_value = 128 + (new_value - 128) % 224
                decoded += str(chr(new_value))
            plaintext.append(decoded.encode() + b'\n')
            
        return plaintext
        

def main():
    parser = ArgumentParser(prog='encoder')
    parser.add_argument('file', help='file to encrypt')
    parser.add_argument('-e', '--encode', action='store_true')
    parser.add_argument('-d', '--decode', action='store_true')
    parser.add_argument('--rot', type=int, help='number of rotations')
    
    args = parser.parse_args()
    
    if not args.rot:
        args.rot = 0
    
    if args.encode == args.decode:
        print('You must choose one \'--encode\' or \'--decode\' method.')
        raise SystemExit(1)
    
    with open(args.file, mode='rb') as content:
        data = content.readlines()
    
    if args.encode:
        with open(args.file, mode='wb') as file:
            cipher = CustomCryptography().encrypt(data, args.rot)
            file.writelines(cipher)
            raise SystemExit(0)
    if args.decode:
        with open(args.file, mode='wb') as file:
            plaintext = CustomCryptography().decrypt(data, args.rot)
            file.writelines(plaintext)
            raise SystemExit(0)


if __name__ == '__main__':
    main()