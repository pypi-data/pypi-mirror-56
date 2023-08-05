import autodiffcc as ad

x = ad.AD(2, 1)

f = dir(ad)

print(f)

g = ad.cos(x)
print(g)