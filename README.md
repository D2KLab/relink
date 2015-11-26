# relink

#### external modules:
- Hybrid Annotator:   please contact @giusepperizzo
- ReCon : https://github.com/filipdbrsk/NWRDomainModel
- scorer: https://github.com/newsreader/evaluation/tree/master/ned-evaluation

#### workflow:
    txt: plain text , token: tokenized text -> adel -> conlle: annotations in conll extended format
    
    conlle -> conll2naf.py -> naf
    
    naf -> recon -> out:reranked links
    
#### datasets
The dataset consists of 120 English Wikinews articles annotated with entities, events, temporal expressions and semantic roles. In the entity annotation layer, links to DBpedia are included in the context of the NewsReader project. The WikiNews corpus articles are split into four sub-corpora each revolving the following core topics:  1)  Airbus  Boeing, 2) Apple Inc., 3) General Motors, Ford and Chrysler, and 4) the Stock market.

#### scripts
...

#### licence


#### team
* Giuseppe Rizzo 
* Filip Ilievski
* Marieke van Erp
* Julien Plu
* Raphael Troncy
