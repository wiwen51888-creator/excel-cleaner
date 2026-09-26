# excel-cleaner

Excel / CSV 数据清洗工具。一键去除空行、重复行、首尾空格，统一格式。

## 安装

```bash
pip install -r requirements.txt
```

## 用法

```bash
# 清洗单个文件（输出到 ./cleaned）
python cleaner.py data.xlsx

# 指定输出文件
python cleaner.py data.csv -o clean.csv

# 只去重，不删空行
python cleaner.py data.xlsx --no-dropna

# 去重时只按指定列判断
python cleaner.py data.xlsx --subset 姓名,电话

# 指定工作表
python cleaner.py data.xlsx --sheet Sheet2
```

## 会做的事

1. 去除完全空白的行
2. 去除重复行（可指定列）
3. 去除单元格首尾空格
4. 列名去空格
5. 输出为同格式文件

## 参数

- `-o/--output`：输出文件路径
- `--no-dropna`：不删除空行
- `--no-dropdup`：不去重
- `--subset`：去重参考列，逗号分隔
- `--sheet`：Excel 工作表名