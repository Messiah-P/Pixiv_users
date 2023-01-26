#import xlwt as xlwt
#from HTMLParser import HTMLParser
import requests

import Deduplicate
from DataOutPut import DataOutPut
from Search import User
#from Search import Tags
import MultiThreadDownload
import numpy as np
import xlrd

#file_path = './Painter' # Mac本地测试
file_path = '/mnt/photos/画师'
logo_pixiv = 'https://lsky.pantheon.center/image/2022/11/20/637a374fa4aca.jpeg'
head_bark = 'https://bark.pantheon.center/LdnaqCAHc49Huy2SWNnDz'
painter_info_path = "/mnt/python/Painter/Pixiv.xls"
wb = xlrd.open_workbook(painter_info_path) #Pixiv工作表文件
sh = wb.sheet_by_name('作者信息') #作者信息
#user_info = np.array([['米山舞', 1554775]])
user_info =np.empty(shape=(0,2)) #生成0行2列数组

def getPainter(user_info, deduplicate_list):
     # 通过输入构造目录
     bark_new = '--更新画作--'
     bark_null = '--未更新--'
     for i in range(len(user_info)): #遍历行
         # for user_id in range(len(user[0])): #遍历列
         user_name = user_info[i][0]
         user_id = user_info[i][1]
         print('\n')
         print('画师:' + user_name + ' - ' + user_id)
         d = DataOutPut()
         path = file_path
         d.mkdir(path)
         # 下载
         print('正在搜索ing...')
         user = User(user_id)  # 创建对象
         illust_ids = list(user.get_illust_ids(file_path, deduplicate_list))  # 获取列表
         if len(illust_ids) != 0:
             print('该画师共有' + str(len(illust_ids)) + '作品未下载, 即将开始下载画师' + str(user_id) + '的作品')
             print('正在下载ing...')
             bark_info = ('画师: ' + user_name + '\n' +'作品更新数: ' + str(len(illust_ids)))
             bark_new = bark_new + '\n' + bark_info
             MultiThreadDownload.multi_download(illust_ids, 0, path)
         else:
             print('该画师没有作品更新。')
             bark_null = bark_null + '\n' + user_name
     bark = bark_new + '\n' + bark_null
     ret = requests.get('%s/Pixiv画师更新/%s?icon=%s&group=画师' % (head_bark, bark, logo_pixiv))
     print('\n下载结束啦')

if __name__ == '__main__':
    # 获取作者信息
    for r in range(1, sh.nrows):
        ctype = sh.cell(r, 1).ctype  # 表格的数据类型
        cell = sh.cell_value(r, 1)
        if ctype == 2 and cell % 1 == 0.0:  # ctype为2且为浮点
            cell = int(cell)  # 浮点转成整型
        user_info_row = sh.row_values(r)
        user_info_row[1] = cell
        user_info = np.row_stack((user_info, user_info_row))
    print(user_info)
    Deduplicate_list = Deduplicate.all_pids(file_path)
    getPainter(user_info, Deduplicate_list)
