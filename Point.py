import numpy as np

class Point(object):
	"""Each point has x and y coordinate"""
	def __init__(self, x, y):
		self.x = x # x coordinate of a point
		self.y = y # y coordinate of a point
		self.neighbours = []

	def add_neighbour(self, point):
		self.neighbours.append(point)

	def remove_neighbour(self, point):
		self.neighbours.remove(self.neighbours.find(point))
		
	def draw(self, canvas , color = 'white' , margin = 3): # draws a point on canvas
		x1, y1 = (self.x - margin), (self.y - margin)
		x2, y2 = (self.x + margin), (self.y + margin)
		canvas.create_oval(x1, y1, x2, y2, fill=color)

	def __str__(self):
		return "Point : " + str(self.x) + " " + str(self.y)

	def __repr__(self):
		return "Point : " + str(self.x) + " " + str(self.y)

	def equal(self, other):
		return self.x == other.x and self.y == other.y

	def draw_neighbours(self, canvas):
		for item in self.neighbours:
			item.draw(canvas, color='blue')

	def dist(self, p2):
		a = np.array([self.x,self.y])
		b = np.array([p2.x,p2.y])
		return np.linalg.norm(a - b)
