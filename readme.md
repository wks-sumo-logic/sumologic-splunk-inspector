Sumologic-Splunk-Inspector
==========================

Splunk-inspector unpacks and organizes a Splunk diagnostic file and publishes this to Sumo Logic.

The result is different Sumo Logic sources showing usage, configuration, content to help migration and planning.

Installing the Source
=====================

If you prefer to clone the archive and run from source then you'll need Python 3.6 or higher and the modules listed 
in the dependency section.  

The steps are as follows: 

    1. Download and install python 3.6 or higher from python.org. 
       Make sure to choose the "add python to the default "path" checkbox in the installer (may be in 
       advanced settings.)

    2. Download and install git for your platform if you don't already have it installed.
       It can be downloaded from https://git-scm.com/downloads
    
    3. Open a new shell/command prompt. It must be new since only a new shell will include the new python 
       path that was created in step 1. Cd to the folder where you want to install the project
    
    4. Execute the following command to install pipenv, which will manage all of the library dependencies 
       for us:

        pip3 install pipenv
    
        -or-
    
        sudo pip3 install pipenv 
 
    5. Clone this repo and change to the directory
    
    6. Change into the previous folder. Type the following to install all the package 
       dependencies (this may take a while as this will download all of the libraries that it uses):

    pipenv install
    
Configuring the Source
======================

As the script can be installed both locally or remotely, the client can choose to run the script
locally or remotely.

    1. if remotely, then configure SSH access for an admin or operations account
    
    2. if locally, then follow the confirmation steps and install any python modules required
    
Dependencies
============

See the contents of "pipfile"

Features and Usage
==================

* write up and examples coming soon

License
=======

Copyright 2019 Wayne Kirk Schmidt
https://www.linkedin.com/in/waynekirkschmidt

Licensed under the Apache 2.0 License (the "License");

You may not use this file except in compliance with the License.
You may obtain a copy of the License at

    license-name   APACHE 2.0
    license-url    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
=======

Feel free to e-mail me with issues to: 

*    wschmidt@sumologic.com

*    wayne.kirk.schmidt@gmail.com

I will provide "best effort" fixes and extend the scripts.
