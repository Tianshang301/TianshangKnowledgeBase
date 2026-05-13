# BibTeX 鍏ラ棬涓庝娇鐢?
## 涓€銆佷粈涔堟槸 BibTeX

BibTeX 鏄?LaTeX 鐨勫弬鑰冩枃鐚鐞嗗伐鍏凤紝鐢?Oren Patashnik 浜?1985 骞村紑鍙戙€傚畠閫氳繃鍗曠嫭鐨?.bib 鏂囦欢瀛樺偍鏂囩尞鏁版嵁锛岄厤鍚?.bst 鏍峰紡鏂囦欢鑷姩鐢熸垚鏍煎紡鍖栫殑鍙傝€冩枃鐚垪琛ㄣ€侭ibLaTeX 鏄叾鍚庣户鏂规锛屾彁渚涙洿澶氬姛鑳藉拰鐏垫椿鎬с€?
## 浜屻€?bib 鏂囦欢缁撴瀯

涓€涓?.bib 鏂囦欢鍖呭惈澶氭潯鏂囩尞鏉＄洰锛屾瘡鏉℃潯鐩伒寰互涓嬫牸寮忥細

```
@鏉＄洰绫诲瀷{寮曠敤鏍囩,
  瀛楁1 = {鍊?},
  瀛楁2 = {鍊?},
  ...
}
```

- 寮曠敤鏍囩锛氭鏂囦腑閫氳繃 `\cite{鏍囩}` 寮曠敤
- 瀛楁鍊肩敤鑺辨嫭鍙?`{}` 鎴栧弻寮曞彿 `""` 鍖呰９
- 鍚勫瓧娈典箣闂翠互閫楀彿鍒嗛殧锛堟渶鍚庝竴涓瓧娈靛悗涓嶅姞閫楀彿锛?
## 涓夈€佸父瑙佹潯鐩被鍨嬪姣?
| 鏉＄洰绫诲瀷 | 鐢ㄩ€?| 蹇呭～瀛楁 | 甯哥敤鍙€夊瓧娈?|
|----------|------|----------|-------------|
| @article | 鏈熷垔璁烘枃 | author, title, journal, year, volume | number, pages, doi, issn, month |
| @book | 涔︾睄 | author/editor, title, publisher, year | edition, volume, series, isbn |
| @inproceedings | 浼氳璁烘枃 | author, title, booktitle, year | pages, editor, volume, series, doi |
| @phdthesis | 鍗氬＋璁烘枃 | author, title, school, year | month, address, doi |
| @mastersthesis | 纭曞＋璁烘枃 | author, title, school, year | month, address, type |
| @incollection | 涔︿腑鐨勭珷鑺?| author, title, booktitle, publisher, year | editor, pages, chapter |
| @techreport | 鎶€鏈姤鍛?| author, title, institution, year | number, address, month, type |
| @misc | 鏉傞」 | 鏃犲繀濉?| author, title, howpublished, year, note |
| @proceedings | 浼氳璁烘枃闆?| title, year | editor, publisher, organization |
| @inbook | 涔︿腑鐨勪竴閮ㄥ垎 | author/editor, title, chapter/pages, publisher, year | edition, series |

## 鍥涖€佸瓧娈佃鏄?
鏍稿績瀛楁璇﹁В锛?
- author锛氫綔鑰呭悕锛屽浣滆€呯敤 `and` 鍒嗛殧銆傛牸寮忥細`First Last` 鎴?`Last, First`
  - 绀轰緥锛歚author = {John Smith and Jane Doe}`
- editor锛氱紪鑰咃紙鏍煎紡鍚?author锛?- title锛氭爣棰樸€傚涔﹀悕銆佹湡鍒婂悕浣跨敤澶у皬鍐欐晱鎰熸椂锛岀敤鑺辨嫭鍙蜂繚鎶?  - 绀轰緥锛歚title = {The {LaTeX} Companion}`
- journal锛氭湡鍒婂悕绉?- year锛氬嚭鐗堝勾浠?- volume锛氬嵎鍙?- number锛氭湡鍙凤紙鏈熷垔锛夋垨鎶ュ憡鍙?- pages锛氶〉鐮侊紝鏍煎紡涓?`12--34`锛堜娇鐢ㄥ弻杩炲瓧绗︼級
- publisher锛氬嚭鐗堝晢
- address锛氬嚭鐗堝湴
- doi锛氭暟瀛楀璞℃爣璇嗙
- url锛氬湪绾块摼鎺?- note锛氳ˉ鍏呰鏄?
## 浜斻€佺ず渚?.bib 鏉＄洰

```
@article{li2023deep,
  author    = {Li, Ming and Zhang, Wei and Wang, Yu},
  title     = {Deep Learning for Natural Language Processing: A Comprehensive Survey},
  journal   = {Journal of Artificial Intelligence Research},
  year      = {2023},
  volume    = {76},
  number    = {2},
  pages     = {345--389},
  doi       = {10.1613/jair.1.14567}
}

@book{knuth1984tex,
  author    = {Knuth, Donald E.},
  title     = {The {TeX}book},
  publisher = {Addison-Wesley},
  year      = {1984},
  address   = {Reading, Massachusetts},
  isbn      = {0-201-13448-9}
}

@inproceedings{vaswani2017attention,
  author    = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  title     = {Attention Is All You Need},
  booktitle = {Advances in Neural Information Processing Systems},
  year      = {2017},
  volume    = {30},
  pages     = {5998--6008}
}

@phdthesis{zhang2022representation,
  author  = {Zhang, Yiming},
  title   = {Representation Learning on Graph-Structured Data},
  school  = {Peking University},
  year    = {2022},
  month   = jun
}

@misc{openai2023gpt,
  author       = {{OpenAI}},
  title        = {{GPT}-4 Technical Report},
  howpublished = {arXiv:2303.08774},
  year         = {2023},
  note         = {Preprint}
}
```

## 鍏€佸湪 LaTeX 涓娇鐢?BibTeX

鍩烘湰娴佺▼锛?
1. 鍦?LaTeX 婧愭枃浠朵腑锛?   ```
   \documentclass{article}
   \bibliographystyle{plain}  % 鎸囧畾 .bst 鏍峰紡
   \begin{document}
   ...姝ｆ枃鍐呭锛屼娇鐢?\cite{li2023deep} 寮曠敤...
   \bibliography{myrefs}  % 鎸囧畾 .bib 鏂囦欢锛堜笉鍚墿灞曞悕锛?   \end{document}
   ```

2. 缂栬瘧娴佺▼锛堝洓姝ワ級锛?   ```
   pdflatex paper.tex       % 鐢熸垚 .aux 鏂囦欢
   bibtex paper             % 鏍规嵁 .aux 涓殑寮曠敤鐢熸垚 .bbl
   pdflatex paper.tex       % 鎻掑叆鍙傝€冩枃鐚?   pdflatex paper.tex       % 鏇存柊浜ゅ弶寮曠敤
   ```

3. 甯哥敤寮曠敤鍛戒护锛?   - `\cite{key}` 鈥?鏍囧噯寮曠敤
   - `\citep{key}` 鈥?鎷彿寮曠敤锛堥渶 natbib 鍖咃級
   - `\citet{key}` 鈥?鏂囨湰寮曠敤锛堥渶 natbib 鍖咃級
   - `\cite[page 12]{key}` 鈥?甯﹂〉鐮佸紩鐢?   - `\nocite{*}` 鈥?鍒楀嚭 .bib 涓墍鏈夋枃鐚?   - `\citen{key}` 鈥?涓婃爣寮曠敤

## 涓冦€丅ibTeX 鏍峰紡鏂囦欢锛?bst锛?
甯哥敤鍐呯疆鏍峰紡锛?
| 鏍峰紡 | 寮曠敤鏍煎紡 | 鍙傝€冩枃鐚牸寮?|
|------|----------|-------------|
| plain | [1] 鏁板瓧缂栧彿 | 鎸夐娆″紩鐢ㄩ『搴忔帓鍒?|
| unsrt | [1] 鏁板瓧缂栧彿 | 鎸夊紩鐢ㄥ嚭鐜伴『搴忔帓鍒楋紙鍚?plain 浣嗛『搴忎笉鍚岋級 |
| alpha | [Knu84] 浣滆€?骞翠唤缂╁啓 | 鎸夋爣绛惧瓧姣嶉『搴忔帓鍒?|
| abbrv | [1] 鏁板瓧缂栧彿 | 鍚嶅瓧銆佹湀浠界瓑缂╁啓 |
| apalike | (Knuth, 1984) | 钁楄€?鍑虹増骞村埗 |
| ieeetr | [1] 鏁板瓧缂栧彿 | IEEE 鏍煎紡 |
| siam | [1] 鏁板瓧缂栧彿 | SIAM 鏈熷垔鏍煎紡 |

鑷畾涔夋牱寮忓彲浣跨敤 `makebst` 宸ュ叿锛堥殢 LaTeX 鍙戣鐗堟彁渚涳級浜や簰寮忕敓鎴愩€?
## 鍏€佸父瑙侀棶棰樹笌鎶€宸?
| 闂 | 瑙ｅ喅鏂规硶 |
|------|----------|
| 寮曠敤闂彿鍑虹幇 | 閲嶆柊缂栬瘧锛歱dflatex -> bibtex -> pdflatex x2 |
| 鐗规畩瀛楃澶勭悊 | 浣跨敤 `{\"o}` 鎴?`\"o` 琛ㄧず umlaut 绛夊彉闊崇鍙?|
| 涓枃鏂囩尞 | 浣跨敤 `ctex` 鍖咃紝BibTeX 閰嶅悎 `gbt7714` 鏍峰紡 |
| URL 杩囬暱鎹㈣ | 浣跨敤 `url` 鍖咃紝鎴?`\usepackage{breakurl}` |
| 鍚屼竴浣滆€呭绡囨枃鐚?| 鍦?year 鍚庡姞 a, b, c 鍖哄垎锛堝 2023a, 2023b锛?|
| 鏍囬淇濇寔澶у皬鍐?| 瀵逛笓鏈夊悕璇嶇敤鑺辨嫭鍙峰寘瑁癸細`{Deep Learning}` |

## 鍙傝€冭祫婧?
- BibTeX 瀹樻柟鏂囨。锛歵ug.org/bibtex
- LaTeX 缁村熀鐧剧锛歟n.wikibooks.org/wiki/LaTeX/Bibliography_Management
- Oetiker 绛変汉銆奣he Not So Short Introduction to LaTeX銆?- GB/T 7714-2015 淇℃伅涓庢枃鐚弬鑰冩枃鐚憲褰曡鍒?- JabRef 鍙傝€冩枃鐚鐞嗚蒋浠讹細jabref.org
- biblatex 鍖呮枃妗ｏ細ctan.org/pkg/biblatex
- natbib 鍖呮枃妗ｏ細ctan.org/pkg/natbib

## 鐩稿叧鏉＄洰

[[AcademicPapers]], CitationManagement, [[ResearchMethods]], [[LaTeX]]
