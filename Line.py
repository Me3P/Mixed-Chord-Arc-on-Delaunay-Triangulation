from Point import Point
import numpy as np

class Line(object):
	"""Line is made of two Points which are connected"""
	def __init__(self, point1, point2):
		self.point1 = point1
		self.point2 = point2
		self.triangle1 = None
		self.triangle2 = None

	def set_triangles(self, triangle, number): # in a triangulation each line belongs to two triangles, by using the method you can change the triangles
		if number == 1: self.triangle1 = triangle
		elif number == 2: self.triangle2 = triangle

	def draw(self, canvas, color='#eee', width = 3):
		canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=color, width=width)

	def is_legal(self):
		if self.triangle1 == None or self.triangle2 == None : return True # this line is on outer face which has to be legal
		
		tri1, tri2, new_edge, is_quadrilateral = Triangle.edge_flip(self, self.triangle1, self.triangle2, False)
		
		# print (tri1.angles(), tri2.angles())
		# print (self.triangle1.angles(), self.triangle2.angles())
		# self.triangle1.draw(self.canvas, fill= 'green')
		# self.triangle2.draw(self.canvas, fill = 'blue')
		# self.draw(self.canvas, 'yellow')
		# print (sum(self.triangle1.angles()), sum(self.triangle2.angles()))
		# input('next')
		m1 = min(tri1.angles() + tri2.angles())
		m2 = min(self.triangle1.angles() + self.triangle2.angles())
		
		if m1 >= m2 and is_quadrilateral : return False
		return True

	def __str__(self):
		return "Line : " + str(self.point1) +  str(self.point2) + '\n'

	def __repr__(self):
		return "Line : " + str(self.point1) +  str(self.point2) + '\n'

	def flip(self):
		return Triangle.edge_flip(self, self.triangle1, self.triangle2, True)

	def equal(self, other):
		if self.point1.equal(other.point1) and self.point2.equal(other.point2):
			return True
		if self.point2.equal(other.point1) and self.point1.equal(other.point2):
			return True
		return False

	def is_above(self, point):
		def det(a, b, c):
			return (a.x - c.x)*(b.y - a.y) - (a.x - b.x)*(c.y - a.y)
		if det(self.point1, self.point2, point) >= 0 : return True
		elif det(self.point1, self.point2, point) < 0: return False
		

	def does_intersect(self, other_line):
		def det(a, b, c):
			return (a.x - c.x)*(b.y - a.y) - (a.x - b.x)*(c.y - a.y)
		if det(self.point1, self.point2, other_line.point1) * det(self.point1, self.point2, other_line.point2) <= 0  and \
			det(other_line.point1, other_line.point2, self.point1) * det(other_line.point1, other_line.point2, self.point2) <= 0:
			return True
		return False 

	def intersection_point(self, s_line):
		def det_h(a, b, c):
			return (a.x - c.x)*(b.y - a.y) - (a.x - b.x)*(c.y - a.y)

		line1 = [[self.point1.x, self.point1.y], [self.point2.x, self.point2.y]]
		line2 = [[s_line.point1.x, s_line.point1.y], [s_line.point2.x, s_line.point2.y]]
		xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
		ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

		def det(a, b):
		    return a[0] * b[1] - a[1] * b[0]

		div = det(xdiff, ydiff)
		if div == 0:
			if det_h(self.point1, self.point2, s_line.point1) == 0: return s_line.point1
			else : return s_line.point2
			raise Exception('lines do not intersect, Points are not in general Position')

		d = (det(*line1), det(*line2))
		x = det(d, xdiff) / div
		y = det(d, ydiff) / div
		return Point(x, y)


from Triangle import Triangle
