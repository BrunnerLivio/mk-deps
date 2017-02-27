# mk-deps
Cli tool for installing runtime dependencies of a debian package
# Usage
```
mk-deps [OPTIONS]
mk-deps --install debian/control
mk-deps --install debian/control -p {PACKAGE_NAME}
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

## Try it out with docker

Use the Docker file to create your image and play around with mk-deps, without polluting 
your main system

1. Install Docker, following the instructions https://docs.docker.com/engine/installation/
2. Build your docker image: `docker build -t $USER/mk-deps .`
3. Create a container from this image: `docker run -t -i $USER/mk-deps bash`

4. Build and install the package inside the container `debuild -us -uc && dpkg -i ../mk-deps*.deb`
5. Play around `mk-deps --install tests/input/tsp-web.control`


# Limits

Some packages use variables inside runtime dependencies. mk-deps is (yet) not
able to get the value of these variables. 