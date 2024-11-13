// eslint-disable-next-line no-undef
const chai = require("chai");
const assert = chai.assert;
chai.config.truncateThreshold = 0;

/// SOLUTION IS HERE FROM CODE WARS

let base = 10;
function multiplySmall(a, b) {
    if (b == 0) {
        return [0];
    }
    let divMod = 0;
    const res = [];

    for (let i = 0; i < a.length; ++i) {
        const mul = divMod + a[i] * b;
        const val = mul;
        res.push(val % base);
        divMod = Math.floor(val / base);
    }
    while (divMod > 0) {
        res.push(divMod % base);
        divMod = Math.floor(divMod / base);
    }
    if (res.length == 0) {
        return [0];
    }

    return res;
}
function substruct(a, b) {
    let mod = 0;
    let res = [];
    let i = 0;
    for (; i < a.length; ++i) {
        if (i < b.length) {
            res.push(a[i] - b[i] + mod);
        } else {
            res.push(a[i] + mod);
        }
        if (res[i] < 0) {
            res[i] += base;
            mod = -1;
        } else {
            mod = 0;
        }
    }
    return res;
}

function trim(a) {
    while (a.length > 0 && a[a.length - 1] == 0) {
        a.pop();
    }
    return a;
}
function isAppliedTry(a, b) {
    if (a.length == b.length) {
        for (let i = a.length - 1; i >= 0; --i) {
            if (a[i] < b[i]) {
                return false;
            } else if (a[i] > b[i]) {
                return true;
            }
        }
        return true;
    }
    return a.length > b.length;
}
function findMultiplier(a, b) {
    let res = 0;
    for (let d = 0; d < 2 * base; ++d) {
        const someTry = multiplySmall(b, d);
        if (isAppliedTry(a, someTry)) {
            res = d;
        }
    }
    return res;
}
function divideStrings(a, b) {
    if (a.length < b.length) {
        return ["0", a.toString()];
    }
    if (a.length === b.length && a < b) {
        return ["0", a.toString()];
    }
    const numA = a
        .toString()
        .split("")
        .map(val => val.charCodeAt(0) - "0".charCodeAt(0))
        .reverse();

    const numB = trim(
        b
            .toString()
            .split("")
            .map(val => val.charCodeAt(0) - "0".charCodeAt(0))
            .reverse()
    );

    let mod = [];
    let res = [];
    for (let i = numA.length - 1; i >= 0; --i) {
        mod = multiplySmall(mod, base);
        mod[0] += numA[i];
        mod = trim(mod);
        const d = findMultiplier(mod, numB);
        const val = trim(multiplySmall(numB, d));
        mod = substruct(mod, val);
        res.push(d);
    }
    res.reverse();
    res = trim(res);
    res.reverse();
    if (res.length === 0) {
        res.push(0);
    }
    mod = trim(mod);
    mod.reverse();
    if (mod.length === 0) {
        mod.push(0);
    }

    return [res.join(""), mod.join("")];
}

function largeDiv(a, b) {
    if (b === "0") {
        throw "error";
    }
    let sign = 1;
    a = a.toString();
    b = b.toString();
    if (a.startsWith("-")) {
        a = a.slice(1);
        sign *= -1;
    }
    if (b.startsWith("-")) {
        b = b.slice(1);
        sign *= -1;
    }

    function measureShift(val) {
        const dot = val.indexOf(".");
        return dot === -1 ? 0 : val.length - dot - 1;
    }
    function increaseVal(a, shift) {
        let current = measureShift(a);
        a = a.replace(".", "");

        while (current < shift) {
            a += "0";
            ++current;
        }
        return a;
    }

    const shiftA = measureShift(a);
    const shiftB = measureShift(b);

    const shift = Math.max(shiftA, shiftB);

    a = increaseVal(a, shift + 20);
    b = increaseVal(b, shift);

    let div = divideStrings(a, b)[0];
    const dot = -20;
    while (div.length <= -dot) {
        div = "0" + div;
    }
    div = div.slice(0, div.length + dot) + "." + div.slice(div.length + dot);
    if (sign == -1) {
        div = "-" + div;
    }
    while (div.length > 1 && div.endsWith("0")) {
        div = div.slice(0, div.length - 1);
    }
    if (div.endsWith(".")) {
        div = div.slice(0, div.length - 1);
    }

    return div;
}
/// TESTS ARE HERE
console.log(largeDiv("1000000000000", "1"), "25");
console.log(largeDiv("0.0025", "0.53"), "25");
console.log(largeDiv("13.251", "0.5"), "25");

//Arrange
console.log(
    largeDiv("0.0057971618635961420838224109420750736710", "0.8108614210328393444831922781048234"),
    "0.00714938670557537958"
);
console.log(largeDiv("13.25", "0.53"), "25");
console.log(largeDiv("13.25", "0.53"), "25");
