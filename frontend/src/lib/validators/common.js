import { isInt, isStr, isUndefined, toTitleCase2, filterUnique } from '@/lib/util';


export const createRulesFields = (fields, errors={}, types={}, TErrorCode={}, T_ERROR_STR={}, entity=null) => {
    let ret = {}
    fields.forEach(
        (field) => ret[`${field}_RULES`] = createRules(
            field,
            createRulesBase(
                field,
                errors,
                types,
                TErrorCode,
                T_ERROR_STR,
                entity,
            ),
            TErrorCode,
            T_ERROR_STR,
            entity,
        )
    );
    return ret;
};

const createRules = (field, rules={}, TErrorCode={}, T_ERROR_STR={}, entity=null, errors=null) => {
    TErrorCode = getTErrorCode(errors, entity, TErrorCode);
    T_ERROR_STR = getTErrorStr(errors, entity, T_ERROR_STR);
    if (Array.isArray(field)){
        return field.map((n) => createRules(field, rules, TErrorCode, T_ERROR_STR, entity, errors));
    }
    let ret = []
    if (rules.notNull) ret.push(v => !!v || T_ERROR_STR[TErrorCode[`${field}_EMPTY`]]);
    if (rules.maxLen) ret.push(v => v.length <= rules.maxLen || T_ERROR_STR[TErrorCode[`${field}_TOO_LONG`]]);
    if (isInt(rules.minLen)) ret.push(v => v.length >= rules.minLen || T_ERROR_STR[TErrorCode[`${field}_TOO_SHORT`]]);
    if (rules.enum) ret.push(v => (isInt(v) && (v in rules.enum))  || T_ERROR_STR[TErrorCode[`${field}_INVALID`]]);
    if (rules.isInt) ret.push(v => isInt(v)  || T_ERROR_STR[TErrorCode[`${field}_INVALID`]]);
    if (rules.max) ret.push(v => parseFloat(v) <= rules.max || T_ERROR_STR[TErrorCode[`${field}_INVALID`]]);
    if (isInt(rules.min)) ret.push(v => parseFloat(v) >= rules.min || T_ERROR_STR[TErrorCode[`${field}_INVALID`]]);
    if (rules.regex){
        if (isStr(rules.regex)){
            rules.regex = new RegExp(rules.regex);
        }
        ret.push(v => rules.regex.test(v) || T_ERROR_STR[TErrorCode[`${field}_INVALID`]]);
    }
    let keys = Object.keys(rules);
    if(ret.length != keys.length)
        throw new Error(`Rule count doesn't match. ${ret.length} != ${keys.length}`);
    // if (entity)
    //     ret = filterUnique(ret.concat(createRules(`${entity}_${field}`, rules, TErrorCode, T_ERROR_STR, null, errors)));
    console.log(`Created ${ret.length} rules for ${entity}.${field}: ${keys}`);
    return ret;
}
const createRulesBase = (field, errors={}, types={}, TErrorCode={}, T_ERROR_STR={}, entity=null) => {
    TErrorCode = getTErrorCode(errors, entity, TErrorCode);
    T_ERROR_STR = getTErrorStr(errors, entity, T_ERROR_STR);
    if (Array.isArray(field)){
        return field.map((n) => createRulesBase(field, errors, types, TErrorCode, T_ERROR_STR, entity));
    }
    let rules = {};
    let maxLen = `${field}_MAX_LEN`;
    if (errors.hasOwnProperty(maxLen)) rules.maxLen = errors[maxLen];
    let minLen = `${field}_MIN_LEN`;
    if (errors.hasOwnProperty(minLen)) rules.minLen = errors[minLen];
    let max = `${field}_MAX`;
    if (errors.hasOwnProperty(max)) rules.max = errors[max];
    let min = `${field}_MIN`;
    if (errors.hasOwnProperty(min)) rules.min = errors[min];
    let empty = `${field}_EMPTY`;
    if (TErrorCode.hasOwnProperty(empty)) rules.notNull = true;
    let _enum = `T_${field}_STR`;
    if (types.hasOwnProperty(_enum)) rules.enum = types[_enum];
    let regex = `${field}_REGEX_STR`;
    if (errors.hasOwnProperty(regex)) rules.regex = new RegExp(errors[regex]);
    let invalid = `${field}_INVALID`
    if (TErrorCode.hasOwnProperty(invalid)){
        invalid = T_ERROR_STR[TErrorCode[invalid]].toLowerCase()
        if (invalid.includes("bilangan bulat") || invalid.includes("integer")){
            rules.isInt = true;
        }
    }
    if (entity)
        rules = {...rules, ...createRulesBase(`${entity}_${field}`, errors, types, TErrorCode, T_ERROR_STR)};
    return rules;
}

const getTErrorCode = (errors=null, entity=null, TErrorCode=null) => {
    if (!TErrorCode && !isUndefined(errors) && !isUndefined(entity))
        TErrorCode = errors[`T${toTitleCase2(entity)}ErrorCode`];
    return TErrorCode;
}
const getTErrorStr = (errors=null, entity=null, T_ERROR_STR=null) => {
    if (!T_ERROR_STR && !isUndefined(errors) && !isUndefined(entity))
        T_ERROR_STR = errors[`T_${entity}_ERROR_STR`];
    return T_ERROR_STR;
}

export {createRules, createRulesBase}
export default createRules;
