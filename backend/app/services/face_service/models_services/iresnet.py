from .net import IR_18, IR_34, IR_50, IR_101, IR_152, IR_SE_50, IR_SE_101, IR_SE_152

def iresnet18(num_features=512):
    return IR_18((112, 112))

def iresnet34(num_features=512):
    return IR_34((112, 112))

def iresnet50(num_features=512):
    return IR_50((112, 112))

def iresnet100(num_features=512):  # IR_101 tương ứng với iresnet100
    return IR_101((112, 112))

def iresnet152(num_features=512):
    return IR_152((112, 112))

def iresnet_se50(num_features=512):
    return IR_SE_50((112, 112))

def iresnet_se101(num_features=512):
    return IR_SE_101((112, 112))

def iresnet_se152(num_features=512):
    return IR_SE_152((112, 112))
