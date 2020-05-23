import Lattice

lattice = Lattice.Lattice(227,[5.43],["Si"],[[0,0,0]],[1,0,0],"p-1X1-R0")
print(lattice.elements)
print(lattice.Amat)
print(lattice.Bmat)
print(lattice.base)
print(lattice.kvec)
print(lattice.rotAmat)
print(lattice.rotBmat)
print(lattice.rotbase)