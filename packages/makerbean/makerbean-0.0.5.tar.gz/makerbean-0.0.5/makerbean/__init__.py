# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-11 17:42:18
# @Last Modified by:   Anderson
# @Last Modified time: 2019-11-20 17:52:09
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
import jieba
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import Bar
from pyecharts.charts import WordCloud
from copy import copy
from collections import Counter
from .stop_words import stop_words


class WebCrawlerBot(object):
	"""docstring for WebCrawlerBot"""

	def __init__(self):
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
		}
		self.weibo_hot_list = []

	def get_sum_box_office(self):
		req = requests.get("http://cbooo.cn/BoxOffice/GetHourBoxOffice")
		return req.json()["data1"][0]["sumBoxOffice"]

	def get_rank_movie_data(self, index):
		req = requests.get("http://cbooo.cn/BoxOffice/GetHourBoxOffice")
		if index < len(req.json()["data2"]):
			movie_data = req.json()["data2"][index]
			return [
				movie_data["MovieName"],
				movie_data["BoxOffice"],
				movie_data["sumBoxOffice"],
				movie_data["movieDay"],
				movie_data["larger_url"],
			]
		else:
			raise Exception("排名数字超出范围")

	def get_weibo_hot(self, index):
		if not self.weibo_hot_list:
			base_url = 'https://s.weibo.com/top/summary'
			req = requests.get(base_url, headers=self.headers)
			soup = BeautifulSoup(req.text, 'lxml')
			today_hot = soup.select('#pl_top_realtimehot tr')[1:]
			self.weibo_hot_list = copy(today_hot)
		item = self.weibo_hot_list[index]
		title = item.select('.td-02 a')[0].text.strip()
		hot_count = int(item.select('.td-02 span')[0].text.strip())
		url = item.select('.td-02 a')[0].get('href')
		if 'javascript' in url:
			url = item.select('.td-02 a')[0].get('href_to')
		url = f'https://s.weibo.com{url}'

		# Get detail info
		req = requests.get(url, headers=self.headers)
		soup = BeautifulSoup(req.text, "lxml")
		author = soup.select(".card-wrap .content .info .name")[0].text.strip()
		content = soup.select(".card-wrap .content .txt")[0].text.strip()
		return [hot_count, title, author, content, url]

	def download_image(self, url, filename):
		req = requests.get(url)
		with open(f'{filename}.jpg', 'wb') as f:
			f.write(req.content)


class ExcelBot(object):
	"""docstring for ExcelBot"""

	def __init__(self):
		self.workbook = Workbook()
		self.sheet = self.workbook.active

	def add_row(self, row):
		try:
			self.sheet.append(row)
		except Exception as e:
			print(e)

	def get_row(self, row):
		data = []
		if isinstance(row, int):
			for cell in self.sheet[row]:
				data.append(cell.value)

		return data

	def get_col(self, col):
		data = []
		if isinstance(col, str):
			for cell in self.sheet[col]:
				data.append(cell.value)
		elif isinstance(col, int):
			for row in self.sheet.iter_rows(min_col=col, max_col=col):
				data.append(row[0].value)

		return data

	def clear(self):
		self.workbook.remove_sheet(self.sheet)
		self.sheet = self.workbook.create_sheet('sheet1')

	def save_excel_file(self, filename):
		if self.workbook:
			self.filename = filename
			self.workbook.save(filename=f'{filename}.xlsx')
		else:
			raise Exception("你还没有创建Excel文件")


class DataAnalysisBot(object):
	"""docstring for DataAnalysisBot"""
	def __init__(self):
		self.data = []

	def set_data(self, data):
		self.data = copy(data)

	def get_word_frequency(self, data, count=20):
		word_frequency = []
		words = ''
		if isinstance(data, str):
			words = data
		elif isinstance(data, list):
			words = '\n'.join([str(item) for item in data])

		punct = set(u''' #:!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
		﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
		々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
		︽︿﹁﹃﹙﹛﹝（｛“‘-—_…@~/\\''')

		words_cut = list(filter(lambda x: x not in punct, jieba.lcut(words)))
		words_cut = list(filter(lambda x: x not in stop_words, words_cut))
		word_frequency = Counter(words_cut).most_common(count)

		return copy(word_frequency)

	def generate_word_cloud(self, data):
		wordcloud = WordCloud()
		wordcloud.add("", data, word_size_range=[20, 100])
		wordcloud.render('word_cloud.html')

	def generate_bar(self, x_axis, y_axis):
		bar = Bar(
			init_opts=opts.InitOpts(
				width="1280px",
				height="720px"))
		bar.add_xaxis(x_axis)
		bar.add_yaxis("", y_axis)
		bar.set_global_opts(
			xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=10)))
		bar.render('bar.html')


web_crawler_bot = WebCrawlerBot()
excel_bot = ExcelBot()
data_analysis_bot = DataAnalysisBot()
