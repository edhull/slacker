import pytest
try:
    # Python >= 3.3 
    from unittest import mock
except ImportError:
    # Python < 3.3
    import mock
from handler import MessageHandler
from aiosmtpd.handlers import Message
  
    
def test_not_decode_string():
    test1_res = MessageHandler.decode_base64_if_required("test string")
    assert test1_res == "test string"
    print("Test1: "+ str(test1_res))


def test_decode_base64():
    test2_res = MessageHandler.decode_base64_if_required("dGVzdCBzdHJpbmc=")
    assert test2_res == "test string"
    print("Test2: "+ str(test2_res))


