什么逝http

打开题目看到很明显的提示，must local user,所以搜索有关http请求头的信息，可以了解到X-Forward-For

![image-20230510093032818](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/86eb5652-fcc5-454d-9c7c-89d19a9baffa)

xff 是http的拓展头部，作用是使Web服务器获取访问用户的IP真实地址（可伪造）。由于很多用户通过代理服务器进行访问，服务器只能获取代理服务器的IP地址，而xff的作用在于记录用户的真实IP，以及代理服务器的IP。

我们可以通过修改xff达到要求，有一个好用的浏览器插件hackbar,可以帮我们快速改头
![image-20230510093719721](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/9fb60119-3b28-413d-ab91-6beaffe4b941)


点击load，modifyheader，找到X-Forward-For 添加127.0.0.1如下图，点击Excute


![image-20230510093823859](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/599d63cc-c64a-4099-b12a-9c6e825039a5)


得到下图
![image-20230510093939608](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/0f51ec1c-7a5f-4e31-9558-4062ab08c9fa)

来源于ctf.com，可以查到referer
![image-20230510094155166](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/75a30136-7d44-4d90-8a5c-5634dc77e88c)


![image-20230510094155166](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/7d00fa8b-f670-4899-9b5f-adf99b9db13a)



所以按照上过一个方法，再次点击load,modifyheader,这时我们要把上一题的在操作一遍，加上修改的referer，就可以得到flag了
![image-20230510094350044](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/71242adb-16cd-43d3-95eb-c21c1e81c131)
![image-20230510094357914](https://github.com/r00t-security-lab/rtctf2023/assets/105710395/fa61cb6c-82f4-4bab-b911-205ed9ce86e8)



还可以通过burp改包实现上述操作
