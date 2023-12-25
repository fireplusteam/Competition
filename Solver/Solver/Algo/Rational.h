//
//  Rational.h
//  Solver
//
//  Created by Ievgenii Mykhalevskyi on 24.12.2023.
//

#ifndef Rational_h
#define Rational_h

#include <iostream>
#include <stdexcept>
#include "BigInt.h"

class Rational {
private:
    bigint numerator;
    bigint denominator;

public:
    // Constructors
    Rational() : numerator(0), denominator(1) {}
    Rational(bigint num, bigint denom = 1) : numerator(num), denominator(denom) {
        if (denominator == 0) {
            throw std::invalid_argument("Denominator cannot be zero.");
        }
        simplify();
    }

    // Getter functions
    bigint getNumerator() const { return numerator; }
    bigint getDenominator() const { return denominator; }

    // Arithmetic operators
    Rational operator+(const Rational& other) const {
        return Rational(numerator * other.denominator + other.numerator * denominator,
                        denominator * other.denominator);
    }

    Rational operator-(const Rational& other) const {
        return Rational(numerator * other.denominator - other.numerator * denominator,
                        denominator * other.denominator);
    }

    Rational operator*(const Rational& other) const {
        return Rational(numerator * other.numerator, denominator * other.denominator);
    }

    Rational operator/(const Rational& other) const {
        if (other.numerator == 0) {
            throw std::domain_error("Cannot divide by zero.");
        }
        return Rational(numerator * other.denominator, denominator * other.numerator);
    }

    // Comparison operators
    bool operator==(const Rational& other) const {
        return numerator * other.denominator == other.numerator * denominator;
    }

    bool operator!=(const Rational& other) const {
        return !(*this == other);
    }
    
    bool operator<(const Rational& other) const {
        return numerator * other.denominator < other.numerator * denominator;
    }
    
    bool operator>(const Rational& other) const {
        return numerator * other.denominator > other.numerator * denominator;
    }

    // Output operator
    friend std::ostream& operator<<(std::ostream& os, const Rational& rational) {
        os << rational.numerator;
        if (rational.denominator != 1) {
            os << '/' << rational.denominator;
        }
        return os;
    }

private:
    // Helper function to simplify the fraction
    void simplify() {
        bigint num = numerator;
        if(num < 0) {
            num = -num;
        }
        bigint gcd = greatestCommonDivisor(num, denominator);
        numerator /= gcd;
        denominator /= gcd;

        // Adjust the sign to always be in the numerator
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
    }

    // Helper function to find the greatest common divisor
    bigint greatestCommonDivisor(bigint a, bigint b) const {
        while (b != 0) {
            bigint temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
};


#endif /* Rational_h */
