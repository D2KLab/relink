rm -rf outs
mkdir outs
mkdir outs/aida-yago2	
mkdir outs/airbus
mkdir outs/apple
mkdir outs/gm
mkdir outs/stock

perl -CS ned-evaluation/goldFiveSentences.pl GOLD/Airbus/ outs/airbus/gold.out
perl -CS ned-evaluation/goldFiveSentences.pl GOLD/Apple/ outs/apple/gold.out
perl -CS ned-evaluation/goldFiveSentences.pl GOLD/GM/ outs/gm/gold.out
perl -CS ned-evaluation/goldFiveSentences.pl GOLD/Stock_Market/ outs/stock/gold.out
perl -CS ned-evaluation/goldAllSentences.pl GOLD/aida_naf/ outs/aida-yago2/gold.out

for corpus in airbus apple gm stock; do
	echo "#######################################################################"
	echo $corpus
	echo "HYBRID 2016"
	echo `perl -CS ned-evaluation/systemFiveSentencesFilip.pl ADEL/$corpus/ byADEL outs/$corpus/hybrid.out outs/$corpus/info1.out`
	echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/hybrid.out outs/$corpus/hybrid_results.out`
	echo "RECON 12"
	echo `perl -CS ned-evaluation/systemFiveSentencesFilip.pl ReCon12/$corpus/ dbp outs/$corpus/recon12.out outs/$corpus/info2.out`
	echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon12.out outs/$corpus/recon12_results.out`
	echo "RECON 13"
	echo `perl -CS ned-evaluation/systemFiveSentencesFilip.pl ReCon13/$corpus/ dbp outs/$corpus/recon13.out outs/$corpus/info3.out`
	echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon13.out outs/$corpus/recon13_results.out`
	echo "RECON 123"
	echo `perl -CS ned-evaluation/systemFiveSentencesFilip.pl ReCon123/$corpus/ dbp outs/$corpus/recon123.out outs/$corpus/info4.out`
	echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon123.out outs/$corpus/recon123_results.out`
	echo "RECON 1234"
	echo `perl -CS ned-evaluation/systemFiveSentencesFilip.pl ReCon1234/$corpus/ dbp outs/$corpus/recon1234.out outs/$corpus/info5.out`
	echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon1234.out outs/$corpus/recon1234_results.out`
done

corpus="aida-yago2"
echo "#######################################################################"
echo $corpus
echo "HYBRID 2016"
echo `perl -CS ned-evaluation/systemAllSentences.pl ADEL/$corpus/ byADEL outs/$corpus/hybrid.out outs/$corpus/info1.out`
echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/hybrid.out outs/$corpus/hybrid_results.out`
echo "RECON 12"
echo `perl -CS ned-evaluation/systemAllSentences.pl ReCon12/$corpus/ dbp outs/$corpus/recon12.out outs/$corpus/info2.out`
echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon12.out outs/$corpus/recon12_results.out`
echo "RECON 13"
echo `perl -CS ned-evaluation/systemAllSentences.pl ReCon13/$corpus/ dbp outs/$corpus/recon13.out outs/$corpus/info3.out`
echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon13.out outs/$corpus/recon13_results.out`
echo "RECON 123"
echo `perl -CS ned-evaluation/systemAllSentences.pl ReCon123/$corpus/ dbp outs/$corpus/recon123.out outs/$corpus/info4.out`
echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon123.out outs/$corpus/recon123_results.out`
echo "RECON 1234"
echo `perl -CS ned-evaluation/systemAllSentences.pl ReCon1234/$corpus/ dbp outs/$corpus/recon1234.out outs/$corpus/info5.out`
echo `perl -CS ned-evaluation/evaluate.pl outs/$corpus/gold.out outs/$corpus/recon1234.out outs/$corpus/recon1234_results.out`
