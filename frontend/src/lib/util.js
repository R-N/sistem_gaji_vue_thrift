export function treatAsUTC(date) {
    var result = new Date(date);
    result.setMinutes(result.getMinutes() - result.getTimezoneOffset());
    return result;
}

export const millisecondsPerDay = 24 * 60 * 60 * 1000;
export function daysBetween(startDate, endDate) {
    return (treatAsUTC(endDate) - treatAsUTC(startDate)) / millisecondsPerDay;
}

export function dateAsInt(date){
    return parseInt(date / millisecondsPerDay);
}

export async function checkBackend(url){
	var response = await fetch(url);
	var data = await response.json();
	return data;
}

export function backendUrl(https, host, port){
	var scheme = https ? "https" : "http";
	return scheme + "://" + host + ":" + port;
}

export function replaceArray(arr, anotherArr){
	return Array.prototype.splice.apply(arr, [0, arr.length].concat(anotherArr));
}
export function emptyArray(arr){
	return arr.splice(0, arr.length);
}
export function addEditFields(obj, fields){
	for(let i = 0; i < fields.length; ++i){
		obj[fields[i]+"Edit"] = obj[fields[i]];
	}
	return obj;
}
export function addEditFieldsBulk(arr, fields){
	for(let i = 0; i < arr.length; ++i){
		arr[i] = addEditFields(arr[i], fields);
	}
	return arr;
}
export function isInt(value) {
	return !isNaN(value) && (function(x) { return (x | 0) === x; })(parseFloat(value));
}
export function isInteger(value) {
	return isInt(value);
}
export function isStr(value){
	return (typeof value === 'string' || value instanceof String);
}
export function isString(value){
	return isStr(value);
}
export function isUndefined(value){
	return (typeof value === 'undefined' || value === null);
}
export function toTitleCase(str) {
	return str.replace(
		/\w\S*/g,
		text => text.charAt(0).toUpperCase() + text.substring(1).toLowerCase()
	);
}
export function toTitleCase2(str) {
	return toTitleCase(str.replace(/_/g, ' ')).replace(/\s+/g, '');
}
export function isUnique(value, index, array) {
	return array.indexOf(value) === index;
}
export function filterUnique(array) {
	return array.filter(isUnique);
}
