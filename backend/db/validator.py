import re
from utils.util import get_obj_attrs, to_title_case_2

def bind_rules(obj, rules):
    obj.rules = obj.RULES = rules
    for f, r in rules.items():
        setattr(obj, f"validate_{f[:-6].lower()}", lambda v: execute_rules(r, v))
    return obj

def execute_rules(rules, value):
    for rule in rules:
        y = rule(value)
        if isinstance(y, BaseException):
            raise y
    return True

def create_rules_fields(TError, fields, constants={}, types={}, TErrorCode={}, T_ERROR_STR={}, entity=None):
    ret = {}
    for field in fields:
        ret[f"{field}_RULES"] = create_rules_field(TError, field, constants, types, TErrorCode, T_ERROR_STR, entity)
    return ret

def create_rules_field(TError, field, constants={}, types={}, TErrorCode={}, T_ERROR_STR={}, entity=None):
    return create_rules(
        TError,
        field,
        create_rules_base(
            field,
            constants,
            types,
            TErrorCode,
            T_ERROR_STR,
            entity,
        ),
        TErrorCode,
        T_ERROR_STR,
        entity,
    )

def create_rules(TError, field, rules={}, TErrorCode={}, T_ERROR_STR={}, entity=None, constants=None):
    TErrorCode = get_TErrorCode(constants, entity, TErrorCode)
    T_ERROR_STR = get_T_ERROR_STR(constants, entity, T_ERROR_STR)
    ret = []
    if ("not_null" in rules):
        ret.append(lambda v: v is not None or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_EMPTY"]))
    if ("max_len" in rules):
        ret.append(lambda v: len(v) <= rules["max_len"] or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_TOO_LONG"]))
    if ("min_len" in rules and isinstance(rules["min_len"], int)):
        ret.append(lambda v: len(v) >= rules["min_len"] or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_TOO_SHORT"]))
    if ("enum" in rules):
        ret.append(lambda v: (isinstance(v, int) and (v in rules["enum"]))  or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_INVALID"]))
    if ("is_int" in rules):
        ret.append(lambda v: isinstance(v, int)  or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_INVALID"]))
    if ("max" in rules):
        ret.append(lambda v: float(v) <= rules["max"] or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_INVALID"]))
    if ("min" in rules and isinstance(rules["min"], int)):
        ret.append(lambda v: float(v) >= rules["min"] or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_INVALID"]))
    if ("regex" in rules):
        if (isinstance(rules["regex"], str)):
            rules["regex"] = re.compile(rules["regex"])
        ret.append(lambda v: rules["regex"].match(v) or TError(TErrorCode._NAMES_TO_VALUES[f"{field}_INVALID"]))
    keys = list(rules.keys())
    if(len(ret) != len(keys)):
        raise AssertionError(f"Rule count doesn't match. {len(ret)} != {len(keys)}")
    print(f"Created {len(ret)} rules for {entity}.{field}: {keys}")
    return ret

def create_rules_base(field, constants={}, types={}, TErrorCode={}, T_ERROR_STR={}, entity=None):
    TErrorCode = get_TErrorCode(constants, entity, TErrorCode)
    T_ERROR_STR = get_T_ERROR_STR(constants, entity, T_ERROR_STR)
    rules = {}
    max_len = f"{field}_MAX_LEN"
    if (hasattr(constants, max_len)):
        rules["max_len"] = getattr(constants, max_len)
    min_len = f"{field}_MIN_LEN"
    if (hasattr(constants, min_len)):
        rules["min_len"] = getattr(constants, min_len)
    max = f"{field}_MAX"
    if (hasattr(constants, max)):
        rules["max"] = getattr(constants, max)
    min = f"{field}_MIN"
    if (hasattr(constants, min)):
        rules["min"] = getattr(constants, min)
    empty = f"{field}_EMPTY"
    if (hasattr(TErrorCode, empty)):
        rules["not_null"] = True
    _enum = f"T_{field}_STR"
    if (hasattr(types, _enum)):
        rules["enum"] = types[_enum]
    regex = f"{field}_REGEX_STR"
    if (hasattr(constants, regex)):
         rules["regex"] = re.compile(getattr(constants, regex))
    invalid = f"{field}_INVALID"
    if (hasattr(TErrorCode, invalid)):
        invalid = T_ERROR_STR[TErrorCode._NAMES_TO_VALUES[invalid]].lower()
        if ("bilangan bulat" in invalid or "integer" in invalid):
            rules["is_int"] = True
    if (entity):
        rules = {**rules, **create_rules_base(f"{entity}_{field}", constants, types, TErrorCode, T_ERROR_STR)}
    return rules

def get_TErrorCode(constants=None, entity=None, TErrorCode=None):
    if not TErrorCode and constants and entity:
        TErrorCode = getattr(constants, f"T{to_title_case_2(entity)}ErrorCode")
    return TErrorCode

def get_T_ERROR_STR(constants=None, entity=None, T_ERROR_STR=None):
    if not T_ERROR_STR and constants and entity:
        T_ERROR_STR = getattr(constants, f"T_{entity}_ERROR_STR")
    return T_ERROR_STR
