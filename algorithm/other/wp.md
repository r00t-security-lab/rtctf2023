签到：base64嵌套
略

r00t2023{crypto_is_so_easy!}

四四方方：四方密码（由于一点小big得用官网指定网站hiencode去解）

cipher jkbattbmbpklal

key1Miradonbcefghjklpstuvwxyz

key2 Regilkabcdfhjmnopstuvwxyz

（key分别是密勒顿和雷吉艾勒奇应该有人注意到吧~但是不关键）

r00t2023{lighttingspeed}

神奇凯撒：变异凯撒改了第一位的偏移量

ciphertext = 'o,+n+())pJ8@:OE715J@2+0c'

j = 3

for i in ciphertext:

    print(chr(ord(i) + j), end='')
    
    j += 1
    

r00t2023{VENI_VIDI_VICI}

voide：quipqiup秒掉，竟然有很多人卡住

大致解题思路就是原文是由作者故意写的没有e的一段话，简单分析知道密文和明文都没有e可以想到藏在密钥中

NFZYELOXJWVMIUBTSHKDCRQAGP

ABCDEFGHIJKLMNOPQRSTUVWXYZ

然后就能XOUTEBYRMISFLAG··· 只需要一点点观察力和一点点英文就能发现is 和 flag
于是...
r00t2023{XOUTEBYRM}

