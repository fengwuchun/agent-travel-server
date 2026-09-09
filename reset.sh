#!/bin/bash




echo "删除target目录..."

rm -rf target


echo "删除macOS ._* 文件..."

find . -name "._*" -type f -delete 2>/dev/null


echo "完成!"