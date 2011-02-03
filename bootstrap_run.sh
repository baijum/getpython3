echo "Creating virtualenv"
virtualenv --clear --no-site-packages ve
echo "Installing PIL"
wget -c http://dist.repoze.org/PIL-1.1.6.tar.gz
./ve/bin/easy_install PIL-1.1.6.tar.gz 
echo "Installing dependencies"
./ve/bin/python setup.py develop
echo "Creating tables"
./ve/bin/python create_tables.py
echo "Populating tables with data"
./ve/bin/python populate_packages.py --demo
echo "Running server"
./ve/bin/python runserver.py
