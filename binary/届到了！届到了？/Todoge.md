## 届到了！届到了？  
1,将得到的exe文件放入exeinfo,发现为64位可执行文件且没有加壳。  
2，放入IDA64中，反编译查看main函数。  
![1](./1.jpg)  
发现逻辑为将argv[0]的每一个字符的ASCII码求平方和作为种子，生成10个随机数，将每个随机数与enc异或后打印flag。  
即需要做的是找出正确的参数并传入。  
这里有两种做法，argv[0]实际上在命令行中运行时的第一个参数即文件名本身。  
根据题目中重复了很多很多遍的提示Todoge。可以猜想这个便是需要传入的参数。  
将文件改名为Todoge.exe然后在命令行中输入Todoge运行。  
![2](./2.jpg)  
