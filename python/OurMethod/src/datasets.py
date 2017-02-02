



f = open("synthetic.txt","w")
f2 = open("synthetic2.txt","w")

a=30
k=1
x = -k*a/2
for j in xrange(a):
    
     
    f.write("0: "+str(x)+" 1\n"   )
    f.write("1: "+str(x)+" 0\n"   )
    f.write("0: "+str(x)+" -1\n"   )
        
    f2.write("0: "+str(x)+" 1\n"   )
    f2.write("1: "+str(x)+" 0\n"   )
    f2.write("0: "+str(x)+" -1\n"   )
        
        
    x = x+2*k
    
f.close()
f2.close()    