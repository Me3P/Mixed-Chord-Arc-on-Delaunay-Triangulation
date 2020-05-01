from Point import Point
from Triangulation import Triangulation
from Mix_chord import Mixed_Chord_Arc
import tkinter as tk
import random 
from tkinter import messagebox
import time

static_points = []
DT = Triangulation()
	
root = tk.Tk()
width = 800
height = 600
margin = 10
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0, highlightthickness=0)

alg = tk.StringVar()
alg.set('Greedy')
algorithms = ['Add Point', 'Set Start and End point']
canvas.grid(row=0, column=0, rowspan=len(algorithms)+3)

def print_value():
	print(alg.get())

for i, algorithm in enumerate(algorithms):
	tk.Radiobutton(root, text=algorithm, variable=alg , value=algorithm, command= print_value).grid(row=i, column=1)


root.title("Routing on Delaunay Triangulation")

def DT_draw(points):
	global DT, static_points
	canvas.delete("all")
	DT = Triangulation()
	for i in range(len(static_points)):
		p = Point(static_points[i].x, static_points[i].y)
		static_points[i] = p
		DT.add_point(p, canvas)
	DT.draw(canvas)

def leftHold(event):
	tt = time.time()
	new_point = Point(event.x, event.y)
	DT_draw(static_points + [new_point])
	

def leftRelease(event):
	new_point = Point(event.x, event.y)
	static_points.append(new_point)
	DT_draw(static_points)

st_point = None
end_point = None
def closesPoint(coordinate, color):
	temp = Point(coordinate.x , coordinate.y)
	mx = 9999999999
	res = None
	print (len(static_points), 'static_points')
	for p in static_points:
		if p.dist(temp) < mx:
			mx = p.dist(temp)
			res = p
	res.draw(canvas, color)
	return res

def leftClick(event):
	global st_point, end_point
	algo = alg.get()
	if algo == 'Add Point':
		static_points.append(Point(event.x, event.y))
		DT_draw(static_points)

	if algo == 'Set Start and End point':
		if  end_point != None:
			st_point = end_point = None
		if st_point == None:
			st_point = closesPoint(event, 'green')
		elif end_point == None:
			end_point = closesPoint(event, 'red')
			
			DT_draw(static_points)
			routing_alg = Mixed_Chord_Arc(st_point, end_point, canvas)
			res , _ = routing_alg.run(canvas, True)
			messagebox.showinfo("Routing Ratio", str(res))
		
	if algo == 'Mixed_Chord_Arc':
		mx = 0
		for st in static_points:
			for en in static_points:
				if st != en:
					routing_alg = Mixed_Chord_Arc(st_point, end_point, canvas)
					tot, _ = routing_alg.run(canvas)
					mx = max(tot, mx)
		print (mx)

def run():
	mx = 0
	i = 0
	rounds = len(static_points)**2
	for st in static_points:
		for en in static_points:
			if st != en:
				try:
					routing_alg = Mixed_Chord_Arc(st, en, canvas)
					tot, _ = routing_alg.run(canvas)
					mx = max(tot, mx)	
				except Exception as e:
					print (e)
					# routing_alg = Mixed_Chord_Arc(st, en, canvas)
					# tot, _ = routing_alg.run(canvas, True)
					# mx = max(tot, mx)
					# return
				
			i+=1
			if i % 100 == 0:
				print(i, '/' , rounds)
	print (mx)
	messagebox.showinfo("Routing Ratio", str(mx))


def DelaunayRatio(): # floyd warshall
	global static_points
	n = len(static_points)
	lst = [99999999] * n
	dist = [lst[:] for i in range(n)]

	for i in range(n):
		dist[i][i] = 0
	for i in range(n):
		p = static_points[i]
		for j in range(len(p.neighbours)):
			adj = p.neighbours[j]
			if adj in DT.out_points: continue
			dist[i][static_points.index(adj)] = p.dist(adj)

	for k in range(n):
		for i in range(n):
			for j in range(n):
				dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

	mx = 0
	for i in range(n):
		for j in range(i+1, n):
			mx = max(mx, dist[i][j] / static_points[i].dist(static_points[j]))
	print (mx)
	messagebox.showinfo("Routing Ratio", str(mx))
	return mx


def generate_points():
	global DT, static_points

	static_points.clear()
	print (len(static_points), ' len ')
	n = random.randint(100, 200)

	# static_points.append(Point(100,100))
	# DT.add_point(Point(100,100), canvas)
	# static_points.append(Point(100,200))
	# DT.add_point(Point(100,200), canvas)
	# static_points.append(Point(200,100))
	# DT.add_point(Point(200,100), canvas)
	# static_points.append(Point(250,200))
	# DT.add_point(Point(200,250), canvas)
	# static_points.append(Point(300,200))
	# DT.add_point(Point(300,200), canvas)
	while (n != 0):
		x = random.randint( margin, width - margin)
		y = random.randint( margin, height - margin)
		p = Point(x, y)
		flag = False
		for point in static_points:
			if point.equal(p):
				flag = True
		if flag:
			continue
		static_points.append(p)
		try:
			print (len(static_points))
			DT.add_point(p, canvas)
			# DT_draw(static_points)
		except Exception as e:
			static_points = static_points[:-1]
			print(e, 'e')
			print (len(static_points), ' len :/')
			DT_draw(static_points)
			continue

		n-=1

	print (len(static_points), ' this ')
	DT_draw(static_points)
	# for n in static_points:
	# 	n.draw(canvas, 'blue')

def rightClick(event):
	DT_draw(static_points)
	en = closesPoint(event, 'red')
	print(len(en.neighbours))
	for p in en.neighbours:
		p.draw(canvas, 'blue')

canvas.bind("<Button-1>", leftClick)
B = tk.Button(root, text ="Mixed_Chord_Arc Ratio", command = run)
B.grid(row = 3, column = 1)
B = tk.Button(root, text ="Delaunay Ratio", command = DelaunayRatio)
B.grid(row = 4, column = 1)
B = tk.Button(root, text ="Generate random points", command = generate_points)
B.grid(row = 5, column = 1)
canvas.bind("<Button-3>", rightClick)
# canvas.bind("<B1-Motion>", leftHold)
# canvas.bind("<ButtonRelease-1>", leftRelease)


root.mainloop()
