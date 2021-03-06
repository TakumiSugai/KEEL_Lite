KEEL
====

GUI操作に頼らない3Dモデリングツールとして作成  
他のモデリングソフトや、3Dプリンタで読み込み可能な  
STL形式のファイルを出力することが可能  

## Description

寸法や角度を指定しながらコーディングをベースとして  
3Dモデルを作成するライブラリです。  

本ライブラリによって提供される  
コーディングをベースとした3Dモデル開発は再現性が高く、  
好きな部分を切り出して別プロジェクトで再利用したり、  
3Dモデルの設計を他者に共有したりすることが簡単にできます。

本ライブラリが提供する機能は、  
モデリングとSTLファイルの出力のみです。  
別途STLファイルを読み込み可能なViewerをご用意の上、  
使用することをおすすめします。

描画系のライブラリに依存しないため、  
Pyhtonの実行環境があれば、  
スマートフォン等でも動作させることができます

## Requirement

Python 3.7以上で動作

依存ライブラリ
* numpy

## Usage

demoを参照


## Install

### for PC

```
git clone https://github.com/TakumiSugai/KEEL_Lite.git

cd KEEL_Lite

python setup.py install
```

### for Android device

```
# Python実行環境として
# Termux(https://play.google.com/store/apps/details?id=com.termux)を想定
# インストールと初期設定は完了しているものとする

pkg install git python clang fftw

LDFLAGS=" -lm -lcompiler_rt" pip install numpy

git clone https://github.com/TakumiSugai/KEEL_Lite.git

cd KEEL_Lite

python setup.py install
```