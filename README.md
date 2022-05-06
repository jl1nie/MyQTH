# MyQTH / MyAct
MyQTHはJavascriptを使って端末の位置情報を取り出し、myqth.gaのリバースジオコーダを使ってJCC/JCGコードを国土地理院地図に表示するシステムです。

MYActはMyQTHにJAFF/POTAの公園位置情報とSOTAのサミットを表示するシステムで、各々myqth.gaのリバースジオコーダを使って国土地理院地図上に情報を表示しています。

***
## エリア情報の作り方
公園の領域情報は国土地理院地図の自然公園の領域情報を使って生成しています。
|ファイル名| 内容 |
|:--------|:-----|
|A10-10.geojson| 国土地理院地図の自然公園の領域情報をQGISを使ってGeoJSON形式で保存したもの|
|A10-10-property.xml| GeoJSON中に振られたIDと公園名を紐づける定義ファイル|

まず最初にJAFF/POTAの公園名称・リファレンスコードが入ったsqliteのデータベースを作成します。
```
sh makedump.sh
```
このスクリプトは`JAFFPOTAXref.csv`で定義されているコードをsqliteのデータベースにインポートすると共にデータベースのダンプを行います。

次に`A10-10.geojson`にJAFF/POTAのコードを振ります。
```
python importpotajaff.py
```
このスクリプトは`A10-10.geojson`を読み込み`A10-10-property.xml`とsqliteのデータベースから各領域にJAFF/POTAのリファレンスコード`JAFF`,`POTA`とユニークなID`UID`を属性として付与し`jaffpota.geojson`として出力します。同時に公園の形状から面積を求めsqliteのデータベースで該当する公園の面積データを更新します。この面積のデータはMyActでどのズームレベルでどの大きさの公園まで表示するか判断するために使われます。

`jaffpota.geojson`はファイルサイズが大きいため[Map Shaper](https://mapshaper.org/)を使ってファイルをTopoJSON形式に変換します。地図上に`jaffpota.geojson`をドラッグ後、Simplifyのメニューで25%程度まで圧縮します。その後ExportでTopoJSON形式で`jaffpota.json`というファイル名で保存してください。

最後にこのTopoJSONファイルの各領域に公園名を入れます。
```
python addanotation.py
```
このスクリプトでは各領域に名称を付与する共に瀬戸内海国立公園のようにエリアが細分化されている場合、エリア毎に振られたUID単位で名称の再設定をしています。このスクリプトで生成された`jaffpota-annotated.json`が最終的にMyActから読み込まれる領域ファイルになります。
