min = 0.0
max = 1.0
p = 12
s = 0

step_plus = (max - min) / (p)
step_minus = (max - min) / (24 - p)

i = 0
while i <= 24:
	if i < p:
		print(round(min, 4))
		min += step_plus
	elif i > p:
		print(round(min, 4))
		min -= step_minus
	else:
		pass
	i += 1

input()