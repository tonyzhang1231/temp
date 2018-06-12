import os,sys
from urllib.request import urlopen, urlretrieve
from datetime import datetime
from shutil import rmtree
import logging


def create_dir_if_not_exists(dir_name):
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)


def remove_dir_if_exists(dir_name, force = False):
	if os.path.exists(dir_name):
		if force:
			rmtree(dir_name)
		else:
			os.rmdir(dir_name)


def remove_file_if_exists(filepath):
	if os.path.exists(filepath):
		os.remove(filepath)


def create_file_if_not_exists(filepath):
	if not os.path.exists(filepath):
		filename = os.path.basename(filepath)
		with open(filepath, 'w') as f:
			pass

# convert datetime to date, both input and output are str
def datetime2date(dt, in_format='%Y/%m/%d %H:%M:%S', out_format='%Y%m%d'):
    date = datetime.strptime(dt , in_format).date()
    return datetime.strftime(date, out_format)

"""
example
datetime2date('2018/5/12 12:03:03')
"""



def maybe_download_file(file_url, filename, dest_directory, suffix = None):
    """
    Args:
    file_url: Web location of the file file.
    filename: the name of file saved to
    dest_directory: directory of all file file
    """
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    filepath = os.path.join(dest_directory, filename)
    if suffix:
    	filepath = filepath + '.' + suffix

    if not os.path.exists(filepath):
        def _progress(count, block_size, total_size):
            sys.stdout.write('\r>> Downloading %s %.1f%%' %
                           (filename,
                            float(count * block_size) / float(total_size) * 100.0))
            sys.stdout.flush()

        filepath, _ = urlretrieve(file_url, filepath, _progress)
        print()
        statinfo = os.stat(filepath)  # os.stat
        print ('Successfully downloaded {} {} bytes.'.format(os.path.basename(filepath), statinfo.st_size))
    else:
        print ('Not downloading files, file {} already present in disk'.format(filepath))


# os.walk() yields a 3-tuple   (dirpath, dirnames, filenames)
def iter_files(dir_name):
    for p, sub_d, fs in os.walk(dir_name):
        for f in fs:
            yield (os.path.join(p, f))

def get_size(filepath):
    return os.stat(filepath).st_size

def get_dir_size(dir_path, unit = 'B'):
    sz = 0
    for f in iter_files(dir_path):
        sz += get_size(f)

    print ("Size of {}: {} B, {:d} KB, {:.3f} MB, {:.3} GB".format(dir_path, sz, int(sz/1024), sz/1024**2, sz/1024**3))
    return sz

def count_files(dir_name):
    count = 0
    g = iter_files(dir_name)
    for x in g:
        count += 1
    return count




def scrape_industries(save2file='./all_hy_raw.txt'):
    with open(save2file, 'w') as fopen:
        try:
            url = '''http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI\
&sortType=(Name)&sortRule=1&page=1&pageSize=1000&js={"rank":[(x)]}\
&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.628606915911589&_=1525970262247'''

            try:
                f_url = urlopen(url)
                fp = f_url.read()
            except:
                print('Can not extract {}'.format(url))

            text = None
            try:
                text = fp.decode('utf-8')
            except UnicodeDecodeError as e:
                text = fp.decode('gb2312')
                print("Decode by GB2312: extract_hy_from_eastmoney({})".format(url))
            except UnicodeDecodeError as e:
                text = fp.decode('gbk')
                print("Decode by GBK: extract_hy_from_eastmoney({})".format(url))
            except:
                print("unknown Error: extract_hy_from_eastmoney({})".format(url))
                return

            if text is None:
                return

            hy = json.loads(text)['rank']

            #TODO: use sql later

            for h in hy:
                x = h + '\n'
                fopen.write(x)

            print ("Successfully write hy into disk")
        except:
            print ("Fail to write hy into disk")

def parse_industries(readfile = './all_hy_raw.txt', save2file='./all_hy.txt'):
    pass


def scrape_companies_by_industry(save2file='./companies_by_industry_raw.txt'):
    url = None
    pass

def parse_companies_by_industry(readfile = './companies_by_industry_raw.txt', save2file='./companies_by_industry.txt'):
    pass

def scrape_and_parse_all_companies(save2file='./all_companies.txt'):
    url = "http://quote.eastmoney.com/stock_list.html"
    pass




class Logger(object):
    def __init__(self, name='logger', level=logging.DEBUG, mode ='a', formatter='%(asctime)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        fh = logging.FileHandler('%s.log' % name, mode=mode)
        sh = logging.StreamHandler()

        sh.setFormatter(formatter)
        fh.setFormatter(formatter)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)



    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)




if __name__ == '__main__':
    log = Logger('test')
    log.info('abc')
    log.debug('debug')
