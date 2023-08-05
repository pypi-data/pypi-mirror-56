from math import pow as _pow


def rgb(l):
    startcol = [120, 0, 240]
    recpar = [2, 4]

    if l < 0 or (300 < l < 400) or l > 700:
        print("Error. Invalid Value")
        return None
    if 400 <= l <= 700:
        l -= 300

    to_firstmod = int(l / 60)
    lastmodArr = []
    if to_firstmod > 0:
        lastmodArr = [60] * (to_firstmod)
    lastmodArr.append(l % 60)

    for firstmod in range(to_firstmod + 1):
        startcol[firstmod % 3] += \
            int((_pow(-1, firstmod % 2 + 1)) * (recpar[firstmod > 0] * lastmodArr[firstmod]))

    return (startcol[0], startcol[1], startcol[2])


def extraColorSystem(num, colbit):
    colorpercentArr = []
    colorpercentArr.append(0)

    colors = []

    for i in range(1, num):
        colorpercentArr.append(i / (num - 1))

    for i in range(num):
        if not colbit:
            colors.append(int(colorpercentArr[i] * 255))
        else:
            colors.append(rgb(int(colorpercentArr[i] * 300)))

    return colors