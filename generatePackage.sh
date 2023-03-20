version=1.0.0-alpha

rm -r ./build

python -m venv env
source env/bin/activate
pip install -r requirements.txt
python setup.py build

cd ./build/exe.*

tar -cvf cims-bot-$version.tar lib/ main

cp -r cims-bot-$version.tar ../ 

cd ..

rm -r exe.*
