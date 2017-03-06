#coding utf-8

class Activity(object):

	def __init__(self,name,fromNode,toNode,dur):
		print('Activity '  + name + ' be created')
		self.name = name
		self.fromNode = fromNode
		self.toNode = toNode
		self.dur = int(dur)
		self.fromNode.addOut(self)
		self.toNode.addIn(self)
		self.ES = self.EF = self.LS = self.LF = 0
		self.TF = self.FF = self.INTF = self.INDF = 0
		self.onCP = False

	def printRelation(self):
		print('N'+str(self.fromNode.id) + ' ---'+self.name+'---> ' + 'N'+str(self.toNode.id))

	def getDur(self):
		return self.dur

	def cal_time(self):
		self.ES = int(self.fromNode.TE)
		self.LF = int(self.toNode.TL)
		self.EF = int(self.ES) + self.dur
		self.LS = int(self.LF) - self.dur
		cals = self.ES - self.LS
		calf = self.EF - self.LF
		if cals == 0 :
			if calf == 0:
				self.onCP = True

	def cal_FloatTime(self):
		self.TF = int(self.LF) - int(self.ES) - self.dur
		self.FF = int(self.toNode.TE) - int(self.fromNode.TE) - self.dur
		self.INTF = self.TF - self.FF
		self.INDF = self.toNode.TE - self.fromNode.TL - self.dur


class Node(object):

	def __init__(self,idn,TE = 0):
		print('Node '+str(idn)+' be created')
		self.id = idn
		self.TE = TE
		self.TL = 0
		self.inList = []
		self.outList = []

	def addIn(self,A):
		self.inList.append(A)

	def addOut(self,A):
		self.outList.append(A)

	def printInList(self):
		s = 'n'+str(self.id) + ' : '
		for a in self.inList:
			s = s + a.name + ' '
		print(s)

	def printoutList(self):
		s = 'n'+str(self.id) + ' : '
		for a in self.outList:
			s = s + a.name + ' '
		print(s)

	def cal_TE(self):
		maxTE = self.TE
		for a in self.inList:
			if maxTE < (a.dur + int(a.fromNode.TE)):
				maxTE = (a.dur + int(a.fromNode.TE))
		self.TE = maxTE
		self.TL = self.TE

	def cal_TL(self):
		if len(self.outList) > 0:
			minTL = 999
			for a in self.outList:
				if minTL > (int(a.toNode.TL) - int(a.dur)):
					minTL = (int(a.toNode.TL) - int(a.dur))
			self.TL = minTL

	def setStartTE(self,ste):
		self.TE = ste

#尋訪 node 與 activity
class Travel(object):
	def __init__(self,nodes,activitys):
		self.nodes = nodes
		self.activitys = activitys

	def cal_TE(self):
		for n in self.nodes:
			n.cal_TE()

	def cal_TL(self):
		for n in reversed(self.nodes):
			n.cal_TL()
	def getCP(self):
		cp = ""
		for a in self.activitys:
			if a.onCP:
				cp = cp + a.name
		print("Critical Path is %s" % cp)

	def printTETL(self):
		for n in self.nodes:
			print('node ' + str(n.id))
			print('TE ' + str(n.TE))
			print('TL ' + str(n.TL) + '\n')

	def cal_ELTime(self):
		for a in self.activitys:
			a.cal_time()

	def print_activity_Time(self):
		for a in self.activitys:
			print(a.name)
			print('| '+str(a.ES)+'  '+str(a.EF) + ' | ' + str(a.TF) + '  ' + str(a.FF)+ ' | ' )
			print('| '+str(a.LS)+'  '+str(a.LF) + ' | ' + str(a.INTF) + '  ' + str(a.INDF)+ ' | '  +'\n')

	def cal_floatTime(self):
		for a in self.activitys:
			a.cal_FloatTime()


class FromFileAndCreate(object):
	def __init__(self):
		self.nodes = []
		self.activitys = []

	#從檔案讀取 node
	def ReadNodesFile(self,nodesFile):
		file = open(nodesFile,'r')
		while True:
			line = file.readline()
			if not line:
				break
			line = line.replace('\n','')
			line = line.split(',')
			startTE = 0
			if len(line) > 1:
				startTE = line[1]
			self.nodes.append(Node(int(line[0]),startTE))
		file.close()

	#從 檔案裡讀取 activity
	def ReadActivitysFile(self,activitysFile):
		file = open(activitysFile,'r')
		while True:
			line = file.readline()
			if not line:
				break
			line = line.replace('\n','')
			line = line.split(',')
			self.activitys.append(self.ActivityFactor(line))
		file.close()

	#尋找 Activity 根據 id
	def getTargetNode(self,nid):
		for n in self.nodes:
			if n.id == int(nid):
				return n
		raise EOFError

	#產生一個 Activity
	def ActivityFactor(self,actList):
		try:
			nf = self.getTargetNode(actList[2])
			nt = self.getTargetNode(actList[3])
			a = Activity(actList[0],nf,nt,int(actList[1]))
			return a
		except EOFError:
			print('Error')

def test1():
	n1 = Node(1)
	n2 = Node(2)
	n3 = Node(3)
	n4 = Node(4)
	n5 = Node(5)
	n6 = Node(6)
	n7 = Node(7)

	A = Activity('A*',n1,n2,5)
	B = Activity('B',n2,n3,3)
	C = Activity('C',n2,n4,2)
	D = Activity('D',n2,n5,6)
	E = Activity('E',n3,n6,2)
	F = Activity('F',n4,n6,3)
	G = Activity('G',n5,n7,2)
	H = Activity('H-',n6,n7,4)
	DD = Activity('DD',n5,n6,0)

	Alist = [A,B,C,D,E,F,G,H,DD]
	nodes = [n1,n2,n3,n4,n5,n6,n7]
	T = Travel([n1,n2,n3,n4,n5,n6,n7],[A,B,C,D,E,F,G,H,DD])
	T.cal_TE()
	T.cal_TL()
	T.printTETL()

def test2():
	n2 = Node(2)
	n4 = Node(4)
	n6 = Node(6)
	n8 = Node(8)
	n10 = Node(10)
	n12 = Node(12)
	n14 = Node(14)
	n16 = Node(16)

	A = Activity('A',n2,n4,3)
	B = Activity('B',n4,n12,3)
	C = Activity('C',n4,n6,4)
	D = Activity('D',n4,n8,3)
	E = Activity('E',n6,n12,1)
	F = Activity('F',n8,n10,6)
	G = Activity('G',n12,n14,2)
	H = Activity('H',n10,n12,2)
	I = Activity('I',n10,n14,3)
	J = Activity('J',n14,n16,2)
	T = Travel([n2,n4,n6,n8,n10,n12,n14,n16],[A,B,C,D,E,F,G,H,I,J])
	T.cal_TE()
	T.cal_TL()
	T.printTETL()
	T.cal_ELTime()
	T.cal_floatTime()
	T.print_activity_Time()

def test3():
	n1 = Node(1)
	n2 = Node(2)
	n3 = Node(3)
	n4 = Node(4)
	n5 = Node(5)
	n6 = Node(6)
	n7 = Node(7)
	A = Activity('A',n1,n4,10)
	B = Activity('B',n4,n6,2)
	C = Activity('C',n6,n7,10)
	D = Activity('D',n1,n3,5)
	E = Activity('E',n3,n6,20)
	F = Activity('F',n3,n5,9)
	G = Activity('G',n1,n2,4)
	H = Activity('H',n2,n5,12)
	I = Activity('I',n5,n7,7)

	T = Travel([n1,n2,n3,n4,n5,n6,n7],[A,B,C,D,E,F,G,H,I])
	T.cal_TE()
	T.cal_TL()
	T.printTETL()
	T.cal_ELTime()
	T.cal_floatTime()
	T.print_activity_Time()

def test4():
	ff = FromFileAndCreate()
	ff.ReadNodesFile('aoa_nodes.n')
	ff.ReadActivitysFile('aoa_activitys.n')
	T = Travel(ff.nodes,ff.activitys)
	T.cal_TE()
	T.cal_TL()
	T.printTETL()
	T.cal_ELTime()
	T.cal_floatTime()
	T.print_activity_Time()
	T.getCP()
if __name__ == "__main__":
	test4()
