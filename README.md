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
2. Interactive Game - 7 Up 7 Down (Gambling): Students can enjoy the thrill of gambling without risking real money by playing our interactive game, 7 Up 7 Down. This addictive game offers an engaging experience while adhering to responsible gaming principles.
3. User Authentication and Forgotten Password Functionality: Our website ensures secure access with robust user authentication mechanisms. Additionally, we've implemented a forgotten password feature that allows users to reset their passwords conveniently. Leveraging Django's email capabilities, users receive automated email notifications and instructions for resetting their passwords, enhancing the overall security and user experience of our platform.
4. Attendance Code Points and Leaderboard: Earn points by participating in events and submitting attendance codes! Our platform maintains a dynamic leaderboard, showcasing the top attendees based on accumulated points. This gamified system encourages active engagement within the IIITB community, fostering healthy competition and rewarding students for their involvement in campus activities. Keep track of your progress and climb the leaderboard to earn recognition for your dedication and participation!

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

