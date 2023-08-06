from bitfield import BitHandler

from isc_common import setAttr


def StrToNumber(s):
    if s == None:
        return None
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return None


def DelProps(value):
    if isinstance(value, dict):
        if value.get('props') and isinstance(value.get('props'), BitHandler):
            props = value.get('props')._value
            setAttr(value, 'props', props)
            return value
        else:
            return value
    else:
        value


def GetPropsInt(value):
    if isinstance(value, BitHandler):
        return value._value
    else:
        value
