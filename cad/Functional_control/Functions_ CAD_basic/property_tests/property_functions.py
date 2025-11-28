def get_object_property(obj, property_name):
    """统一获取对象属性（自动识别CAD对象或天正对象）"""
    try:
        obj_name = com_retry(lambda: obj.ObjectName)
        # 天正对象：使用DISPID方式访问
        if obj_name in _TARCH_PROPERTY_MAP:
            dispid = _TARCH_PROPERTY_MAP[obj_name].get(property_name)
            if dispid:
                return obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYGET, True)
        # CAD标准对象：先Cast再访问属性
        obj = _maybe_cast(obj)
        return getattr(obj, property_name)
    except Exception as e:
        return None


def set_object_property(obj, property_name, value):
    """统一设置对象属性（自动识别CAD对象或天正对象）"""
    try:
        obj_name = com_retry(lambda: obj.ObjectName)
        # 天正对象：使用DISPID方式设置
        if obj_name in _TARCH_PROPERTY_MAP:
            dispid = _TARCH_PROPERTY_MAP[obj_name].get(property_name)
            if dispid:
                obj._oleobj_.Invoke(dispid, 0, pythoncom.DISPATCH_PROPERTYPUT, True, value)
                return True
        # CAD标准对象：先Cast再设置属性
        obj = _maybe_cast(obj)
        setattr(obj, property_name, value)
        return True
    except Exception as e:
        return False
