# define a function to switch integer to string
def get_string(number):
    res = []
    for i in range(6):
    	res.append(str(number % 10))
    	number /= 10
    res = "".join(res[::-1])
    return res

for i in range(1, 300500):
    number = get_string(i) 
    print number
