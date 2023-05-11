什么逝http

打开题目看到很明显的提示，must local user,所以搜索有关http请求头的信息，可以了解到X-Forward-For

xff 是http的拓展头部，作用是使Web服务器获取访问用户的IP真实地址（可伪造）。由于很多用户通过代理服务器进行访问，服务器只能获取代理服务器的IP地址，而xff的作用在于记录用户的真实IP，以及代理服务器的IP。

我们可以通过修改xff达到要求，有一个好用的浏览器插件hackbar,可以帮我们快速改头

![image-20230510093032818](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510093032818.png)

![image-20230510093719721](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510093719721.png)

点击load，modifyheader，找到X-Forward-For如下图，点击Excute

![image-20230510093823859](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510093823859.png)



得到下图

![image-20230510094010466](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510094010466.png)

来源于ctf.com，可以查到referer

![image-20230510094155166](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510094155166.png)



所以按照上过一个方法，再次点击load,modifyheader,这时我们要把上一题的在操作一遍，加上修改的referer，就可以得到flag了

![image-20230510094350044](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510094350044.png)

![image-20230510094357914](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20230510094357914.png)

还可以通过burp改包实现上述操作