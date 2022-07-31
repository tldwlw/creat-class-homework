#pragma once
#include<string>
//shi#include<pthread.h>
#include<unordered_map>

//Hash函数
//普通时冲突较多
//进行扰动计算，防止不同高位不同但低位相同导致的hash冲突
int Hash(int key) {
	key ^= (key >> 20) ^ (key >> 12);
	return key ^ (key >>  7) ^ (key >>  4);

}
int Hash1(int key) {
	
	return key;

}

class HashMap {
	class Node {
	public:
		const int key;
		int val;
		const int hash;
		Node* next = NULL;
		Node(int hash, int key, int val) :hash(hash), key(key), val(val) {

		}

		Node* findNode(const int& key) {
			Node* node = this;
			while (node != NULL && node->key != key)
				node = node->next;
			return node;
		}
	};
	using NodePtr = Node*;
	NodePtr* table;

	const double load_factor = 0.75;  //负载因子
	int threshold = 12;  //扩容阈值：load_factor*size
	int size = 1 << 4;  //table大小,
	int maxSize = 1 << 30;  //table最大尺寸
	int count = 0;  //当前元素

	//扩容为2^n
	void resize() {
		if (size >= maxSize) return;
		int newSize = size << 1;
		NodePtr* newTable = new NodePtr[newSize];
		memset(newTable, 0, newSize * sizeof(NodePtr));
		for (int i = 0; i < size; ++i) {
			Node* node = table[i];
			while (node != NULL) {
				int index = node->hash & (newSize - 1);
				//按位与的操作跟取模运算并不等价，这可能会带来index分布不均匀问题
				//只有在2^n时二者等价
				Node* tmp = node->next;
				node->next = newTable[index];
				newTable[index] = node;
				node = tmp;
			}
		}
		std::swap(newTable, table);
		size = newSize;
		threshold = size * load_factor;
		delete[] newTable;
	}

	//增加count
	void addCount(int x) {
		count += x;
		if (count > threshold)
			resize();
	}

public:
	HashMap() {
		table = new NodePtr[size];
		memset(table, 0, size * sizeof(NodePtr));
	}
	~HashMap() {
		for (int i = 0; i < size; ++i) {
			Node* node = table[i];
			while (node != NULL) {
				Node* tmp = node->next;
				delete node;
				node = tmp;
			}
			table[i] = NULL;
		}
		delete[] table;
	}
	HashMap(const HashMap&) = delete;
	HashMap& operator=(const HashMap&) = delete;

	//获取值,
	//不存在key，返回false

	bool get(int key, int& value) {
		int hash = Hash(key);
		Node* node = NULL;
		int index = hash & (size - 1);
		if (table[index] != NULL)
			node = table[index]->findNode(key);
		if (node != NULL) value = node->val;
		return node != NULL;
	}

	//放入值
	void put(int key, int value) {
		int hash = Hash(key);
		Node* node = NULL;
		int index = hash & (size - 1);
		if (table[index] != NULL)
			node = table[index]->findNode(key);
		if (node != NULL) node->val = value;
		else {
			node = new Node(hash, key, value);
			node->next = table[index];
			table[index] = node;
			addCount(1);
		}
	}
	
};


class HashMap1 {
	class Node {
	public:
		const int key;
		int val;
		const int hash;
		Node* next = NULL;
		Node(int hash, int key, int val) :hash(hash), key(key), val(val) {

		}

		Node* findNode(const int& key) {
			Node* node = this;
			while (node != NULL && node->key != key)
				node = node->next;
			return node;
		}
	};
	using NodePtr = Node*;
	NodePtr* table;

	const double load_factor = 0.75;  //负载因子
	int threshold = 12;  //扩容阈值：load_factor*size
	int size = 1 << 4;  //table大小,
	int maxSize = 1 << 30;  //table最大尺寸
	int count = 0;  //当前元素

	//扩容为2^n
	void resize() {
		if (size >= maxSize) return;
		int newSize = size << 1;
		NodePtr* newTable = new NodePtr[newSize];
		memset(newTable, 0, newSize * sizeof(NodePtr));
		for (int i = 0; i < size; ++i) {
			Node* node = table[i];
			while (node != NULL) {
				int index = node->hash%newSize;
				//按位与的操作跟取模运算并不等价，这可能会带来index分布不均匀问题
				//只有在2^n时二者等价
				Node* tmp = node->next;
				node->next = newTable[index];
				newTable[index] = node;
				node = tmp;
			}
		}
		std::swap(newTable, table);
		size = newSize;
		threshold = size * load_factor;
		delete[] newTable;
	}

	//增加count
	void addCount(int x) {
		count += x;
		if (count > threshold)
			resize();
	}

public:
	HashMap1() {
		table = new NodePtr[size];
		memset(table, 0, size * sizeof(NodePtr));
	}
	~HashMap1() {
		for (int i = 0; i < size; ++i) {
			Node* node = table[i];
			while (node != NULL) {
				Node* tmp = node->next;
				delete node;
				node = tmp;
			}
			table[i] = NULL;
		}
		delete[] table;
	}
	HashMap1(const HashMap1&) = delete;
	HashMap1& operator=(const HashMap1&) = delete;

	//获取值,
	//不存在key，返回false

	bool get(int key, int& value) {
		int hash = Hash(key);
		Node* node = NULL;
		int index = hash %size;
		if (table[index] != NULL)
			node = table[index]->findNode(key);
		if (node != NULL) value = node->val;
		return node != NULL;
	}

	//放入值
	void put(int key, int value) {
		int hash = Hash(key);
		Node* node = NULL;
		int index = hash %size ;
		if (table[index] != NULL)
			node = table[index]->findNode(key);
		if (node != NULL) node->val = value;
		else {
			node = new Node(hash, key, value);
			node->next = table[index];
			table[index] = node;
			addCount(1);
		}
	}

};

/*
//红黑树
struct hashmap {
	static const int _TONG = 51007;
	unordered_map<int, int> h[_TONG];
	int f1(int e) {  //映射函数
		return e % _TONG;
	}

	bool add(int e, int val) {    //添加(e,val)到map,
		if (!h[f1(e)].empty() || !h[f1(e)].count(e)) {
			h[f1(e)][e] = val;
			return 1;
		}
		else return 0;
	}

	int get(int e) {     //获取map[e]
		return h[f1(e)][e];
	}

	bool count(int e) {    //查找是否存在这个key
		return h[f1(e)].empty() && h[f1(e)].count(e);
	}
};*/
