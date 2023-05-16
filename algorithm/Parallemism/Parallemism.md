# 提供信息

origin=0123456789abcdefghijklmnopqrstuvwxyz

change=xh7sm1vj3gfqdciea98wpknt64lyur2z0ob5



target=!_sii0iituymnajgx1h!gnaw1{x!e30}rniy

# 解题思路

首先~~观察~~可以的得出origin和change的长度一样，包含的字符也一样，复原一下位置映射关系：

```python
for i in origin:
    for j in change:
        if i==j:
            print(change.index(j),end=',')
        break

'''parallelism order:
33, 17, 7, 28, 22, 1, 31, 19, 3, 16, 15, 26, 13, 12, 18, 14, 10, 9, 8, 32, 25, 20, 23, 29, 6, 4, 21, 34, 30, 27, 2, 35, 0, 24, 11, 5'''
```

直接用这个映射关系重排target即可得到flag:**r00t{y1sh1xiangyu_jinxiangm3iwei!!!}**



但其实本题不需要知道具体的位置映射关系便能解出：

```python
for i in range(len(change)):
    print(target[change.index(origin[i])],end=' ')
```



