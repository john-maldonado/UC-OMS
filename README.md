# UC-OMS
Ultimate Controls Order Management System

## Background
This application is a time entry system I made for my company Ultimate Controls, a provider of software development and industrial automation services.

Origninally created as a "lets see if I can do it project" this was used in production for 2 years before switching to Quickbooks. 

Created early in my software egineering career this program demonstrates: 
<li>A GUI made with Qt and the Pyside2 library,
<li>A custom protocol implemented directly on TCP sockets delievering JSON payloads (this is before I knew about REST)</li>
<li>User Authentication using username and password, and a token mechanism

This repo consists of Front End and Backend applications.
The Backend application runs in a container on a remote server hosting a MySQL database, and creates an interface to the database.
The Frontend application runs on a client PC which provides the GUI and communicates to the Backend using the custom TCP protocol.
