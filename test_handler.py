import pytest
from handler import MessageHandler
from aiosmtpd.handlers import Message


def test_check_base64_decrypt():
    assert MessageHandler.decode_base64_if_required(Message,"dGVzdCBzdHJpbmc=") == "test string"
    
    
def test_check_strings_arent_read_as_base64():
    assert MessageHandler.decode_base64_if_required(Message,"test string") == "test string"    
    
    
def test_isbase64():
    b64 = "VHJpZ2dlcjogTmV4dENsb3VkIG5vdCByZXNwb25kaW5nDQpUcmlnZ2VyIHN0YXR1czogT0sNClRy \
    aWdnZXIgc2V2ZXJpdHk6IERpc2FzdGVyDQpUcmlnZ2VyIFVSTDogDQoNCkl0ZW0gdmFsdWVzOg0K \
    DQoxLiBOZXh0Q2xvdWQgUnVubmluZyAoTkFTLURBVDpuZXQudGNwLnNlcnZpY2VbdGNwLCw4MF0p \
    OiAxDQoyLiAqVU5LTk9XTiogKCpVTktOT1dOKjoqVU5LTk9XTiopOiAqVU5LTk9XTioNCjMuICpV \
    TktOT1dOKiAoKlVOS05PV04qOipVTktOT1dOKik6ICpVTktOT1dOKg0KDQpPcmlnaW5hbCBldmVu \
    dCBJRDogMzQxMzc="
    test1_res = MessageHandler.isBase64(Message, "test string")
    assert test1_res == False
    print("Test1: "+ str(test1_res))

    test2_res = MessageHandler.isBase64(Message, "dGVzdA==")
    assert test2_res != False
    print("Test2: "+ str(test2_res))

    test3_res = MessageHandler.isBase64(Message, b64)
    assert test3_res != False
    print("Test3: "+ str(test3_res))


test_isbase64()
