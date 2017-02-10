# mk-deps
Cli tool for installing runtime dependencies of a debian package
# Usage
```
mk-deps [OPTIONS]
mk-deps --install debian/control
```
# Installation

## From Source
1. Clone the repository
2. Run the following commands
```
sudo apt-get install fakeroot dh-make build-essential devscripts # Packages nessesary for building package
cd mk-deps
debuild -us -uc # Build the package
sudo dpkg -i ../mk-deps*.deb # Install the package
```

# Limits

Some packages use variables inside runtime dependencies. mk-deps is (yet) not
able to get the value of these variables. 