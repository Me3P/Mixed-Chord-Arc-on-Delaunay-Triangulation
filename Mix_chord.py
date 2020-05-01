from Point import Point
from Line import Line
import numpy as np
import math

class Mixed_Chord_Arc(object):
	"""d3ocstring for Mixed_Chord_Arc"""
	def __init__(self, strating_point, destination, canvas):
		self.strating_point = strating_point
		self.destination = destination
		self.current_point = strating_point
		self.canvas = canvas

	def next(self, a , b, A_c, B_c, p, st):
		
		def dist(p1, p2):
			a = np.array([p1.x,p1.y])
			b = np.array([p2.x,p2.y])
			return np.linalg.norm(a - b)

		if st.is_above(p) :
			return a if A_c <= dist(p, b) + B_c else b
		else :
			return b if B_c <= dist(p, a) + A_c else a

	def terminate(self):
		if self.current_point == self.destination: return True
		if self.destination in self.current_point.neighbours:
			return True
		return False

	def run(self, canvas, if_draw = False):
		max_limit = 1000
		line = Line(self.strating_point, self.destination)
		if if_draw: line.draw(self.canvas, color = 'yellow')
		prev_point = self.current_point
		if if_draw:self.strating_point.draw(canvas, 'green')
		if if_draw:self.destination.draw(canvas, 'red')
		p = self.strating_point
		t = self.destination
		st = Line(self.strating_point, self.destination)
		total_dist = 0
		i = 0
		while not self.terminate():
			i+= 1
			if i > max_limit:
				raise Exception('limit exceeed, Points are not in general position')
			next_line = self.next_line_intersects_st(p, st)

			if st.is_above(next_line.point1):
				a, b = next_line.point1, next_line.point2
			else :
				b, a = next_line.point1, next_line.point2

			# if if_draw:p.draw(canvas,color='blue')
			# if if_draw:a.draw(canvas,color='blue')
			# if if_draw:b.draw(canvas,color='blue')

			center_of_cycle = findCircle(p.x, p.y, a.x, a.y, b.x, b.y)

			r = center_of_cycle.dist(p)

			t1, t2 = intersectoin_oself_and_circle(center_of_cycle, r, st)

			t_C = t1 if t1.dist(self.destination) < t2.dist(self.destination) else t2
			# print (center_of_cycle, t_C ,' this ')
			# t_C.draw(canvas, 'yellow')

			A_c = self.arc_length(center_of_cycle, t_C, a, False, '#1E49F0')
			B_c = self.arc_length(center_of_cycle, b, t_C, False, '#D51E1B')
			prev_point = p
			p = self.next(a, b, A_c, B_c, p, st)
			self.current_point = p

			if if_draw:Line(prev_point, p).draw(canvas, color = 'black')
			total_dist += prev_point.dist(p)
			# input('next move')
		if if_draw:Line(self.current_point, self.destination).draw(self.canvas, 'black')
		total_dist += self.current_point.dist(self.destination)
		xx = self.strating_point.dist(self.destination)
		return total_dist / xx, xx

	def next_line_intersects_st(self, p, st):
		Min_L = None # line that contains the right most triangle and startign at s
		min_val = 9999999

		for a in p.neighbours:
			for b in a.neighbours:
				if b not in p.neighbours : continue
				L = Line(a, b)
				#L.draw(self.canvas)
				if st.does_intersect(L):
					inter_point = st.intersection_point(L)
					dist = inter_point.dist(self.destination)
					if dist < min_val:
						min_val = dist
						Min_L = L
		return Min_L

	
	def arc_length(self, center_point, point1, point2, draw=False, color = "#eee"):
		def angle(vec1, vec2): # returns
			cosine_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
			angle = np.arccos(cosine_angle)
			return np.degrees(angle)
		def point_to_vec(p1, p2):
			a = np.array([p1.x,p1.y])
			b = np.array([p2.x,p2.y])
			return b - a

		vec1 = point_to_vec(center_point, point1)
		vec2 = point_to_vec(center_point, point2)
		p_vec1 = np.array(-vec1[1], vec1[0])
		cnt = np.array([center_point.x, center_point.y])

		top_left = cnt - vec1 + p_vec1
		bottom_right = cnt + vec1 - p_vec1

		# if draw:
		# 	Point(top_left[0], top_left[1]).draw(canvas, 'black')
		# 	Point(bottom_right[0], bottom_right[1]).draw(canvas, 'yellow')
		# Line(center_point, Point(center_point.x +  vec1[0], center_point.y +  vec1[1])).draw(self.canvas, 'yellow')
		ang = angle(vec1, vec2)
	
		start_angle = angle(np.array([1,0]), vec1)
		r = np.linalg.norm(vec1)
		if draw :
			# xy = top_left[0], top_left[1], bottom_right[0], bottom_right[1]
			xy = cnt[0] - r, cnt[1] - r, cnt[0] + r, cnt[1] + r
			# self.canvas.create_rectangle(xy, fill='blue')
			self.canvas.create_arc(xy, start=start_angle, extent=start_angle + ang, fill=color, style=tk.ARC, width=3)	
		return 2*math.pi*r * np.abs(ang)/360 # portion of angle times 2*pi*r



# Function to find the circle on  
# which the given three points lie  
def findCircle(x1, y1, x2, y2, x3, y3) : 
	a = (x2 - x1, y2 - y1) # t*a + t0
	b = (x3 - x2, y3 - y2) # l*b + l0
	perpend_a = (-a[1], a[0])
	perpend_b = (-b[1], b[0])
	m1 = ((x1 + x2)/2, (y1+y2)/2) # middle point of first and second point
	m2 = ((x3 + x2)/2, (y3+y2)/2) # middle point of secpond and third point

	l1 = Line(Point(m1[0], m1[1]), Point(m1[0] + perpend_a[0], m1[1] + perpend_a[1]))
	l2 = Line(Point(m2[0], m2[1]), Point(m2[0] + perpend_b[0], m2[1] + perpend_b[1]))
	return l1.intersection_point(l2)

def intersectoin_oself_and_circle(center_of_cycle, radius, line):
	p1, p2 = line.point1, line.point2
	p1 = np.array([p1.x, p1.y])
	p2 = np.array([p2.x, p2.y])
	r = radius

	C = np.array([center_of_cycle.x, center_of_cycle.y])
	d = p2 - p1 #Direction vector of ray, from start to end 
	f = p1 - C #Vector from center sphere to ray start 

	a = d.dot(d)
	b = 2*f.dot(d)
	c = f.dot(f) - r*r

	discriminant = b*b-4*a*c

	if discriminant < 0 : 
		raise Exception('Line and circle does not intersect')

	t1 = (-b - math.sqrt(discriminant))/(2*a)
	t2 = (-b + math.sqrt(discriminant))/(2*a)

	inter_point1 = p1 + t1 * d
	inter_point2 = p1 + t2 * d

	return Point(inter_point1[0], inter_point1[1]), Point(inter_point2[0], inter_point2[1])