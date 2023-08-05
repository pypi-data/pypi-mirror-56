# -*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-11 17:42:18
# @Last Modified by:   Anderson
# @Last Modified time: 2019-11-19 18:25:10
from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup
from copy import copy


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

	def clear(self):
		self.workbook.remove_sheet(self.sheet)
		self.sheet = self.workbook.create_sheet('sheet1')

	def save_excel_file(self, filename):
		if self.workbook:
			self.filename = filename
			self.workbook.save(filename=f'{filename}.xlsx')
		else:
			raise Exception("你还没有创建Excel文件")


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
		return [hot_count, title, f'https://s.weibo.com{url}']


excel_bot = ExcelBot()
web_crawler_bot = WebCrawlerBot()
