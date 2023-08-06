# Senta工具介绍
## Senta 工具介绍
Senta是一个情感分析工具。与传统的情感分析工具相比，其具有以下特点与优势：
1. 通过pip命令安装Senta后，一行代码即可进行情感预测，非常方便，
2. Senta支持用户指定训练数据对模型进行重训，使得其在新的领域达到更好的效果，
3. Senta是基于字粒度的情感分类模型，避免了中文分词同时在效果上达到基于词粒度的情感分类模型，
4. 我们对模型进行了一定的速率优化，使得模型更为轻便高效
5. 我们团队会对模型进行持续优化。

## 安装与使用
### 安装说明
- 代码对Python2/3均兼容，在联网情况下可直接通过pip进行安装
```
pip install Senta==1.0.1
```
- 也可以先到网站[https://pypi.org/project/Senta/1.0.1/](https://pypi.org/project/Senta/1.0.1/)下载Senta-1.0.1-py2.py3-none-any.whl安装包或Senta-1.0.1.tar.gz压缩包进行安装：

```
# 对于Senta-1.0.1-py2.py3-none-any.whl安装包
pip install Senta-1.0.1-py2.py3-none-any.whl 

# 对于Senta-1.0.1.tar.gz压缩包
tar -zxvf Senta-1.0.1.tar.gz
cd Senta-1.0.1
python setup.py install
```

### 功能与使用
#### 分词
- 代码示例：
```
from Senta import Senta
senta = Senta()

# 单个样本输入，输入为Unicode编码的字符串
text = u"百度是一家高科技公司"
result = senta.predict(text)

# 批量样本输入, 输入为多个句子组成的list，平均速率更快
texts = [u"中山大学是岭南第一学府", u"百度是一家高科技公司"]
result = senta.predict(texts)
```
- 输出：
对于一个样本的输出是一个元组，其元素分别为：输入句子，预测的情感，负向情感的概率，正向情感的概率。
```text
【单样本】：result = [('百度是一家高科技公司', 1, 0.3747188150882721, 0.6252812147140503)]
【批量样本】：result = [('中山大学是岭南第一学府', 1, 0.33073002099990845, 0.6692699790000916), ('百度是一家高科技公司', 1, 0.3747188150882721, 0.6252812147140503)]
```

#### 增量训练
- 代码示例

```
from Senta import Senta
senta = Senta()

# 训练和测试数据集
# 数据样例可查看：https://baidu-nlp.bj.bcebos.com/sentiment_classification-dataset-1.0.0.tar.gz
train_file = "./data/train.tsv"
test_file = "./data/test.tsv"
senta.train(model_save_dir='./my_model/',train_data=train_file, test_data=test_file)

# 使用自己训练好的模型
my_senta = Senta(model_path='my_model')
```

文件结构
---

```text
.
├── Senta
│   ├── _compat.py              # 兼容Python2和Python3的脚本
│   ├── conf                    # 使用到的相关配置字典
│   ├── demo.py                 # Senta的使用示例
│   ├── infer_model             # 预训练好的模型
│   ├── __init__.py             # Senta类的封装代码
│   ├── nets.py                 # Senta的Paddle模型的代码
│   ├── reader.py               # 读取数据的代码
│   ├── run_classifier.py       # 模型训练的代码
│   ├── senta_config.json       # 模型训练时的配置文件 
│   └── utils.py                # 使用的工具函数
├── README.md                   # 本文件
└── setup.py                    # 模型生成安装包脚本

```

版本信息
---
本项目的各版本信息和变更历史可以在[这里][changelog]查看。

维护者
---
### owners


### committers


讨论
---
百度Hi交流群：群号


[changelog]: http://icode.baidu.com/repos/baidu/nlp/Senta/blob/master:CHANGELOG.md
