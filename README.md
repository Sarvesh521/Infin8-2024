# Infin8-2024


## About
Welcome to our collaborative project between the Student Activities Council (SAC) and the 8Bit (Magazine Club of IIITB)!<p>
Our innovative website serves as a tool to streamline attendance tracking for student events while fostering a sense of engagement and excitement within the IIITB community. Through the website we hope to enhance overall experience for both organizers and attendees.

## TechStack
1. **Django**
2. **SQL**
3. **Python**
4. **JavaScript**
5. **HTML**
6. **CSS**
7. **Docker**
8. **AWS Deployment**


## Description
This project contains a Django application that handles user authentication. It includes a login page where users can enter their email and password to access the system. You can enter passcodes to gain sand (points) and time. The website uses sql database to identify which codes are sand and which are time and increase the timer/points accordingly. The database also ensures that one won't gain points for entering the same code more than once. Finally you can also see a leaderboard once you login. 

The website was used by around 25% students to enter codes.

## Features
1. Attendance Tracking : Our website simplifies the process of monitoring attendance allowing organizers to focus on creating memorable experiences and allowing SAC to make informed decisions for future events.

## Installation
1. Clone the repository: `git clone https://github.com/Sarvesh521/Sands-Of-Time.git`
2. Navigate into the project directory: `cd Infin8`
3. Install the required packages: `pip install -r requirements.txt`
4. Make necessary migrations: <br>`python manage.py make migrations`<br> `python manage.py migrate` 
5. Run the server: `python manage.py runserver`

## Usage
Open your web browser and navigate to `localhost:8000` to access the login page.

## Deployment
Go to `https://infin8loyalty.iiitb.net/` to checkout the site!! <br> Edit : The site is currently down.

