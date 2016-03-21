# ReLink

#### ReLink in a nutshell
ReLink consists of two consecutive modules:
- General-purpose Hybrid Annotator
- Set of Domain Heuristics, ReCon (first version of ReCon is developed within the NewsReader project - https://github.com/filipdbrsk/NWRDomainModel)

For consistency in terms of evaluation we reuse and adapt NewsReader's evaluation scripts found at: https://github.com/newsreader/evaluation/tree/master/ned-evaluation.

#### Run ReLink

1. Run the hybrid annotator (ReLink step 1 out of 2) to annotate entities in .txt files. Please contact [@giusepperizzo](https://github.com/giusepperizzo) for the latest version of this annotator.
2. Run scripts/generateannotations.sh to produce annotations in conll extended format (.conlle).
3. Run scripts/conll2naf_encoding.py to convert all annotated files to .naf format, which is used by ReCon and by our scoring scripts.
4. Run scripts/run_recon.sh to rerank the results according to ReCon, the second step of ReLink.
 
Note: Along these steps, ensure you supply the correct parameters to the scripts. If any problems, feel free to contact us.

#### Dependencies for the ReCon module:
- Install dbpediaEnquirerPy from https://github.com/rubenIzquierdo/dbpediaEnquirerPy
- Install KafNafParserPy from https://github.com/cltl/KafNafParserPy
- Download the dictionary file for lemma-to-entity information from https://www.dropbox.com/s/rl6ypazj2a9wnt5/lemma.json?dl=0

#### Summary of the format workflow
    txt: plain text , token: tokenized text -> adel -> conlle: annotations in conll extended format
    
    conlle -> conll2naf.py -> naf
    
    naf -> recon -> out:reranked links

### LREC 2016 experiments

#### Datasets

- MEANTIME corpus: http://www.newsreader-project.eu/results/data/wikinews/
- AIDA-YAGO2 dataset: https://www.mpi-inf.mpg.de/departments/databases-and-information-systems/research/yago-naga/aida/downloads/

For convenience of potential replicators, we provide the .naf versions of the gold standard versions of these datasets in the GOLD/ folder. 

If desired, our replicators are also welcome to download the TSV version of AIDA-YAGO2 and convert it to NAF themselves using scripts/aida2naf_encoding.py.

The files found on github which implement the sequence of four instructions to run ReLink noted above, contain the default settings to evaluate ReLink on the datasets AIDA-YAGO2 and MEANTIME. 

#### Scoring

The adapted version of NewsReader's scorers can be found in the ned-evaluation/ folder. See the script evaluate.sh for the set of commands we used to evaluate our solutions for our LREC 2016 paper. For understanding of potential replicators, we detail briefly the operation of these scoring functions. They consist of three Perl scripts:
- Analyze system annotations (ned-evaluation/systemFiveSentencesFilip.pl or ned-evaluation/systemAllSentences.pl) and transform the .naf files in a folder to a single output file
- Analyze gold standard data (ned-evaluation/goldFiveSentences.pl or ned-evaluation/goldAllSentences.pl) and transform the .naf files in a folder to a single output file
- Compare the outputs of the previous two files, using the script ned-evaluation/evaluate.pl. For correct evaluation, you should ensure the filenames of the previous two steps coincide.
    
### Licence
http://www.apache.org/licenses/LICENSE-2.0

### Team
* Giuseppe Rizzo 
* Filip Ilievski
* Marieke van Erp
* Julien Plu
* Raphael Troncy
