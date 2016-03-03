### Data generation for the website

#### /DAC-Graph-Library
- papers.pkl <- build\_papers\_dict.py
  + DAC\_Entire\_DataBase.json
  + titlelist.txt <- /data_generation_helper/generate\_corpus.py
  + phrase\_topic\_modelling\_results/outputFiles/document\_topic\_distribution.txt
  + paperid\_titles\_map.csv <- /data_generation_helper/paperIDmap.py
  + authors\_papers\_map.csv <- /data_generation_helper/authorPaperMap.py

- authors.pkl <- build\_authors.py
  + author\_coauthor\_paper\_map.csv <- /data_generation_helper/coauthorMap.py
  + papers.pkl

- authors\_test.json <- build\_authors\_json.py
  + authors.pkl <- build\_authors.py
  + author\_index\_memo.pkl <- build\_authors.py (authorID to index map)

- authors\_central\_test.json <- calculate\_author\_network\_statistics.py
  + authors\_test.json <- build\_authors\_json.py
