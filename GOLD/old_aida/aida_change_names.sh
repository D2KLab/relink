for old in *testb.naf; do 
#	mv $old `basename $old .txt`.md
	num=${old:0:4}
	newnum=$((num-1162))
	mv $old "$newnum.conll.naf"
done
