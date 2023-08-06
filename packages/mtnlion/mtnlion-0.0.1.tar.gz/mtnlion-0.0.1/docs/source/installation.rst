.. highlight:: shell

============
Installation
============

Mountain Lion CSS is a wrapper around FEniCS, and inherits the installation difficulty. 
Mountain Lion provides two methods to install:

1. Docker image with provided dependencies
2. Manual install

It's recommended to use the provided docker images as a base for your environments, and customize as required.
Unfortunately, docker does impose restrictions on how you can interact with your environment.
Therefore the manual install option is provided for users who provide their own distribution of FEniCS.

Docker Install
--------------

There are two evolving docker images provided with this project: ``latest`` and ``devel``.
The ``latest`` tag is provides a docker image with the latest tested version of FEniCS, and tracks the latest releases from PyPI and Gitlab releases.
The ``devel`` image tracks the development branch of the repository, and represents the nightly build of the platform.
The ``devel`` tag provides a repository for mtnlion in the users home folder, which provides the installed distribution as a development package.
This allows mtnlion source files to be modified without having to re-install the package after every change. 

For a basic setup, simply run one of these tags directly from the registry::

	$ docker run --rm -it registry.gitlab.com/macklenc/mtnlion:<tag>

This will launch a temporary container for developing in.
However, you'll probably want to use it for development.
In order to keep your changes (including your development code) between launches, you'll need to get a little fancier with the run command::

	$ docker run --rm -ti --network host --name mtnlion -v mtnlion_dev:/home/fenics registry.gitlab.com/macklenc/mtnlion:<tag>

This will create a docker volume called ``mtnlion_dev`` to save all of the data inside ``/home/fenics``, which is the default home folder.
Now when you leave and re-enter the container with the same command, you'll have the same files available to you as long as it's in the folder that you attached the volume to.

It is recommended, however, that you customize the image to add development tools.
An example is provided in the `Gitlab repo`_ in the dockerfiles folder (``mtnlion-development.dockerfile``)::

	FROM registry.gitlab.com/macklenc/mtnlion:devel as sde

	# Shell
	RUN sudo apt-get install -y zsh

	# Nice shell
	RUN wget -O .zshrc https://git.grml.org/f/grml-etc-core/etc/zsh/zshrc &&\
	    wget -O .zshrc.local  https://git.grml.org/f/grml-etc-core/etc/skel/.zshrc

	# Install gvim
	RUN sudo apt-get install -y vim-gtk3

	# Install sublime
	RUN wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add - &&\
	    sudo apt-get install -y apt-transport-https &&\
	    echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list &&\
	    sudo apt-get update &&\
	    sudo apt-get install -y sublime-text sublime-merge

	# Install pycharm
	RUN wget https://download.jetbrains.com/python/pycharm-community-2019.1.1.tar.gz -qO - | sudo tar xfz - -C /opt/ &&\
	    cd /usr/bin &&\
	    sudo ln -s /opt/pycharm-*/bin/pycharm.sh pycharm

As you can see, this adds some development tools that require a GUI. 
To display the GUI elements, you'll have to enable X11 forwarding.
The process is different on each host OS:

Linux
^^^^^
In Linux, you can use the following script::

	XSOCK=/tmp/.X11-unix
	XAUTH=/tmp/.docker.xauth
	xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
	chmod 644 $XAUTH
	docker run -ti --rm -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH -e DISPLAY=$DISPLAY -v mtnlion_dev:/home/mtnlion registry.gitlab.com/macklenc/mtnlion:<tag>

This script will securely enable X11 forwarding to your host.
Now you can run, for example, PyCharm.


MacOS
^^^^^
In MacOS, you'll need to install `XQuartz`_ to provide an X11 server.
Once XQuartz is installed, enable the option `Allow connections from network clients`_, then restart XQuartz.
Then you'll need to run the following script every time you launch your development container::

	xhost + 127.0.0.1
	docker run -e DISPLAY=host.docker.internal:0 -v mtnlion_dev:/home/mtnlion registry.gitlab.com/macklenc/mtnlion:<tag>

Now you should be able to run your graphical apps from inside the container.

.. _XQuartz: https://www.xquartz.org/
.. _Allow connections from network clients: https://blogs.oracle.com/oraclewebcentersuite/running-gui-applications-on-native-docker-containers-for-mac


Manual Install
--------------

You can FEnsCS by following the `FEniCS installation instructions`_.
Make sure that the FEniCS version is compatible with the version of mtnlion you are using by checking the setup.py requirements, or observing the changelog in the Gitlab `release`_ repository.

Stable release
^^^^^^^^^^^^^^

To install Mountian Lion CSS, run this command in your terminal:

.. code-block:: console

    $ pip install mtnlion

This is the preferred method to install mtnlion outside of docker images, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
^^^^^^^^^^^^

The sources for Mountian Lion CSS can be downloaded from the `Gitlab repo`_ or Gitlab `release`_ repository.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://gitlab.com/macklenc/mtnlion

Or download the `release`_:

.. code-block:: console

    $ curl  -OL https://gitlab.com/macklenc/mtnlion/-/releases/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Gitlab repo: https://gitlab.com/macklenc/mtnlion
.. _release: https://gitlab.com/macklenc/mtnlion/-/releases
.. _FEniCS installation instructions: https://fenicsproject.org/download/
