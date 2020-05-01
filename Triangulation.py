from Point import Point
from Line import Line
from Triangle import Triangle

class Triangulation(object):
	"""docstring for Triangulation"""
	def __init__(self):
		initial_distance = 10000
		m = 0
		p1 = Point(-initial_distance + m, -initial_distance + m)
		p2 = Point(initial_distance + m, -initial_distance + m)
		p3 = Point(0 + m, initial_distance + m)
		line1 = Line(p1, p2)
		line2 = Line(p2, p3)
		line3 = Line(p3, p1)
		
		self.triangle = Triangle(line1, line2, line3)

		line1.set_triangles(self.triangle, 1)
		line2.set_triangles(self.triangle, 1)
		line3.set_triangles(self.triangle, 1)

		self.points = [p1, p2, p3]
		self.out_points = [p1, p2, p3]
		self.triangles = [self.triangle]
		self.search_data_structure = self.triangle # DS()

	def draw(self, canvas):
		triangles = self.triangle.find_last_layer_triangles({})
		self.draw_triangles(list(set(triangles)), canvas)
		self.draw_points(canvas)
		

	def draw_triangles(self, triangles, canvas):
		for triangle in triangles:
			flag = False
			for i in range(1, 4):
				for j in range(1, 3):
					if getattr(getattr(triangle, "line{}".format(i)), "point{}".format(j)) in self.out_points:
						flag = True 	
						break
			if not flag:
				triangle.draw(canvas)

	def draw_points(self, canvas):
		for point in self.points:
			point.draw(canvas)

	def add_point(self, point, canvas):
		self.points.append(point)
		tri = self.triangle.search(point)
		self.add_edges(tri, point)
		
		Triangle.validity_check(point, tri.line1)
		Triangle.validity_check(point, tri.line2)
		Triangle.validity_check(point, tri.line3)

	def add_triangle(self, triangle):
		self.triangles.append(triangle)

	def remove_triangle(self, triangle):
		self.triangles.remove(self.triangles.find(triangle))

	def add_edges(self, triangle, point):
		def index_of_other_triangle_in_its_side_edges(line, triangle):
			if line.triangle1 == triangle : return 1
			return 2
		l1, l2, l3 = triangle.sort_lines()

		line1 = Line(l1.point1, point)
		line2 = Line(l2.point1, point)
		line3 = Line(l3.point1, point)

		tri1 = Triangle(triangle.line1, line1, line2)
		tri2 = Triangle(triangle.line2, line3, line2)
		tri3 = Triangle(triangle.line3, line1, line3)

		line1.set_triangles(tri1, 1)
		line1.set_triangles(tri3, 2)

		line2.set_triangles(tri1, 1)
		line2.set_triangles(tri2, 2)

		line3.set_triangles(tri3, 1)
		line3.set_triangles(tri2, 2)

		triangle.line1.set_triangles(tri1, index_of_other_triangle_in_its_side_edges(triangle.line1, triangle))
		triangle.line2.set_triangles(tri2, index_of_other_triangle_in_its_side_edges(triangle.line2, triangle))
		triangle.line3.set_triangles(tri3, index_of_other_triangle_in_its_side_edges(triangle.line3, triangle))

		triangle.triangles += [tri1, tri2, tri3]

		point.neighbours += [l1.point1, l2.point1, l3.point1]
		l1.point1.neighbours.append(point)
		l2.point1.neighbours.append(point)
		l3.point1.neighbours.append(point)


	def print_points(self):
		for item in self.points:
			print(item.x, item.y)
	