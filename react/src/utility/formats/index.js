export const Capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

export const Numero = (num) => {
    return num.toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
}
