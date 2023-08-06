def cap(wstr):
	w=""
	for i in range (0, len(wstr)):
		if(wstr[i].isalpha() == False):
			i += 1
			continue
		else:
			w += wstr[:i] + wstr[i].capitalize() + wstr[i+1:]
			break
	return w

def capitalizer(x):
	n = len(x.split(" "))
	print('Your sentence contains', n, 'words')
	result = ""
	u = ""
	for word in x.split():
		if(len(word) == 1):
			result += word[0].capitalize() + " " 
		else:
			for n in range (len(word)-1 , 0,-1):
				if(word[n].isalpha() == True):
					result += word[0].capitalize() + word[1:n] + word[n:].capitalize()+ " "
					break
	for word in result.split():
		u += cap(word) + " "
	return (u)

def counter(string):
	Temp = string.casefold().split()
	print("Your sentence contains %d words"%len(Temp))
	for i in range (0,len(Temp)):
		if not (Temp[i].isalpha() == True):
		    x = ""
		    y = Temp[i]
		    for j in range(0,len(y)):
		       if (y[j].isalpha() == True):
		        x += y[j]
		    else:
		        j += 1
		    Temp.remove(Temp[i])
		    Temp.insert(i, x)
		else:
		    i += 1
	d = dict()
	for word in Temp:
		d[word] = d.get(word, 0) + 1
	return (d)
if (__name__ == '__main__'):
	sample = '!!w!e! have to #m$a$ke# it worth it!!!!'
	print(capitalizer(sample))
	print(counter(sample))
