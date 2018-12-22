'''
#ip 2
    seti 123 0 4        ; r4 = 123
@1:
    bani 4 456 4        ; r4 = r4 & 456
    eqri 4 72 4
    addr 4 2 2          ; branch to @5 if r4 == 72
    seti 0 0 2          ; branch to @1

@5:
    seti 0 1 4          ; r4 = 0
@6:
    bori 4 65536 1      ; r1 = r4 | 65536
    seti 16031208 7 4   ; r4 = 16031208
@8:
    bani 1 255 3        ; r3 = r1 & 255
    addr 4 3 4          ; r4 += r3
    bani 4 16777215 4   ; r4 &= 16777215
    muli 4 65899 4      ; r4 *= 65899
    bani 4 16777215 4   ; r4 &= 16777215
    gtir 256 1 3
    addr 3 2 2          ; branch to @16 if 256 > r1
    addi 2 1 2          ; branch to @17
@16:
    seti 27 3 2         ; branch to @28

@17:
    seti 0 9 3          ; r3 = 0
@18:
    addi 3 1 5          ; r5 = r3 + 1
    muli 5 256 5        ; r5 *= 256
    gtrr 5 1 5
    addr 5 2 2          ; branch to @23 if r5 > r1
    addi 2 1 2          ; branch to @24
@23:
    seti 25 7 2         ; branch to @26
@24:
    addi 3 1 3          ; r3 += 1
    seti 17 4 2         ; branch to @18
@26:
    setr 3 1 1          ; r1 = r3
    seti 7 5 2          ; branch to @8

@28:
    eqrr 4 0 3
    addr 3 2 2          ; halt if r4 == r0
    seti 5 1 2          ; branch to @6
'''

r4 = 0
seen = set()
prev = None

while True:
    r1 = r4 | 65536
    r4 = 16031208

    while True:
        r4 += r1 & 255
        r4 *= 65899
        r4 &= 16777215
        if r1 < 256:
            break
        r1 >>= 8

    if prev is None:
        print(r4)

    if r4 in seen:
        print(prev)
        break

    seen.add(r4)
    prev = r4
