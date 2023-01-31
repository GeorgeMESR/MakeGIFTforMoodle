import io
import numpy as np
from PIL import Image, ImageChops
import matplotlib.pyplot as plt
import base64


class answer:
	""" клас содержащий вопрос к тесту
		: txt: - строка с ответом
		: result: - правильный (1) или нет (0)
		: comment: - коментарий к ответу (если не нужен то пустая строка)
	"""

	def __init__(self, txt='', result='', comment=''):
		"""
		инициализация класса с заполнением переменных
		:param txt: текст ответа
		:param result: правильность: правильный (1) или нет (0)
		:param comment: комментарий
		"""
		self.txt = txt
		self.result = result
		self.comment = comment


	def ConvertFromGift(self, s):
		"""
		Функция преобразующая строку формата GIFT в класс с ответом
		:param s: строка в формате GIFT
		"""
		s = s.strip()
		self.res = 0
		self.txt = ''
		self.comment = ''
		if (s[0] == '='):
			self.result = 1
		s1 = s[1:len(s)].strip()
		i = s1.find('#')
		if (i != -1):
			self.txt = s1[0:i].strip()
			self.comment = s1[i + 1:len(s1)].strip()
		else:
			self.txt = s1.strip()
			self.comment = ''


class qst:
	""" клас содержащий вопрос к тесту
		: txt: - строка содержащая вопрос
		: answ: - список содержащий ответы в виде класса answer
		Таким образом в классе хранятся и вопрос и нужное количество ответов (правильных и нет)
	"""

	def __init__(self):
		self.txt = ''
		self.answ = []

	def AddAnsw(self, s:str):
		"""
		Функция добавляющая ответ из строки формата GIFT в список ответов
		:param s: строка в формате GIFT
		"""
		a = answer().ConvertFromGift(s)
		self.answ.append(a)

	def AddNew(self, txt, result, comment):
		"""
		Функция добавляющая ответ из строки формата GIFT в список ответов
		:param s: строка в формате GIFT
		"""
		self.answ.append(answer(txt, result, comment))

class catqst:
	"""
	класс хранящий категорию и список вопросов в этой категории
	: name: - строка с названием категории
	: qsts: - список хранящий вопросы с ответами в виде класса  qst
	"""

	def __init__(self):
		self.name = ''
		self.qsts = []

	def GetName(self, s: str):
		"""
		Функция которая добавляет имя категории, если встерчается ключевое слово '$CATEGORY:'
		:param s: строка в формате GIFT
		"""
		i = s.find('$CATEGORY:')
		if (i != -1):
			i += len('$CATEGORY:')
			self.name = s[i:len(s)]
			self.name = self.name.strip()


class tests:
	"""
	класс хранящий категории class catqst
	: title: Название дисциплины (используется для вывода ЦОР в формат треб. уч. отд.
	: test: список категорий из class catqst
	: defaultcat: Категория по умолчанию для упрощения добавления тестов
	"""

	def __init__(self):
		self.title = []
		self.tests = []
		self.defaultcat = None

	def AddCategor(self, name):
		"""
		Добавление категории с именем name в список (эта категория становится defaultcat
		:param name: имя категории
		:return: ничего
		"""
		a = catqst()
		a.name = name
		self.tests.append(a)
		self.defaultcat = self.tests[-1]


def LoadTest(input_file):
	"""
	Функция загрузки файла в формате GIFT
	:param input_file: имя файла
	:return: class tests, содержащий загруженные тесты
	"""
	catst = 0
	tst = tests()
	with open(input_file, 'r', encoding='utf-8') as f:
		ls = f.readlines()
		f.close()
		for i in range(len(ls)):
			if (ls[i].find('$CATEGORY') != -1):
				catst = i
				break
			if (len(ls[i]) > 3):
				tst.title.append(ls[i])
		while (True):
			cs = catqst()
			cs.GetName(ls[catst])
			catst += 1
			toname = 0
			q = qst()
			for i in range(catst, len(ls)):
				if (ls[i].find('$CATEGORY') != -1):
					catst = i
					tst.tests.append(cs)
					break
				if (toname == 0):
					if (len(ls[i]) > 2):
						if (q.txt != ''):
							q.txt += '<BR>'
						else:
							if (ls[i][0:1].isnumeric()):
								sts = ls[i].find(' ')
								ls[i] = ls[i][sts:len(ls[i])].strip()
						q.txt += ls[i].strip()
					if (ls[i].strip() == '{'):
						toname = 1
						continue
				if (toname == 1):
					if (len(ls[i]) > 2):
						q.AddAnsw(ls[i])
					if (ls[i].strip() == '}'):
						cs.qsts.append(q)
						q = qst()
						toname = 0
			if (catst != i):
				tst.tests.append(cs)
				break
	return tst


def SaveTest(output_file, tst: tests):
	"""
	Функция сохраняющая тесты в формат GIFT.
	:param output_file: имя файла куда будет произведено сохранение
	:param tst: тесты class tests
	:return: ничего
	"""
	with open(output_file, 'w', encoding='utf-8') as f:
		for cat in tst.tests:
			f.write('$CATEGORY: %s\n\n' % (cat.name))
			k = 1
			for t in cat.qsts:
				f.write('%s\n{\n' % (t.txt.replace('\n','<BR>').replace('=', '\\=')))
				for a in t.answ:
					if (a.result == 1):
						f.write('= ')
					else:
						f.write('~ ')
					f.write('%s' % (a.txt.replace('\n','<BR>').replace('=', '\\=')))
					if (a.comment != ''):
						f.write(' # %s' % (a.comment.replace('\n','<BR>').replace('=', '\\=')))
					f.write('\n')
				f.write('}\n\n')
				k += 1
		f.close()


def SaveTestInHtml(output_file, tst: tests):
	"""
	Функция сохраняющая тесты в формат HTML (если задать расширение html).
	Если задать расширение doc, то будет открыватся в редакторе MS Word и оттуда можно скопировать в ФОС
	требует два файла:
	"Header.txt" - начало html документа
	"FootNotes.txt" - окончание html документа
	:param output_file: имя файла куда будет произведено сохранение
	:param tst: тесты class tests
	:return:
	"""
	header = ''
	FootNotes = ''
	with open('Header.txt', 'r', encoding='utf-8') as f:
		header = f.read()
		f.close()
	with open('FootNotes.txt', 'r', encoding='utf-8') as f:
		FootNotes = f.read()
		f.close()

	with open(output_file, 'w', encoding='utf-8') as f:
		f.write(header)
		for cat in tst.tests:
			f.write('%s<BR><BR>\n' % (cat.name))
			k = 1
			for t in cat.qsts:
				f.write('Вопрос %d<BR>\n %s<BR>\n' % (
				k, t.txt.replace('<BR>', '\n').replace('\\=', '=').replace('[html]', '')))
				for a in t.answ:
					if (a.result == 1):
						f.write('правильный ответ:<BR>\n ')
					else:
						f.write('неправильный ответ:<BR>\n')
					f.write('%s' % (a.txt.replace('<BR>', '\n').replace('\\=', '=').replace('[html]', '')))
					if (a.comment != ''):
						f.write('<BR>Коментарий к ответу: %s' % (
							a.comment.replace('<BR>', '\n').replace('\\=', '=').replace('[html]', '')))
					f.write('<BR>\n')
				f.write('<BR>\n\n')
				k += 1
		f.write(FootNotes)
		f.close()


def swapPositions(list, pos1, pos2):
	"""
	Функция обмена двух позиций в списке
	:param list: список
	:param pos1: первая позиция
	:param pos2: вторая позиция
	:return: измененный список
	"""
	if (pos1 == pos2):
		return list
	if (pos1 < pos2):
		# popping both the elements from list
		first_ele = list.pop(pos1)
		second_ele = list.pop(pos2 - 1)
		# inserting in each others positions
		list.insert(pos1, second_ele)
		list.insert(pos2, first_ele)
	else:
		# popping both the elements from list
		first_ele = list.pop(pos2)
		second_ele = list.pop(pos1 - 1)
		# inserting in each others positions
		list.insert(pos2, second_ele)
		list.insert(pos1, first_ele)
	return list


def ConvertFigureInBase64(img):
	"""
	конвертация изображения Image в строку в формате base64
	:param img: изображения class Image
	:return: строка в формате base64
	"""
	b = io.BytesIO()
	img.save(b, format='png')
	binary_fc = b.getvalue()  # fc aka file_content
	base64_utf8_str = base64.b64encode(binary_fc).decode('utf-8')
	ext = 'png'
	dataurl = f'data:image/{ext};base64,{base64_utf8_str}'
	return dataurl


def plot_figure_preambule(xlabel_name,ylabel_name):
	"""
	Функция настраивающая вывод рисунка в ограниченный размер ( 2 x 1 дюйм).
	Размер необходимо ограничивать, так как в Moodle нет автомаштабирования картинок.
	После этой функции необходимо использовать сам вывод данных:
	plt.plot(x, y)
	Можно добавить текст :
	bbox = dict(boxstyle="round", fc="1.0")
	plt.text(0.1,0,1, txt, bbox=bbox,  fontsize=10)
	установить пределы:
	plt.xlim([minF,maxF])
	plt.ylim([minI,maxI])
	выключить стики по y:
	plt.yticks([])

	:param xlabel_name: Название оси абсцисс
	:param ylabel_name: Название оси ординат
	:return: структуру плота
	"""
	plt.rc('xtick', top=True, direction='in')
	plt.rc('ytick', right=True, direction='in')
	fig = plt.gcf()
	fig.set_size_inches(3, 3)
	margins = {  # +++
		"left": 0.040,
		"bottom": 0.180,
		"right": 0.960,
		"top": 0.900
	}
	fig.subplots_adjust(**margins)
	plt.minorticks_on()
	plt.xlabel(xlabel_name)
	plt.ylabel(ylabel_name)
	return fig


def plot_figure_convertimageToBase64():
	"""
	Функция сохраняющая рисунок matplotlib в строку Base64
	:return: строка в формате  Base64
	"""
	buf = io.BytesIO()
	# plt.show() # Можно раскоментировать и каждый рисунок будет показан на экране
	plt.savefig(buf, format='png')
	im = Image.open(buf)
	# im.save('img1.png') # Можно раскоментировать и рисунок будет сохранен в файл img1.png ( с затиранием старого)
	fig0 = ConvertFigureInBase64(im)
	plt.close()
	return fig0

white = (255, 255, 255, 255)
def latex2img(tex):
	"""
	конвертация формулы или текста latex в картинку через matplotlib
	работает неустойчиво, требует неявно устанавливаемых модулей
	:param tex: текст в формате latex
	:return: изображение Image
	"""
	buf = io.BytesIO()
	plt.rc('text', usetex=True)
	plt.rc('font', family='serif')
	plt.rcParams["text.latex.preamble"] =r"\usepackage{blkarray} \usepackage[utf8]{inputenc} \usepackage[T1]{fontenc}"
	# matplotlib.verbose.level = 'debug-annoying'
	fig = plt.figure()
	ax = fig.add_axes([0, 0, 1, 1])
	ax.set_axis_off()

	t = ax.text(0.5, 0.5, tex, horizontalalignment='center', verticalalignment='center', fontsize=15, color='black')
	ax.figure.canvas.draw()
	bbox = t.get_window_extent()
	# print(bbox.width, bbox.height)
	# Установка размеров области отрисовки
	fig.set_size_inches(bbox.width / 100, bbox.height / 100)
	plt.savefig(buf, format='png')
	plt.close()

	im = Image.open(buf)
	bg = Image.new(im.mode, im.size, white)
	diff = ImageChops.difference(im, bg)
	diff = ImageChops.add(diff, diff, 1.0, -5)
	bbox = diff.getbbox()
	return im.crop(bbox)

def latex2base64(tex_text):
	"""
	конвертация формулы или текста latex в строку Base64 через matplotlib
	работает неустойчиво, требует неявно устанавливаемых модулей
	:param tex_text:
	:return:
	"""
	s=tex_text.replace(r'\[',r'\[\rho(0)=')
	img=latex2img(s)
	# img.save('img1.png')
	return ConvertFigureInBase64(img)

SiPrefixRUSfull=['атто','фемто', 'пико', 'нано', 'микро', 'милли', '', 'кило', 'мега', 'гига', 'тера', 'пета', 'экса']
SiPrefixRUSshort=['а','ф', 'п', 'н', 'мк', 'м', '', 'к', 'М', 'Г', 'Т', 'П', 'Э']
def PhysicalFormatNumber(f:float):
	"""
	Преобразование числа в научный формат
	:param f:
	:return: кортеж из 4 полей
	поле 0 - округленное до 3-4 значаших цифр число
	поле 1-  Число для печати
	поле 2-  показатель степени 10  для числа в позиции 2
	поле 3- индекс для списка префиксов SiPrefixRUSfull или SiPrefixRUSshort
	"""
	pwr=int(np.log10(f))
	if(pwr>=0):
		pwr1=int(int(pwr/3)*3)
		div=np.power(10,pwr1)
		f1=f/div
		f2 = np.round(f1, 2)
		if(abs(pwr-pwr1)==1):
			f2=np.round(f1,1)
		if(abs(pwr-pwr1)==2):
			f2=np.round(f1,0)
		f3=f2*np.power(10,pwr1)
		return (f3, f2, pwr1, 6+int(pwr1/3))
	else:
		pwr=-pwr
		pwr1=int(int(pwr/3)*3)+3
		div=1/np.power(10,pwr1)
		f1=f/div
		f2 = np.round(f1, 2)
		if(abs(pwr-pwr1)==1):
			f2=np.round(f1,1)
		if(abs(pwr-pwr1)==2):
			f2=np.round(f1,0)
		f3=f2/np.power(10,pwr1)
		return (f3, f2, -pwr1, 6-int(pwr1/3))
