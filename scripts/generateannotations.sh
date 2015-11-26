for d in airbus apple gm stock; do 
  for f in $d/*.naf.conll; do
    echo $f; 
    java -jar adel-1.0-SNAPSHOT-jar-with-dependencies.jar -tk linking -of conlle -f $f.txt -a $f -o $f.conlle ;
  done; 
done
