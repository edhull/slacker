import pytest
from handler import MessageHandler
from aiosmtpd.handlers import Message


def test_check_base64_decrypt():
    assert MessageHandler.decode_base64_if_required(Message,"dGVzdCBzdHJpbmc=") == "test string"
    
    
def test_check_strings_arent_read_as_base64():
    assert MessageHandler.decode_base64_if_required(Message,"test string") == "test string"    
    
    
def test_isbase64():
    assert MessageHandler.isBase64("test string") == False
    assert MessageHandler.isBase64("dGVzdA==") == True
    