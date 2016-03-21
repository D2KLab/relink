#!/bin/bash

rm -r ../ReCon1*

mkdir ../ReCon12
mkdir ../ReCon12/aida-yago2	
mkdir ../ReCon12/airbus
mkdir ../ReCon12/apple
mkdir ../ReCon12/gm
mkdir ../ReCon12/stock

cp -r ../ReCon12 ../ReCon13
cp -r ../ReCon12 ../ReCon123
cp -r ../ReCon12 ../ReCon1234

python3 recon_encoding.py airbus 12 False
python3 recon_encoding.py apple 12 False
python3 recon_encoding.py gm 12 False
python3 recon_encoding.py stock 12 False
python3 recon_encoding.py aida-yago2 12 False

python3 recon_encoding.py airbus 13 False
python3 recon_encoding.py apple 13 False
python3 recon_encoding.py gm 13 False
python3 recon_encoding.py stock 13 False
python3 recon_encoding.py aida-yago2 13 False

python3 recon_encoding.py airbus 123 False
python3 recon_encoding.py apple 123 False
python3 recon_encoding.py gm 123 False
python3 recon_encoding.py stock 123 False
python3 recon_encoding.py aida-yago2 123 False

python3 recon_encoding.py airbus 123 True
python3 recon_encoding.py apple 123 True
python3 recon_encoding.py gm 123 True
python3 recon_encoding.py stock 123 True
python3 recon_encoding.py aida-yago2 123 True
