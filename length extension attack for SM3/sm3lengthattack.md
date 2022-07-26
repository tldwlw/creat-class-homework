## 实验目的

实现对SM3的长度扩展攻击

## 实验原理

长度扩展攻击（length extension attack），是指针对某些允许包含额外信息的散列函数的攻击手段。

SM3的消息填充：以64字节的数据分组作为输入；在填充时先填充一个 1 ，后面加上k个 0 满足(n+1+k) mod 64 = 56；再追加8字节。

SM3的消息扩展：不直接使用数据分组；将每个64字节的数据分组分为每个8字节、共8个的消息字；第一个分组的8个消息字递推生成之后的消息字。

攻击时，根据消息扩展原理，即使不知道加密的消息，但已知消息的长度。只要得到第一次加密后的8个消息字，通过对任意假消息后填充并附加消息，即可构造。

## 实现过程

1. 随机生成secret，并得到对应的hash值secrethash
2. 随机生成附加消息m。用secrehash推算出该次加密后的8个消息字，用其加密m得到hashguess
3. 如果secrehash+padding+m的hash值new_hash与hashguess相同，则说明攻击成功

## 实验结果

![image](https://github.com/tldwlw/creat-class-homework/blob/main/images/capture_20220728000144578.png)



