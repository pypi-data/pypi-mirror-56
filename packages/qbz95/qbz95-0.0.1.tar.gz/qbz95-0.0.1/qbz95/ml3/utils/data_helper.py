import logging
import os
import six.moves.urllib as urllib


class MnistHelper:
    """提供MNIST手写数字数据集的下载，获取"""

    @classmethod
    def download(cls, target_path, source_url='http://yann.lecun.com/exdb/mnist', http_proxy=None):
        """下载MNIST数据文件"""
        if http_proxy is None:
            proxy_handler = urllib.request.ProxyHandler({'http': http_proxy, 'https': http_proxy})
            opener = urllib.request.build_opener(proxy_handler)
        else:
            opener = urllib.request.build_opener()

        urllib.request.install_opener(opener)

        def maybe_download(file_name):
            if not os.path.exists(target_path):
                os.mkdir(target_path)
            file_path = os.path.join(target_path, file_name)
            if not os.path.exists(file_path):
                source_file_url = os.path.join(source_url, file_name)
                logging.info(source_file_url)
                filepath, _ = urllib.request.urlretrieve(source_file_url, file_path)
                statinfo = os.stat(filepath)
                logging.info('Successfully downloaded {} {} bytes.'.format(file_name, statinfo.st_size))
            else:
                logging.info('Already downloaded {}'.format(file_name))
            return file_path

        train_data_path= maybe_download('train-images-idx3-ubyte.gz')
        train_label_path = maybe_download('train-labels-idx1-ubyte.gz')
        test_data_path= maybe_download('t10k-images-idx3-ubyte.gz')
        test_label_path = maybe_download('t10k-labels-idx1-ubyte.gz')
        return train_data_path, train_label_path, test_data_path, test_label_path