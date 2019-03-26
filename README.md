# MayaSquid
## Description
Tools for Maya.

## Install
まずリポジトリをクローン、もしくは[release](https://github.com/tm8r/MayaSquid/releases/)よりダウンロードしたzipを解凍してください。\
次に、`MayaSquid.mod` を `MAYA_MODULE_PATH` が通ったところにコピーし、ファイルの1行目の「.」を解凍先のパスに書き換えてください。
```
+ MayaSquid 1.0 /Users/tm8r/Documents/MayaSquid
```
もしくは、解凍先のディレクトリをMaya.envに以下のように追記してください。
```
MAYA_MODULE_PATH=/Users/tm8r/Documents/MayaSquid
```
※既にMaya.envにMAYA_MODULE_PATHが設定されている場合は、その行の末尾に「;」を追加し、その後にパスを追記してください。

上記の作業後にMayaを起動してメニューバーに「Squid」が追加されていれば成功です。

## Inspector
メニューバーのSquid>Inspectorから起動します。

選択ノードのMaterial、Constraintといった情報にアクセスしやすくします。
![maya_inspector](https://user-images.githubusercontent.com/1896961/54471737-474e6d00-4801-11e9-967f-621b8dce2de9.gif)

## License
[MIT](https://en.wikipedia.org/wiki/MIT_License)

## Author
tm8r (https://github.com/tm8r)
