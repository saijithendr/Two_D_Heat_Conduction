import numpy as np
import matplotlib.pyplot as plt
import copy
import tkinter as tk



root =tk.Tk()
root.title('Heat Distribution')

root.geometry("655x335")

#Displaying the text to enter the length
length = tk.Label(root, text="Length(m):-")
length.grid(row=0,column=1)

nodes = tk.Label(root, text = "Nodes(x,y axis):-")
nodes.grid(row=1,column=1)

left = tk.Label(root, text = "Left B.c:-")
left.grid(row=2,column=1)

right = tk.Label(root, text = "Right B.c:-")
right.grid(row=3,column=1)

top = tk.Label(root, text = "Top B.c:-")
top.grid(row=4,column=1)

bottom = tk.Label(root, text = "Bottom B.c:-")
bottom.grid(row=5,column=1)



###Values to take as a input
lengthval = tk.IntVar()
nodeval = tk.IntVar()
leftval = tk.IntVar()
rightval = tk.IntVar()
topval = tk.IntVar()
bottomval = tk.IntVar()



###Assigning it to a box
lengthentry = tk.Entry(root, textvariable =lengthval).grid(row=0,column=2)
nodeentry = tk.Entry(root, textvariable=nodeval).grid(row=1,column=2)
leftentry = tk.Entry(root,textvariable=leftval).grid(row =2,column=2)
rightentry = tk.Entry(root,textvariable=rightval).grid(row =3,column=2)
topentry = tk.Entry(root,textvariable=topval).grid(row =4,column=2)
bottomentry = tk.Entry(root,textvariable=bottomval).grid(row =5,column=2)



# Heat Transfer by using Two dimensional heat conduction equation


def mysolution():

    #No of nodes
    nx = nodeval.get()
    ny = nodeval.get()

    #Grid points
    l = lengthval.get()                    #int(input("Enter the length"))
    x = np.linspace(0,l,nx)
    y = np.linspace(0,l,ny)

    dx = x[2]-x[1]
    dy = y[2]-y[1]

    k = 2*(dx**2+dy**2)/(dx**2*dy**2)


    #Initial matrix of size (xxy)
    T = np.ones(shape=(nx,ny))*300   # STP condition


    #User defined boundary Temperatures
    T[0] = topval.get()             #Top boundary---- user defined 600
    T[-1] = bottomval.get()         # bottom boundary --- user defined 900

    for i in range(nx):
        T[i,0] = leftval.get()  # left boundary--- user defined 400
        T[i,-1] = rightval.get() # Right boundary-- user defined  800


        #Computing the corner temperatures
    T[0,0] = (T[0,1]+T[1,0])/2
    T[-1,-1] = (T[-1,-2]+T[-2,-1])/2
    T[0,-1] = (T[0,-2]+T[1,-1])/2
    T[-1,0] = (T[-2,0]+T[-1,1])/2

    #Discretizing the  equation
    tolerance = 1e-4
    error = 9e9
    Told = copy.deepcopy(T)

    iter =0

    while error>tolerance:
        for i in range(1,nx-1):
            for j in range(1,ny-1):
                T[i,j] = 1/k *( (T[i-1,j] + Told[i+1,j])/dx**2 + (T[i,j-1]+Told[i,j+1])/dy**2)

        error = np.amax(abs(Told-T))
        Told = copy.deepcopy(T)

            #print(Told)
        iter = iter+1


    cax = plt.contourf(x,np.flip(y),T,cmap="jet")
    plt.colorbar(cax)
    plt.show()

tk.Button(root, text ="Solution", command=mysolution, padx=10, pady=8, fg="white", bg="#263D42").grid()

root.mainloop()