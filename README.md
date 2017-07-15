# SCTF
Security Capture the Flag Platform is the best platform for CTF Challenges. You will be able to define Teams, Challenges and access to relative statistics. SCTF is lightweight and fast django application that is able to support large competition. 

We would love to see how you use this awesome Platform. You can notify us about your site, app or service by mail. 

# Install & Start
<b>1. [OPTIONAL] Virtual Environment (Strongly Suggested)</b>: 
	
	$ pyvenv-3.5 venv
	$ source venv/bin/activate

<b>2. Install Requirements</b>:

	$ pip install -r requirements.txt

<b>3. [OPTIONAL] Install Demo Data</b>:
	
	$ chmod +x loaddata.sh
	$ ./loaddata.sh

<b>4. Start Application</b>:
	
	$ python manage.py runserver 0.0.0.0:<[port]>
	
<b>5. Reset Application</b>:
	
	$ chmod +x reset.sh
	$ ./reset.sh
	
# Features

* Arbitrary categories and challenges.
* Scoreboard.
* Challenge hints.
* Team progress page.
* Challenge overview page.
* and more ...

# Live Demo
Insert Description

<img src="https://raw.github.com/SynAckPwn23/SCTF/master/Uploads_For_Demo/img/All_Teams.PNG" width="100%"/>

<img src="https://raw.github.com/SynAckPwn23/SCTF/master/Uploads_For_Demo/img/Challenge.PNG" width="100%"/>

<img src="https://raw.github.com/SynAckPwn23/SCTF/master/Uploads_For_Demo/img/Rank.PNG" width="100%"/>

# License Information
<b>SCTF is licensed under the GNU General Public License v3.0 - Copyright (c) [2017] [Daniele Votta, Filippo Schiavio]</b>

Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

<b>Permissions</b>: Commercial use, Modification, Distribution, Patent use, Private use.

<b>Conditions</b>: License and copyright notice, State changes, Disclose source, Same License.

<b>Limitations</b>: Liability, Warranty.

Project is developed and maintained by Daniele Votta and Filippo Schiavio.
Template is based on Colorlib and Aigars Silkalns work: https://github.com/puikinsh/gentelella
