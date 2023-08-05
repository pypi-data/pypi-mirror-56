# coding: utf-8
import subprocess
import re
import json


class TargetError(Exception):
    pass


class WhoIs:
    FIELD_MAP = {
        "Registrar": "注册商",
        "Registrar Abuse Contact Email": "联系邮箱",
        "Registrar Abuse Contact Phone": "联系电话",
        "Creation Date": "创建时间",
        "Registry Expiry Date": "过期时间",
        "Registrar WHOIS Server": "域名服务器",
        "Name Server": "DNS"
    }

    def __init__(self, target):
        self.target = target

    @staticmethod
    def _match_field(field, text):
        """
        正则匹配获取对应字段的内容
        """
        reg = rf"{field}: (.+)"
        m = re.findall(reg, text)
        if m is not None:
            m = set(m)
        return m

    def _who_is(self):
        """
        调用系统上安装的whois, 返回查询的结果.
        """
        text = subprocess.getoutput(f"whois {self.target}")

        reg = rf'No match for domain "{self.target}".'
        if re.search(reg, text) is not None:
            raise TargetError("该域名未被注册或隐藏")
        return text

    def query(self):
        try:
            text = self._who_is()
        except TargetError as e:
            return json.dumps(e, ensure_ascii=False)

        res = []
        for key, value in self.FIELD_MAP.items():
            r = self._match_field(key, text)
            res.append({
                "name": value,
                "content": list(r)
            })
        res = json.dumps(res, ensure_ascii=False)
        return res
