# Movie Recommendation Demo

社内勉強会で発表した[Scrapyとscikit-learn、Streamlitで作るかんたん機械学習アプリケーション](https://speakerdeck.com/amaotone/making-ml-app-with-scrapy-scikit-learn-and-streamlit)で作成したデモアプリです。

## Usage

Python3.7とPoetryが必要です。

### Poetryで作った仮想環境の有効化

```bash
$ poetry install
$ poetry shell
```

### クローリング

予め `crawler/crawler/settings.py` の `USER_AGENT` を自分のものに編集してください。

```python
USER_AGENT = "movie-recommend-crawler (+hoge@fuga.com)"
```

クロールは `./crawler` ディレクトリ内で行います。

```bash
$ cd crawler
$ scrapy crawl jtnews
$ mv *.csv ../data
```

### モデルの訓練

```bash
$ python train.py
```

### デモアプリの起動

```bash
$ streamlit run app.py
```

## Author

Amane Suzuki <amane.suzu@gmail.com>

疑問点などあれば [@SakuEji](https://twitter.com/SakuEji) までお気軽にどうぞ。
