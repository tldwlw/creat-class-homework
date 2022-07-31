## 创新创业作业

### 个人

姓名：罗网

账号：tldwlw

### 项目

详细说明在对应文件

#### SM3的长度扩展攻击

对于一般的MAC算法是：把secret和message连接到一起，然后取摘要。当知道hash(secret + message)的值及secret长度的情况下，可以轻松推算出hash(secret + message||padding||m’)。当填充后，原始hash值与添加扩展字符串并覆盖初始链变量所计算出来的一样。这是因为攻击者的哈希计算过程，相当于从计算过程的一半紧接着进行下去。此hash值便能通过验证。

#### HashChain

HashChain是 Key-Value 对映射的抽象接口，该映射不包括重复的键，即一个键对应一个值。实际上就是一个链表的数组，对于每个 key-value对元素，根据其key的哈希，该元素被分配到某个桶当中，桶使用链表实现，链表的节点包含了一个key，一个value，以及一个指向下一个节点的指针。

### 参考资料

[长度扩展攻击详解](https://blog.csdn.net/szuaurora/article/details/78125585)

[C++简单实现HashMap](https://blog.csdn.net/xin_hen/article/details/108166528?spm=1001.2101.3001.6650.7&amp;utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-7-108166528-blog-81588983.pc_relevant_multi_platform_whitelistv3&amp;depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-7-108166528-blog-81588983.pc_relevant_multi_platform_whitelistv3&amp;utm_relevant_index=10)


