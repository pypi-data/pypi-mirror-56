"""rsa工具模块
"""
import base64
import rsa


RSA_KEY_LENGTH = 2048
MAX_ENCRYPT_BLOCK = RSA_KEY_LENGTH // 8 - 11
MAX_DECRYPT_BLOCK = RSA_KEY_LENGTH // 8

def get_keypair_from_pem(pub_pem_file, priv_pem_file):
    """
    通过加载pem文件获取对一个的PKCS1类型的公私钥

    Parameters:
        pub_pem_file - 公钥pem文件路径
        priv_pem_file - 私钥pem文件路径

    Returns:
        返回公私钥组成的元组
    """
    with open(pub_pem_file, 'r') as pub_key_file:
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_file.read())
    with open(priv_pem_file, 'r') as priv_key_file:
        priv_key = rsa.PrivateKey.load_pkcs1(priv_key_file.read())
    return (pub_key, priv_key)

def get_pubkey_from_pem(pub_pem_file):
    """
    通过加载pem文件获取PKCS1类型的公钥

    Parameters:
        pub_pem_file - 公钥pem文件路径

    Returns:
        返回公钥，类型为rsa.PublicKey
    """
    with open(pub_pem_file, 'r') as pub_key_file:
        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_file.read())
    return pub_key

def get_privkey_from_pem(priv_pem_file):
    """
    通过加载pem文件获取PKCS1类型的私钥

    Parameters:
        priv_pem_file - 私钥pem文件路径

    Returns:
        返回私钥，类型为rsa.PrivateKey
    """
    with open(priv_pem_file, 'r') as priv_key_file:
        priv_key = rsa.PrivateKey.load_pkcs1(priv_key_file.read())
    return priv_key

def encrypt(data, pub_key, max_encrypt_block=MAX_ENCRYPT_BLOCK):
    """
    使用公钥对数据进行加密，可以对长数据进行分段加密

    Parameters:
        data - 要加密的数据
        pub_key - 加密数据要使用的公钥，类型为rsa.PublicKey
        max_encrypt_block - 加密数据时每段可加密的最大长度

    Returns:
        加密后的数据，是经过base64处理后的字符串
    """
    b64data = data.encode('utf8')
    res = []
    for i in range(0, len(b64data), max_encrypt_block):
        temp_data = b64data[i:i+max_encrypt_block]
        res.append(rsa.encrypt(temp_data, pub_key))
    return base64.b64encode(b"".join(res))

def decrypt(b64data, priv_key, max_decrypt_block=MAX_DECRYPT_BLOCK):
    """
    使用私钥对base64处理过后的加密数据进行解密

    Parameters:
        b64data - 经过base64编码后的加密之后的数据
        priv_key - 解密数据使用的私钥，类型为rsa.PrivateKey
        max_decrypt_block - 解密数据时每段可解密的最大长度

    Returns:
        解密后的原始数据
    """
    data = base64.b64decode(b64data)
    res = []
    for i in range(0, len(data), max_decrypt_block):
        temp_data = data[i:i+max_decrypt_block]
        res.append(rsa.decrypt(temp_data, priv_key))
    res_bytes = b"".join(res)
    return res_bytes.decode('utf8')

def sign(data, priv_key, hash_method='SHA-1'):
    """
    使用私钥对数据进行签名，默认采用SHA-1算法

    Parameters:
        data - 要签名的数据
        priv_key - 签名使用的私钥，类型为rsa.PrivateKey
        hash_method - 签名使用的hash算法，默认使用SHA-1

    Returns:
        经base64编码后的签名的结果
    """
    sign_result = rsa.sign(data.encode('utf8'), priv_key, hash_method)
    return base64.b64encode(sign_result)

def verify(b64data, pub_key, expect_data):
    """
    使用公钥对签名数据进行验签

    Parameters:
        b64data - 经过base64编码处理的签名后的数据
        pub_key - 验签要使用的公钥，类型为rsa.PublicKey
        expect_data - 预期的签名前的数据

    Returns:
        签名使用的算法类型，如：SHA-1
    """
    data = base64.b64decode(b64data)
    return rsa.verify(expect_data.encode('utf8'), data, pub_key)
