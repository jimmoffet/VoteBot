# VoteBot
VoteBot is an extensible SMS chatbot for civic engagement

<a href="#"><img src="https://jamesdavidmoffet.com/images/opendatabeta/votebot.png" /></a>

## OpenDataBeta
As a civic tech fellow, with funding from the Harvard Graduate School of Design Community Service Fellowship, I developed a suite of software tools for strengthening municipal civic engagement in collaboration with City Councillor Nadeem Mazen and his design firm, Nimblebot. We did intensive user research with civil society organizations and ultimately created tools that allow them to easily pull data from government websites and deliver it to their constituencies via inexpensive, low-touch, high-engagement channels, such as SMS, with almost no technical volunteer labor.

Note: VoteBot requires an account at https://www.twilio.com. The cost as of the deployment of this project was $1/month and $0.0075/SMS. 

Note: You may want to delete the clientsecret.json file that controls access to your google sheet if you plan to publish a copy of this repository. Making that file public is equivalent to the sharing option: "Anyone with a link can edit."

VoteBot was designed to be easily adapted and deployed for free on heroku.

# Install and run project
    
    git clone https://github.com/jimmoffet/VoteBot.git
    cd VoteBot
    pip install -r requirements.txt
    python app.py # run on 127.0.0.1:5000

Check out the open campaign finance data viz: https://opendatabeta.herokuapp.com
