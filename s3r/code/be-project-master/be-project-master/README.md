# Real Time Intrusion Detection System for IoT Networks using Random Forest

The project contains a full stack web app created with React front end and Django back end. It is an Intrusion Detection system which detects attacks in real time that occur within the IoT network in consideration.

## Steps to install and run the application:

1. Ensure you have python 3.6.9, node v12.6.0, npm 6.13.4.

2. Clone the repo and cd to s3r-be-proj-ids
> cd s3r-be-proj-ids

3. Create virtual environment for backend development
> virtualenv env

4. Activate the virtual environment
> source env/bin/activate

5. Install backend dependencies present in requirements.txt
> pip3 install -r requirements.txt

6. Install frontend dependencies present in package.json
> npm i

7. Build production folder of the front end
> npm run build

8. Setup data base with backend
> python3 manage.py migrate

9. Run backend + build server
> python3 manage.py runserver

10. To Simulate the node (if actual node is not used) (move to parent dir -> be-project and run the sim)
> python3 ../node_simulator.py

11. The shell script for tshark is in the home folder of s3r-be-proj-ids.
Before you run it, you'll have to replace s3rbeproj with your computer's password.
> cd home
> ./tshark_shell_script.sh
