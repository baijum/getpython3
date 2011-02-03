VE=`pwd`/ve
echo "Creating virtualenv"
virtualenv --clear --no-site-packages $VE
echo "Installing PIL"
wget -c http://dist.repoze.org/PIL-1.1.6.tar.gz
$VE/bin/easy_install PIL-1.1.6.tar.gz 
echo "Installing dependencies"
$VE/bin/python setup.py develop
$VE/bin/easy_install Flask
echo "Creating tables"
$VE/bin/python create_tables.py
echo "Populating tables with data"
$VE/bin/python populate_packages.py --demo
echo "Running server"
$VE/bin/python runserver.py
