import bs4,scrapy
from ..items import Jobui1Item

class Jobuispider(scrapy.Spider):
    name = 'jobui_1'
    allowed_domains = ['jobui.com']
    start_urls = ['https://www.jobui.com/rank/company/']
    datas = []
    def parse(self, response):
        # parse是默认处理response的方法
        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        # 用BeautifulSoup解析response（企业排行榜的网页源代码）
        ul_list = bs.find_all('ul', class_="textList flsty cfix")
        # 用find_all提取<ul class_="textList flsty cfix">标签
        for ul in ul_list:
            # 遍历ul_list
            a_list = ul.find_all('a')
            # 用find_all提取出<ul class_="textList flsty cfix">元素里的所有<a>元素
            for a in a_list:
                # 再遍历a_list
                company_id = a['href']
                # 提取出所有<a>元素的href属性的值，也就是公司id标识
                url = 'https://www.jobui.com{id}jobs'
                real_url = url.format(id=company_id)
                # 构造出公司招聘信息的网址链接
                yield scrapy.Request(real_url, callback=self.parse_job)
                # 用yield语句把构造好的request对象传递给引擎。用scrapy.Request构造request对象。callback参数设置调用parsejob方法。


    def parse_job(self, response):
        # 定义新的处理response的方法parse_job（方法的名字可以自己起）

        #f = open(r'E:\getdata\Pythoncode\job.csv','a',encoding='utf-8')

        bs = bs4.BeautifulSoup(response.text, 'html.parser')
        # 用BeautifulSoup解析response(公司招聘信息的网页源代码)
        company = bs.find(id="companyH1").text
        # 用fin方法提取出公司名称
        datas = bs.find_all('div', class_="c-job-list")
        # 用find_all提取<li class_="company-job-list">标签，里面含有招聘信息的数据
        for data in datas:
            # 遍历datas
            item = Jobui1Item()
            # 实例化JobuiItem这个类
            item['company'] = company
            # 把公司名称放回JobuiItem类的company属性里
            item['position'] = data.find('a',class_='job-name').find('h3').text
            # 提取出职位名称，并把这个数据放回JobuiItem类的position属性里
            item['address'] = data.find('span').text
            # 提取出工作地点，并把这个数据放回JobuiItem类的address属性里
            item['detail'] = data.find_all('span')[1].text
            # 提取出招聘要求，并把这个数据放回JobuiItem类的detail属性里
            #datas.append([item['company'],item['position'],item['address'],item['detail']])
            #f.wirte([item['company'],item['position'],item['address'],item['detail']])
            yield item
        #f.close()
            # 用yield语句把item传递给引擎
        #wb = openpyxl.Workbook()
        #sheet = wb.active
        #sheet.title = 'joblist'
        #sheet.append(['公司', '职位', '地址', '招聘信息'])
        #for data in datas:
        #    sheet.append(data)
        #wb.save('job.xlsx')
        #wb.close()