import math
def base(number, base, baseLookup = "default"):
	negative = False
	if number < 0:
		number = abs(number)
		negative = True
	if base < 2:
		raise Exception("Base number must be larger than 1. Base value given was " + str(base) + ".")
	if baseLookup == "default":
		baseLookup = {
			0: "0",
			1: "1",
			2: "2",
			3: "3",
			4: "4",
			5: "5",
			6: "6",
			7: "7",
			8: "8",
			9: "9",
			10: "A",
			11: "B",
			12: "C",
			13: "D",
			14: "E",
			15: "F"
		}
	array = []
	string = ""
	while math.ceil(number / base) != 0:
		array.append(number % base)
		number = math.floor(number / base)
	while len(array) != 0:
		i = array.pop()
		string += str(baseLookup.get(i))
	if negative:
		string = "-" + string
	return string