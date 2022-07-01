# codingwithwally
A coding site akin to CodingBat specifically for Harvey Mudd's introductory CS course

## About
[Link to Coding with Wally](http://codingwithwally-hmccsstudio.pythonanywhere.com/login) (note: requires HMC email. If you'd like to see the site, use username: wart@hmc.edu, password: 12345678)
A HMC-themed (hence the gold and black) coding site designed for beginner coders to practice their Python skills. 

A notable feature is that each coding problem is accompanied by several modes. The default is the one that most expect; students type in code into a embedded code editor and check it against test cases. However, this inflexibility can sometimes be detrimental to truly understanding what one is supposed to solve. Thus, we have added three more modes in order to remedy this:

* Test inputs: You are given a test case, and then asked to predict what the output would be
* Test outputs: You are given the outputs of a test case, and then asked what possible inputs could be
* Test bugs: You are given buggy code; read over the code and fix the bugs

The hope is that by having these three extra modes, students will not just jump straight into coding but slow down and truly investigate the problem. 

## Features
### Users
* View coding problems
* Filter coding problems by tags (language, difficulty, etc)
* Write code for problems and check against test cases
* Test inputs, outputs, and bugs as described above
### Admins
* Submit coding problems

## Technologies
* Flask, a Python framework for webapps 
  * Significant work with JSON to communicate between Javascript and Python
* SQLAlchemy for database
* WTForms for form validation


