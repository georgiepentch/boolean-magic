# libraries
from string import ascii_uppercase
import numpy as np
from tabulate import tabulate as tb
from inspect import signature
from itertools import chain, combinations


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


# DECIMAL DIGIT —> 7-SEGMENT DISPLAY
dig_to_segs = {
    0: ['a', 'b', 'c', 'd', 'e', 'f'],
    1: ['b', 'c'],
    2: ['a', 'b', 'g', 'e', 'd'],
    3: ['a', 'b', 'g', 'c', 'd'],
    4: ['f', 'g', 'b', 'c'],
    5: ['a', 'f', 'g', 'c', 'd'],
    6: ['a', 'f', 'g', 'c', 'd', 'e'],
    7: ['a', 'b', 'c'],
    8: ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    9: ['a', 'f', 'g', 'c', 'b']
}

# 7-SEGMENT DISPLAY —> DECIMAL DIGIT
segs_to_dig = {k: [] for k in dig_to_segs[8]}
for digs, segs in dig_to_segs.items():
    for seg in segs:
        segs_to_dig[seg] += [digs]


class TT:
    def __init__(self, out, padding='x', var_names=ascii_uppercase):
        """
        :param out: A string of '1' (True), '0' (False), and 'x' (Either) characters.
        :param padding: If len(out) != 2^n, which of '1', '0', or 'x' is used to pad the remaining output space.
        :param var_names: String/list of characters/names to be used as variable names in tables and formulas.
        """
        self.p = int(np.ceil(np.log2(len(out))))  # num of input cols
        self.entries = 1 << self.p  # num of rows
        self.out = out + (self.entries - len(out)) * padding
        self.var_names = var_names
        self.frmla = None

    def __str__(self):
        varr = []
        for i in range(self.entries):
            varr.append(list(format(i, "0" + str(self.p) + "b")))
        varr = np.append(varr, [[k] for k in self.out], axis=1)
        return tb(varr, list(self.var_names[:self.p]) + [self.frmla], tablefmt="fancy_outline")

    @classmethod
    def from_expression(cls, f):
        """:param f: A boolean-valued expression."""
        p = f.__code__.co_argcount
        out = ''
        for i in range(1 << p):
            out += str(int(f(*[int(q) for q in (format(i, "0" + str(p) + "b"))])))
        var_names = list(signature(f).parameters)
        return cls(out, var_names=var_names)

    def qmc(self):
        out1 = self.out.replace('x', '1')
        minterms = [format(i, "0" + str(self.p) + "b") for i, b in enumerate(out1) if b == '1']
        iteration = -1
        x = 0
        while len(minterms) > x:
            iteration += 1
            x = len(minterms)
            for i in range(x):
                if minterms[i].count('-') != iteration:
                    continue
                for j in range(i + 1, x):
                    t = int(minterms[i].replace('-', '0'), 2) ^ int(minterms[j].replace('-', '0'), 2)
                    if [a for a, b in enumerate(minterms[i]) if b == '-'] \
                            == [a for a, b in enumerate(minterms[j]) if b == '-'] and t.bit_count() == 1:
                        pos = format(t, "0" + str(self.p) + "b").index('1')
                        minterms.append(minterms[i][:pos] + '-' + minterms[i][pos+1:])
            minterms = f7(minterms)

        implicants = []
        for m in reversed(minterms):
            dashes = m.count('-')
            imp = []
            for i in range(1 << dashes):
                m1 = m
                for bit in format(i, '0' + str(dashes) + 'b'):
                    m1 = m1.replace('-', bit, 1)
                imp += [int(m1, 2)]
            implicants.append(imp)

        numbers = set([i for i, b in enumerate(out1) if b == '1'])
        prime_implicants = []
        while numbers:
            prime_implicants.append(implicants[0])
            numbers -= set(implicants[0])
            implicants = [s for s in implicants if numbers.intersection(set(s))]

        out0 = self.out.replace('x', '0')
        numbers = [i for i, b in enumerate(out0) if b == '1']
        flat_primes = [s for implicant in prime_implicants for s in implicant]
        essentials = set([e for e in numbers if flat_primes.count(e) == 1])
        final_implicants = [s for s in prime_implicants if set(s).intersection(essentials)]
        if len(prime_implicants) - len(final_implicants) > 2:
            remainder = [s for s in prime_implicants if s not in final_implicants]
            for i in powerset(remainder):
                if not set([a for b in i for a in b]) - set(numbers):
                    final_implicants += list(i)
                    break

        return final_implicants

    def formula(self, style=None):
        """:param style: Notation options. Default is sum of product. Alternatives are 'python', 'math', 'text'."""

        if style == "python":
            andsym, orsym, notsym = '&', '|', '~'
        elif style == "math":
            andsym, orsym, notsym = '∧', '∨', '¬'
        elif style == "text":
            andsym, orsym, notsym = ' and ', 'or', 'not '
        else:
            andsym, orsym, notsym = '', '+', '~'

        PI = self.qmc()
        expr = ''
        for prod in PI:
            b = 0
            for i in prod:
                b |= prod[0] ^ i
            for i in range(self.p):
                bit = 1 << self.p - i - 1
                if not (bit & b):
                    if bit & ~prod[0]:
                        expr += notsym
                    expr += self.var_names[i] + andsym
            if len(andsym) > 0:
                expr = expr[:-len(andsym)]
            expr += ' ' + orsym + ' '
        expr = expr[:-len(orsym)-2]
        self.frmla = expr
        return expr
