# encoding:utf-8
import re
import jieba
import jieba.analyse
import redis
import zhon.hanzi
from simhash import Simhash


class TextHashChecker(object):
    def __init__(self, threshold=3, bit_block_size=16, host='localhost', port=6379, db=2, password="123456"):
        self.threshold = threshold
        self.bit_block_size = bit_block_size
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.key_prefix = "text_simhash:"

    @staticmethod
    def calculate_hash(text: str) -> int:
        text = re.sub(r"[%s\n]+" % zhon.hanzi.punctuation, "", text)
        split_text = jieba.cut(text)
        return Simhash(split_text).value

    @staticmethod
    def hamming_distance(x: int, y: int):
        return len(list(filter(lambda _n: _n == "1", f"{x ^ y:064b}")))

    def save_split_hash(self, raw_hash: int):
        bit64 = f"{raw_hash:064b}"
        split_bit = [bit64[i:i + self.bit_block_size] for i in range(0, 64, self.bit_block_size)]
        for b in split_bit:
            self.redis.sadd(f"{self.key_prefix}{b}", raw_hash)

    def cal_rds_hash(self, raw_hash: int):
        bit64 = f"{raw_hash:064b}"
        split_bit = [bit64[i:i + self.bit_block_size] for i in range(0, 64, self.bit_block_size)]
        _hamming_distance = {self.threshold + 1}
        hash_all = set()
        for b in split_bit:
            rds_hash = self.redis.smembers(f"{self.key_prefix}{b}")
            if not rds_hash:
                continue
            for _hash in rds_hash:
                hash_all.add(_hash)
        for _hash in hash_all:
            _hamming_distance.add(self.hamming_distance(raw_hash, int(_hash)))
        return min(_hamming_distance)

    def is_text_duplicated(self, text: str, mode: int = 1):
        """

        :param text:
        :param mode: 0：全不入，1：全入，2：只入不重复的
        :return:
        """
        is_duplicated = False
        if self.cal_rds_hash(self.calculate_hash(text)) <= self.threshold:
            is_duplicated = True

        if mode == 0:
            return is_duplicated
        elif mode == 1:
            self.save_split_hash(self.calculate_hash(text))
            return is_duplicated
        elif mode == 2:
            if not is_duplicated:
                self.save_split_hash(self.calculate_hash(text))
            return is_duplicated


if __name__ == '__main__':
    thc = TextHashChecker(threshold=3, bit_block_size=16, host='47.93.234.57', port=6379, db=5, password="123456")
    t = '''
    央行11月18日发布的公告显示，当日开展1800亿元逆回购操作，期限为7天，中标利率为2.5%，较此前下调5个基点。业内人士认为，这是央行在本月初下调MLF操作利率以来，开展的又一项超出一些市场人士预期的货币政策操作。数据显示，此前1年期MLF利率下调是2016年6月以来首次，此次7天期央行逆回购利率下调则是2015年10月以来首次。
    '''
    print(thc.is_text_duplicated(t))
