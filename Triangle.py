import numpy as np
from Line import Line	

class Triangle(object):
	"""A triangle is definable by 3 lines which each of them has one end point in common"""
	def __init__(self, line1, line2, line3):
		self.line1 = line1
		self.line2 = line2
		self.line3 = line3
		self.triangles = []

	@staticmethod
	def edge_flip(edge, tri1, tri2, not_test):
		def det(a, b, c):
			return (a.x - c.x)*(b.y - a.y) - (a.x - b.x)*(c.y - a.y)
		def det_helper(line, point):
			return det(line.point1, line.point2, point)
		def fix_triangle(line, tri, new_tri):
			if line.triangle1 == tri:
				line.set_triangles(new_tri, 1)
			else:
				line.set_triangles(new_tri, 2)

		common_edges = []
		fliped_edge = None
		
		for i in range(1,4):
			for j in range(1,4):
				line1 = getattr(tri1, "line{}".format(i))
				line2 = getattr(tri2, "line{}".format(j))
				if line1.equal(edge) or line2.equal(edge) : continue
				if line1.point1.equal(line2.point2): 
					common_edges.append([line1, line2])
					fliped_edge = Line(line1.point2, line2.point1)
				elif line1.point1.equal(line2.point1):
					common_edges.append([line1, line2])
					fliped_edge = Line(line1.point2, line2.point2)
				elif line1.point2.equal(line2.point2):
					common_edges.append([line1, line2])
					fliped_edge = Line(line1.point1, line2.point1)
				elif line1.point2.equal(line2.point1):
					common_edges.append([line1, line2])
					fliped_edge = Line(line1.point1, line2.point2)

		is_quadrilateral = True
		if det_helper(fliped_edge, edge.point1) * det_helper(fliped_edge, edge.point2) >= 0 : is_quadrilateral = False

		triangle1 = Triangle(common_edges[0][0], common_edges[0][1], fliped_edge)
		triangle2 = Triangle(common_edges[1][0], common_edges[1][1], fliped_edge)

		if not_test:
			fix_triangle(common_edges[0][0], tri1, triangle1)
			fix_triangle(common_edges[0][1], tri2, triangle1)
			fix_triangle(common_edges[1][0], tri1, triangle2)
			fix_triangle(common_edges[1][1], tri2, triangle2)
		
		return triangle1, triangle2, fliped_edge, is_quadrilateral

	

	def draw(self, canvas, outline='#000000', fill='#FFFFFF', width=0.05):
		lines = self.sort_lines()
		points = []
		for line in lines :
			points += [line.point1.x, line.point1.y]
		
		points += [lines[0].point1.x, lines[0].point1.y]
		canvas.create_polygon(points, outline=outline,
    		fill=fill, width=width)

	def search(self, point): 
		if len(self.triangles) == 0 : return self
		for tri in self.triangles:
			if tri.is_point_inside(point):
				return tri.search(point)

	def find_last_layer_triangles(self, visited):
		if len(self.triangles) == 0 : return [self]
		lst = []
		for tri in self.triangles:
			if tri not in visited:
				visited[tri] = True
				lst += tri.find_last_layer_triangles(visited)

		return lst

	def is_point_inside(self, point):
		# determinant
		def det(a, b, c):
			return (a.x - c.x)*(b.y - a.y) - (a.x - b.x)*(c.y - a.y)
		def det_helper(line, point):
			return det(line.point1, line.point2, point)
		line1, line2, line3 = self.sort_lines()

		if det_helper(line1, point) <= 0 and det_helper(line2, point) <= 0 and det_helper(line3, point) <= 0 :
			return True
		if det_helper(line1, point) >= 0 and det_helper(line2, point) >= 0 and det_helper(line3, point) >= 0 :
			return True
		return False

	def sort_lines(self): # returns the lines in clockwise order
		line1 , line2, line3 = self.line1 , self.line2, self.line3
		if not line1.point2.equal(line2.point1) and not line1.point2.equal(line2.point2):
			line2, line3 = line3, line2
		if not line1.point2.equal(line2.point1):
			line2.point1, line2.point2 = line2.point2, line2.point1
		if not line1.point1.equal(line3.point2): 
			line3.point1, line3.point2 = line3.point2, line3.point1

		self.line1, self.line2, self.line3 = line1 , line2, line3
		return line1 , line2, line3

	def __str__(self):
		return  "Triangle : " + str(self.line1) + " " + str(self.line2) + " " + str(self.line3) + "\n"

	def __repr__(self):
		return  "Triangle : " + str(self.line1) + " " + str(self.line2) + " " + str(self.line3) + "\n"

	def angles(self): # return the 3 angles of this triangle
		def angle_helper(vec1, vec2): # returns
			cosine_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
			angle = np.arccos(cosine_angle)
			return np.abs(np.degrees(angle))
		l1,l2,l3 = self.sort_lines()
		# print ('pointsssssssssssss ', l1.point1, l2.point1, l3.point1)
		a = np.array([self.line1.point1.x,self.line1.point1.y])
		b = np.array([self.line2.point1.x,self.line2.point1.y])
		c = np.array([self.line3.point1.x,self.line3.point1.y])

		ba = a - b
		bc = c - b
		ca = a - c

		return [angle_helper(ba, bc), angle_helper(-ba, -ca), angle_helper(ca, -bc)]

	@staticmethod
	def validity_check(point, line): # legalizing
		def edge_without_point(tri, point):
			for i in range(1,4):
				line = getattr(tri, "line{}".format(i))
				if not line.point1.equal(point) and not line.point2.equal(point):
					return line

		if not line.is_legal():
			tri1, tri2, edge, is_quadrilateral = line.flip()
			
			edge.set_triangles(tri1, 1)
			edge.set_triangles(tri2, 2)
			
			line.triangle1.triangles.append(tri1)
			line.triangle1.triangles.append(tri2)

			line.triangle2.triangles.append(tri1)
			line.triangle2.triangles.append(tri2)

			next_candidate_edge1 = edge_without_point(tri1, point)
			next_candidate_edge2 = edge_without_point(tri2, point)

			Triangle.validity_check(point, next_candidate_edge1)
			Triangle.validity_check(point, next_candidate_edge2)

			edge.point1.neighbours.append(edge.point2)
			edge.point2.neighbours.append(edge.point1)

			line.point1.neighbours.remove(line.point2)
			line.point2.neighbours.remove(line.point1)
	