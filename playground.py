import truthtables as tt
from math import sqrt, floor

As = tt.TT(''.join([str(int('a' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Bs = tt.TT(''.join([str(int('b' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Cs = tt.TT(''.join([str(int('c' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Ds = tt.TT(''.join([str(int('d' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Es = tt.TT(''.join([str(int('e' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Fs = tt.TT(''.join([str(int('f' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))
Gs = tt.TT(''.join([str(int('g' in tt.dig_to_segs[floor(sqrt(i) % 10)])) for i in range(100)]))

print(As.formula())
print(Bs.formula())
print(Cs.formula())
print(Ds.formula())
print(Es.formula())
print(Fs.formula())
print(Gs.formula())

