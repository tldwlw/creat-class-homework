## HashChain C++优化

### 简介

在HashMap中，其会根据hash算法来计算key-value的存储位置并进行快速存取。

使用的c++ hashmap实际是在普通hashchain的基础上模仿Java的HashMap进行优化。

### HashChain

使用拉链法，数据结构为链表的数组。

对于某个元素，通过哈希算法，根据元素特征计算元素在数组中的下标，从而将元素分配、插入到不同的链表中去。在查找时，同样通过元素特征找到正确的链表，再从链表中找出正确的元素。

### 优化点

#### 1、寻找下标

一般将 hashcode 转化为链表数组中的下标时，是直接使用求模计算，但运算效率较低。位运算直接对内存数据进行操作，不需要转成十进制，处理速度非常快，所以将 hashcode 与 n-1 进行按位与获得小于n的结果。

但对于bin(n-1)结尾为0时，按位与后最后一位永远为0，导致空间的减少，碰撞几率的进一步增加，查询速度慢。所以应该保证数组的大小 n 为 2^m。

#### 2、将元素均匀分配

为了防止产生冲突过多的 hashcode，可将该hashcode 进行扰动计算，防止不同hashCode的高位不同但低位相同导致的hash冲突：

```c++
int Hash(int key) {
	key ^= (key >> 20) ^ (key >> 12);
	return key ^ (key >>  7) ^ (key >>  4);

}
```

### 结果展示

![image](https://github.com/tldwlw/creat-class-homework/blob/main/images/capture_20220731115323306.png)



#### 
