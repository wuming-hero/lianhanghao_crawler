# -*- coding:utf-8 -*-
import HTMLParser
from cgi import escape
from json import loads, dumps
import string
import subprocess
import types
import urllib
import time
from hashlib import md5
import urlparse
import datetime
from bson import ObjectId
from pyramid.threadlocal import get_current_registry

from webhelpers.html import literal
from webhelpers.html.tags import *


def css_link(request, cssname):
    # "request.static_url('mypackage:static/foo.css') =>"
    return str(stylesheet_link(request.static_path('lllserver:static/css/' + cssname), rel='stylesheet/less'))


def js_link(request, jsname):
    # "request.static_url('mypackage:static/foo.css') =>"
    return str(javascript_link(request.static_path('lllserver:static/js/' + jsname)))


def less_stylesheet_link(*urls):
    return stylesheet_link(*urls, rel='stylesheet/less')


# 方法 返回 一个 不转 html   用 endswith 来判断
def isCurrent(request, path, more_css=None):
    rpath = request.path
    if isinstance(path, long):
        path = str(path) + '/'

    if path[-1] != '/':
        path = path + '/'

    if rpath[-1] != '/':
        rpath = rpath + '/'

    if rpath.endswith(str(path)):
        if more_css:
            return "class='current " + more_css + "'"
        else:
            return "class='current'"
    if more_css:
        return "class='" + more_css + "'"
    return ''


def day_formate(date):
    if date is None: return ""
    return date.strftime('%Y-%m-%d')


def daytime_formate(date):
    if date is None: return ""
    return date.strftime('%Y-%m-%d %H:%M:%S')


def datetime_formate(date):
    if date is None: return ""
    return date.strftime('%Y%m%d')


def pager(items):
    if items is None: return ''
    return items.pager(format='$link_first $link_previous ~2~ $link_next $link_last ', symbol_previous=u'<前页',
                       symbol_next=u'后页>', symbol_first=u'首页', symbol_last=u'尾页')


def is_alphabet(uchar):
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_safe_name(name):
    for n in name:
        if n.isalpha() or n.isdigit() or n in ('_', '-', '@'):
            continue
        else:
            return False

    return True


def to_safe_name(name):
    tmp = []
    for n in name:
        if n.isalpha() or n.isdigit() or n in ('_', '-', ' '):
            tmp.append(n)

    return string.join(tmp, "")


def exec_cmd(args):
    p = subprocess.Popen(args,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    code = p.wait()
    return code, p.stdout.read(), p.stderr.read()


def xssescape(text):
    """Gets rid of < and > and & and, for good measure, :"""
    return escape(text, quote=True).replace(':', '&#58;')


# 将半角字符转换成全角字符
def charB2Q(uchar):
    if uchar == '':
        return ''

    inside_code = ord(uchar)

    if not inside_code in range(32, 127):
        return uchar

    if inside_code == 32:
        inside_code = 12288
    else:
        inside_code += 65248

    if inside_code in range(32, 127):
        return uchar

    return unichr(inside_code).encode('utf-8', 'ignore')


# 将全角字符转换成半角字符
def charQ2B(uchar):
    if uchar == '':
        return ''

    inside_code = ord(uchar)

    if inside_code in range(32, 127):
        return uchar

    if inside_code == 12288:
        inside_code = 32
    else:
        inside_code -= 65248

    if not inside_code in range(32, 127):
        return uchar

    return unichr(inside_code).encode('utf-8', 'ignore')


# 将字符串中的半角转换成全角
def stringB2Q(ustring):
    try:
        ustring = ustring.decode('utf-8', 'ignore')
    except:
        pass

    result = ''
    for uchar in ustring:
        try:
            uchar = uchar.encode('utf-8', 'ignore')
        except:
            pass

        try:
            inside_code = ord(uchar)
        except:
            inside_code = ''

        if inside_code:
            if inside_code in range(32, 127):
                result += charB2Q(uchar)
            else:
                result += uchar
        else:
            result += uchar

    return result


# 将字符串中的全角转换成半角
def stringQ2B(ustring):
    try:
        ustring = ustring.decode('utf-8', 'ignore')
    except:
        pass

    result = ''
    for uchar in ustring:
        try:
            inside_code = ord(uchar)
        except:
            inside_code = ''

        if inside_code:
            if inside_code in range(32, 127):
                result += uchar
            else:
                result += charQ2B(uchar)
        else:
            result += uchar

    return result.encode('utf-8', 'ignore')


import random, re

alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
secret = alphabet  # Please set this in .development1.ini or .production.ini
numbers = '0123456789'


def encrypt(s):
    m = md5()
    m.update(s)
    return m.hexdigest()


def make_token(user):
    m = md5()
    timestamp = time.time()
    m.update(str(timestamp) + user)
    return m.hexdigest()


def make_random_string(length):
    'Return a random string of a specified length'
    return ''.join(random.choice(alphabet) for x in xrange(length))

def make_random_unique_string(length, is_unique):
    'Return a random string given a function that checks for uniqueness'
    # Initialize
    iterationCount = 0
    permutationCount = len(alphabet) ** length
    while iterationCount < permutationCount:
        # Make randomID
        randomID = make_random_string(length)
        iterationCount += 1
        # If our randomID is unique, return it
        if is_unique(randomID):
            return randomID
            # Raise exception if we have no more permutations left
    raise RuntimeError('Could not create a unique string')


def make_random_num(length):
    return ''.join(random.choice(numbers) for x in xrange(length))


def get_remote_ip(request):
    'Return IP address of client'
    return request.environ.get('HTTP_X_REAL_IP',
                               request.environ.get('HTTP_X_FORWARDED_FOR',
                                                   request.environ.get('REMOTE_ADDR')))


# 验证 图片类型
def validateImg(im):
    if im.format in ('JPEG', 'JPG', 'PNG', 'GIF', 'BMP'):
        return True
    return False


# 计算 文件 大小 为 XX 字节
def get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return size


""" form  https://github.com/joelsemar/django-webservice-tools/blob/b5ed057beb5a5202811c9adbc9f61ada9260a12e/webservice_tools/utils.py"""
EMAIL_REGEX = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"

MOBILE_REGEX = "^1[34578][0-9]{9}$"


def is_valid_email(email):
    return re.match(EMAIL_REGEX, email)


def is_valid_mobile(mobile):
    return re.match(MOBILE_REGEX, mobile)


def str_to_class(s):
    if s in globals() and isinstance(globals()[s], types.ClassType):
        return globals()[s]
    return None


def is_string_blank(s):
    return s is None or s.strip().isspace() or s.strip() == ''


class Tools(object):
    def __init__(self, request):
        self.request = request

    def s(self, filep):
        return literal(self.request.static_url('lllserver:static' + filep))

    def s0(self, filep):
        #settings = get_current_registry().settings
        #if settings['env'] == 'dev':
        #    return literal(self.request.static_url('lllserver:static' + filep))
        #return "http://asset_wmr.wdbvip.com/static%s" % filep
        return literal(self.request.static_url('lllserver:static' + filep))

    def p(self, filep):
        return literal(self.request.application_url + '/static_photos' + filep)

    def u(self, *elements, **kw):
        return literal(self.request.resource_url(self.request.context, *elements, **kw))

    def ur(self, *elements, **kw):
        return literal(self.request.resource_url(self.request.root, *elements, **kw))


    def html_unescape(self, text):
        return HTMLParser.HTMLParser().unescape(text)

    def html_truncate(self, text, length):
        if len(text) <= length:
            return text
        else:
            return text.substring(0, length) + "..."

    def exist(self, id, ids):
        for id1 in ids:
            if id1[0] == id:
                return True
        return False

    @classmethod
    def mFullSafeUrl(cls, url, request):
        settings = get_current_registry().settings
        mobileServiceUrl = settings['mobileServerUrl']
        safeUrl = url
        if url is None or url is '':
            safeUrl = "%s/m/" % mobileServiceUrl
            return safeUrl
        if url.startswith("http://"):
            safeUrl = url
        else:
            if url.startswith("/"):
                safeUrl = "%s%s" % (mobileServiceUrl, url)
            else:
                safeUrl = "http://%s" % url

        if url.startswith("tel:"):
            return url
        if url.startswith("mailto:"):
            return url
        if safeUrl.startswith(mobileServiceUrl):
            params = qs(safeUrl)
            ret = urlparse.urlparse(url)
            requestUrl = ret.scheme + "://" + ret.netloc + ret.path
            index = 0
            for key in params.iterkeys():
                if index == 0:
                    requestUrl += "?" + key + "=" + params[key]
                else:
                    requestUrl += "&" + key + "=" + params[key]
                index += 1
            return requestUrl
        return url

    @classmethod
    def tagsplits(cls, tags):
        if tags is None or tags == '':
            return []

        try:
            return loads(tags)
        except:
            return tags

    @classmethod
    def ssplit(cls, string, sp):
        if string is None or string == '':
            return []
        return string.split(sp)

    @classmethod
    def jsondumps(cls, str):
        return dumps(str)

    @classmethod
    def jsonloads(cls, str):
        if str is None or str == '':
            return []
        return loads(str)

    @classmethod
    def pinyinescape(cls, str):
        return str.replace(":", "___")

    @classmethod
    def date(cls, t):
        if t:
            return day_formate(t)

    @classmethod
    def datetime(cls, t):
        if t and type(t) == type(datetime.datetime.now()):
            return daytime_formate(t)
        else:
            return t

    @classmethod
    def datetime0(cls, t):
        if t:
            if isinstance(t, str):
                datetime0 = int(t)
                t0 = datetime.datetime.fromtimestamp(datetime0)
                return daytime_formate(t0)
            elif type(t) == type(datetime.datetime.now()):
                return daytime_formate(t)

    @classmethod
    def remainDaytime(cls, time):
        if time:
            if isinstance(time, str):
                return datetime.datetime.now() - datetime.datetime.now()
            elif type(time) == type(datetime.datetime.now()):
                return time - datetime.datetime.now()

    @classmethod
    def week(cls):
        import time

        week = int(time.strftime("%w"))
        return week

def tagsplits(tags):
    if tags is None:
        return []

    splitflag = [',', '，', '；', ' ', ';']
    arrays = re.split(r'(\,|\ |\;|\，|\；)', tags, re.U | re.S)
    ret = []
    for ars in arrays:
        if ars not in splitflag and not is_string_blank(ars):
            ret.append(ars)
    return ret


def timetoint(td):
    return (td.seconds + td.days * 24 * 3600) * 10 ** 6


def qs(url):
    query = urlparse.urlparse(url).query
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(query).items()])


#仅适用于ObjectId
def safeParam(params):
    if not params:
        return params
    #print "params=%s" % params
    pattern = re.compile(r'\\?(\w+)')
    match = pattern.match(params)
    if match:
        params = match.group(0)
    pattern1 = re.compile(r'\\&(\w+)')
    match1 = pattern1.match(params)
    if match1:
        params = match1.group(0)
    #print "params=%s" % params
    return params


def float2str(param):
    param = '%s' % float(param)
    if param[-1] == '0':
        param = param[:-2]
    return param


def list_reduce(list_1, list_2):
    result = []
    for i in list_1:
        for j in list_2:
            result.append([list_1[i], list_2[j]])
    return result


def dict_handler(t_dict):
    """将dict中的日期和ObjectId转为字符串,便于序列化"""
    if t_dict and isinstance(t_dict, dict):
        for k in t_dict.keys():
            v = t_dict[k]
            if isinstance(v, dict):
                # 深封装：找到所有的dict
                dict_handler(v)
            elif isinstance(v, ObjectId):
                t_dict[k] = str(v)
            elif isinstance(v, datetime.datetime):
                t_dict[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(v, list):
                for tmp in v:
                    if isinstance(tmp, dict):
                        dict_handler(tmp)
            else:
                pass
    return t_dict


def filterModule(serviceMenuMap, moduleList):
    if not moduleList or not 'moduleList' in moduleList:
        return serviceMenuMap
    newServiceMenuMap = {}
    for k, v in serviceMenuMap.iteritems():
        itemList = []
        for item in v:
            if moduleList['moduleList'].get(item['serviceCode'], True):
                itemList.append(item)
        newServiceMenuMap[k] = itemList
    return newServiceMenuMap


def is_chinese(unicodex):
    """判断一个unicode是否是汉字"""
    # if uchar >= u'u4e00' and uchar <= u'u9fa5':
    if 19968 <= unicodex <= 40895:
        return True
    else:
        return False


def sum_string_length(content):
    length = 0
    for item in content:
        if is_chinese(ord(item)):
            length += 2
        else:
            length += 1
    return length


def content_format(content, length=0):
    if length == 0:
        return content
    slen = sum_string_length(content)
    placeholder = ' '
    while slen < length:
        content += placeholder
        slen += 1
    return content


def content_format_for_device_print(content, length, head=''):
    """
    将字符串格式化成指定长度的多行显示
    :param content:
    :param length:
    :return:
    """
    if len(content) > length:
        head = '%s%s\n' % (head, content[:length])
        result = content_format_for_device_print(content[length:], length, head)
    else:
        tmp = content_format(content, length * 2)
        result = '%s%s' % (head, tmp)
    return result


# def dict_to_xml(dict_data):
#     if isinstance(dict_data, dict):
#         xml = '<xml>'
#         for k, v in dict_data.items():
#             if isinstance(v, (int, float)):
#                 xml = '%s<%s>%s</%s>' % (xml, k, v, k)
#             else:
#                 xml = '%s<%s><![CDATA[%s]]></%s>' % (xml, k, v, k)
#         xml = '%s%s' % (xml, '</xml>')
#         return smart_str(xml)
#     return None


def parse(html):
    number = 0
    nodeCollect = []
    newlat = ""

    def func(number, newlat, lat, collect):
        if number <= 160:
            if len(lat) == 0:
                return newlat, False
            elif lat.startswith("<div"):
                n = lat.find(">")
                newlat = newlat + lat[0:n + 1]
                collect.insert(0, "</div>")
                return func(number, newlat, lat[n + 1:], collect)
            elif lat.startswith("<span"):
                n = lat.find(">")
                newlat = newlat + lat[0:n + 1]
                collect.insert(0, "</span>")
                return func(number, newlat, lat[n + 1:], collect)
            elif lat.startswith("</div>"):
                newlat = newlat + "</div>"
                collect = collect[1:]
                return func(number, newlat, lat[6:], collect)
            elif lat.startswith("</span>"):
                newlat = newlat + "</span>"
                collect = collect[1:]
                return func(number, newlat, lat[7:], collect)
            elif lat.startswith("<br>"):
                newlat = newlat + "<br>"
                return func(number, newlat, lat[4:], collect)
            elif lat.startswith("&nbsp"):
                newlat = newlat + "<br>"
                number = number + 1
                return func(number, newlat, lat[5:], collect)
            elif lat.startswith("<img"):
                n = lat.find(">")
                newlat = newlat + lat[0:n + 1]
                return func(number, newlat, lat[n + 1:], collect)
            elif lat.startswith("<p"):
                n = lat.find(">")
                newlat = newlat + lat[0:n + 1]
                collect.insert(0, "</p>")
                return func(number, newlat, lat[n + 1:], collect)
            else:
                newlat = newlat + lat[0]
                number = number + 1
                return func(number, newlat, lat[1:], collect)
        else:
            for endNode in collect:
                newlat = newlat + endNode
            newlat = newlat + "..."
            return newlat, True

    return func(number, newlat, html, nodeCollect)




