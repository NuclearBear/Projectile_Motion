from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from math import *

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

def makeform(root, fields, inputs):
   entries = {}
   count = 0
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0, inputs[count])
      row.pack(side=BOTTOM, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries[field] = ent
      count += 1
   return entries


class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)               
		self.master = master
		self.run = 0
		self.init_window()

	def init_window(self):
		self.pack(fill=BOTH, expand=1)
		
		# Initializing the data table
		columns = ('Max Distance', 'Max Height', 'Time', 'Air Resistance?', 'Initial Height', 'Angle',
						'Velocity', 'Diameter', 'Mass', 'Drag Coefficient', 'Planet')
		table = Frame(self)
		table.pack(side=BOTTOM, fill=BOTH)
		
		self.scrollbar = Scrollbar(table)
		self.scrollbar.pack(side=RIGHT, fill=Y)
		
		DT = Treeview(table, yscrollcommand=self.scrollbar.set)
		DT['columns'] = columns
		DT.heading("#0", text='Run Number', anchor='w')
		DT.column("#0", anchor="w", width=100)
		for column in columns:
			DT.heading(column, text=column)
			DT.column(column, anchor='center', width=100)
		DT.pack(side=BOTTOM,anchor='s')
		
		self.scrollbar.config(command=DT.yview)

		# Setting up inputs in a dict and 
		fields = ('Drag Coefficient','Mass (kg)', 'Diameter (m)', 'Velocity (m/s)', 'Angle (degrees)', 'Initial Height (m)')
		inputs = ["0.3","2",".25","100","45","0"]
		self.ent = makeform(self, fields, inputs)

		# Label and drop down menu
		lab = Label(self,text='Planet Gravity')
		planets = StringVar()
		self.ent['Gravity'] = planets # adds selection varible to dict
		drop = OptionMenu(self,planets, 'Select','Earth','Moon','Sun','Mercury','Venus','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto')
		planets.set('Earth')

		# Air Risistance checkbox
		self.ent['Air'] = IntVar()
		C1 = Checkbutton(self, text='Air Resistance', variable=self.ent['Air'])
		   
		clearButton = Button(self, text="Graph on New",command=(lambda: self.graph_array(DT, 1)))
		clearButton.pack(side=TOP, anchor='n')

		graphButton = Button(self, text="Graph on Current",command=(lambda: self.graph_array(DT)))
		graphButton.pack(side=TOP, anchor='n')

		lab.pack(side=LEFT,anchor='s')
		drop.pack(side=LEFT,anchor='s')
		C1.pack(side=LEFT,anchor='s',padx=20)


	def graph_array(self, DT, clear=0):
		self.run += 1

		# Setting varible for calculations from inputs
		vi = self.nonint('Velocity (m/s)')
		ai = self.nonint('Angle (degrees)')
		hi = self.nonint('Initial Height (m)')
		mass = self.nonint('Mass (kg)')
		di = self.nonint('Diameter (m)')
		Cd = self.nonint('Drag Coefficient')

		# Selection of gravity based off planet
		gravity = {'Earth':9.81,'Moon':1.623,'Sun':274.88,'Mercury':3.728,'Venus':8.868,'Mars':3.689,'Jupiter':24.82,
					'Saturn':10.497,'Uranus':8.731,'Neptune':11.18,'Pluto':0.657}
		planet = self.ent['Gravity'].get()
		g = gravity[planet]

		if clear == 1:
			plt.clf()

		if self.ent['Air'].get() == 0:
			pAir = 0
			use = 'No'
		else:
			Air = {'Earth':1.225,'Moon':0,'Sun':0,'Mercury':0,'Venus':67,'Mars':0.02,'Jupiter':0.16,
					'Saturn':0.19,'Uranus':0.42,'Neptune':0.45,'Pluto':0}
			pAir = Air[self.ent['Gravity'].get()]
			use = 'Yes'   							# kg/m^3 Density of Air
													# for gas planets the density is taken from altitude of pressure of 1 bar
		
		A = pi*(di/2)**2 # cross section area of ball
		K = (1/2)*pAir*Cd*A/mass # Total resultant force of drag
		Th = ai * pi / 180

		# Calculations
		# Initial position, velocity, and acceleration
		v_x, v_y, a_x, a_y, x, y = [], [], [], [], [0], [hi]
		delta_t = 0.01
		t = 0

		while y[-1] >= 0:
			t += delta_t
			v_x = vi*cos(Th)*exp(-K*t)
			if pAir is not 0:
				v_y = ((K*vi*sin(Th)+g)*exp(-K*t)-g)/K
			else:
				v_y = vi*sin(Th)*exp(-K*t)
			x.append(abs(v_x * t))
			y.append((-.5*g*(t**2)) + (v_y*t) + hi)
		y[len(y)-1] = 0

		# Adding values to table
		DT.insert('', 'end', text=str(self.run), values=('%10.2f m' % max(x), '%10.2f m' % max(y), '%10.2f s' % t,
				use, '%d m' % hi, '%d˚' % ai, '%d m/s' % vi, '%d m' % di, '%d kg' % mass, Cd, planet))

		# Using matplotlib to plot data in new window
		plt.plot(x, y)
		plt.xlabel('Distance (m)')
		plt.ylabel('Height (m)')
		plt.axis('Normal')
		plt.title('Projectile Motion')
		plt.text(0, max(y), ' Run: %d' % self.run , verticalalignment='top', horizontalalignment='left')
		plt.show()


	def nonint(self, input):
		try:
			# Will try to return input as a type float if not it will throw exception instead of an error
			return float(self.ent[input].get())
		except:
			messagebox.showwarning("Non Int Value","Expected Input Type: Number")

root = Tk()
app = Window(root)
root.mainloop()