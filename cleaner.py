#!/usr/bin/env python
"""Excel / CSV 数据清洗工具。"""

import argparse
from pathlib import Path

import pandas as pd


def load(path: Path, sheet: str | None) -> pd.DataFrame:
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=sheet or 0)
    return pd.read_csv(path)


def save(df: pd.DataFrame, path: Path, sheet: str | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() in (".xlsx", ".xls"):
        df.to_excel(path, index=False, sheet_name=sheet or "Sheet1")
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")


def clean(df: pd.DataFrame, args) -> tuple[pd.DataFrame, list[str]]:
    report: list[str] = []
    before = len(df)

    # 1. 列名去空格
    df.columns = [str(c).strip() for c in df.columns]

    # 2. 单元格文本去首尾空格
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)

    # 3. 删空行
    if not args.no_dropna:
        df = df.dropna(how="all")
        report.append(f"删除空行 {before - len(df)} 行")

    # 4. 去重
    if not args.no_dropdup:
        n = len(df)
        subset = args.subset.split(",") if args.subset else None
        if subset:
            subset = [s.strip() for s in subset if s.strip() in df.columns]
        df = df.drop_duplicates(subset=subset or None)
        report.append(f"删除重复行 {n - len(df)} 行")

    report.append(f"最终 {len(df)} 行 x {len(df.columns)} 列")
    return df, report


def main() -> int:
    parser = argparse.ArgumentParser(description="Excel/CSV 数据清洗")
    parser.add_argument("input", help="输入文件")
    parser.add_argument("-o", "--output", help="输出文件")
    parser.add_argument("--no-dropna", action="store_true", help="不删除空行")
    parser.add_argument("--no-dropdup", action="store_true", help="不去重")
    parser.add_argument("--subset", help="去重参考列，逗号分隔")
    parser.add_argument("--sheet", help="工作表名")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.is_file():
        print(f"[错误] 文件不存在: {src}")
        return 1

    try:
        df = load(src, args.sheet)
    except Exception as exc:
        print(f"[错误] 读取失败: {exc}")
        return 1

    cleaned, report = clean(df, args)

    if args.output:
        out = Path(args.output)
    else:
        out = src.parent / "cleaned" / f"{src.stem}_cleaned{src.suffix}"
    save(cleaned, out, args.sheet)

    print("清洗完成：")
    for line in report:
        print("  - " + line)
    print(f"输出: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())