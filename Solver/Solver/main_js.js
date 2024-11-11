// eslint-disable-next-line no-undef
const chai = require("chai");
const assert = chai.assert;
chai.config.truncateThreshold = 0;

/// SOLUTION IS HERE FROM CODE WARS

function likes(ap) {
    if (ap instanceof Array) {
        if (ap.length === 0) {
            return "no one likes this";
        }
        if (ap.length === 1) {
            return `${ap[0]} likes this`;
        }
        if (ap.length === 2) {
            return `${ap[0]} and ${ap[1]} like this`;
        }
        if (ap.length === 3) {
            return `${ap.slice(0, 2).join(", ")} and ${ap[2]} like this`;
        }
        return `${ap.slice(0, 2).join(", ")} and ${ap.length - 2} others like this`;
    }
}

/// TESTS ARE HERE

assert.strictEqual(likes([]), "no one likes this");
assert.strictEqual(likes(["Peter"]), "Peter likes this");
assert.strictEqual(likes(["Jacob", "Alex"]), "Jacob and Alex like this");
assert.strictEqual(likes(["Max", "John", "Mark"]), "Max, John and Mark like this");
assert.strictEqual(likes(["Alex", "Jacob", "Mark", "Max"]), "Alex, Jacob and 2 others like this");
