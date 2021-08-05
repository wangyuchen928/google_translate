import urllib
import execjs
import requests
from fake_useragent import UserAgent



class Translator:

    def __init__(self, proxies=None):
        self.ua = UserAgent()
        self.ctx = execjs.compile("""
                function TL(a) {
                var k = "";
                var b = 406644;
                var b1 = 3293161072;

                var jd = ".";
                var $b = "+-a^+6";
                var Zb = "+-3^+b+-f";

                for (var e = [], f = 0, g = 0; g < a.length; g++) {
                    var m = a.charCodeAt(g);
                    128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
                    e[f++] = m >> 18 | 240,
                    e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
                    e[f++] = m >> 6 & 63 | 128),
                    e[f++] = m & 63 | 128)
                }
                a = b;
                for (f = 0; f < e.length; f++) a += e[f],
                a = RL(a, $b);
                a = RL(a, Zb);
                a ^= b1 || 0;
                0 > a && (a = (a & 2147483647) + 2147483648);
                a %= 1E6;
                return a.toString() + jd + (a ^ b)
            };

            function RL(a, b) {
                var t = "a";
                var Yb = "+";
                for (var c = 0; c < b.length - 2; c += 3) {
                    var d = b.charAt(c + 2),
                    d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
                    d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
                    a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
                }
                return a
            }
            """)
        # {'http': "http://" + ip, "https": "http://" + ip}
        self.proxies = proxies

    def _get_tk(self, text):
        return self.ctx.call("TL", text)

    def __tran(self, content, tk, lang_in="auto", lang_to="auto"):
        if len(content) > 4891:
            return
        content = urllib.parse.quote(content)
        url = "https://translate.google.cn/translate_a/single?client=webapp&" \
              "sl=%s&tl=%s&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&clearbtn=1&otf=1&" \
              "pc=1&ssel=3&tsel=3&kc=2&tk=%s&q=%s" % (lang_in, lang_to, tk, content)
        result = self.__open_url(url)
        end = result.find("\",")
        if end > 4:
            return result[4:end]

    def __open_url(self, url):
        headers = {'User-Agent': self.ua.random}

        if self.proxies:
            response = requests.get(url=url, headers=headers, proxies=self.proxies)
        else:
            response = requests.get(url=url, headers=headers)
        data = response.content.decode('utf-8')
        return data

    def translate(self, text, lang_in='auto', lang_to='auto'):
        tk = self._get_tk(text)
        value = self.__tran(text, tk, lang_in, lang_to)
        if value:
            return value
        return None


if __name__ == "__main__":
    # 翻译一个单词
    while True:
        ori_word = input('word---:')
        if not ori_word:
            break
        t = Translator()
        # new_word = t.translate(ori_word, lang_to='cy')
        new_word = t.translate(ori_word, lang_to='zh-CN')
        print(new_word)
