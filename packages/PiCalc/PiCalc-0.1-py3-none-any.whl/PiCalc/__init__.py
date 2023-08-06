from decimal import *

def pi(x):
	
	getcontext().prec=x+1	

	def sin(x):
	
		sin=Decimal(0)
		i=Decimal(1)
		pw=x
		fact=Decimal(1)
		sign=Decimal(1)
	
		while(i<3500):
			sin+=sign*pw/fact
			i+=Decimal(2)
			fact*=i*(i-1)
			pw*=Decimal(x**2)
			sign*=Decimal(-1)
		return sin	
	
	pi=Decimal(3)	
	i=1
	while(i<13):
		pi+=Decimal(sin(pi))
		i+=1
	return pi
