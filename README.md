# KUsistant

KUsistant is our computer engineering design project. 
It is a personal student assistant. 
It aims to help students meet their academic and personal needs. 
With KUsistant you can easily learn your GPA or weather of Koç without having to navigate around different websites. 
To retrieve this information KUsistant understands its users' inputs and communicates with various APIs to get the necessary information. 
KUsistant also has the future of small talk, so you can talk with KUsistant and it also can tell you some very bad dad jokes.

It consists of 2 screens which are login and chat.

Login Screen:
- In this screen, the user is prompted to log in to their Blackboard and KUSIS accounts. Once they are logged into their accounts, their cookies will be retrieved
and saved in the MongoDB database with their specific userID for their requests on the chat screen.
<img width="378" alt="Screen Shot 2022-05-19 at 19 03 18" src="https://user-images.githubusercontent.com/31079280/169346270-4c4ffc29-14d7-45d4-95e8-125993b8e16c.png">


Chat Screen:
- On this screen, a Dialogflow integrated chat screen allows the user to chat with our personal assistant. It recognizes intents and entities with the help
of NLP. It responds to the user according to their requests.
<img width="379" alt="Screen Shot 2022-05-19 at 19 04 09" src="https://user-images.githubusercontent.com/31079280/169346333-d7bff9ef-85af-417e-b8e6-3c1ee47c804b.png">

How to setup :gear::

1. Clone git repository using ``` git clone https://github.com/AlkanAkisu/Comp491.git ```

2. Run the following commands to run bridge API on ngrok server:
``` cd Comp491 ``` ``` python3 DialogFlow_Bridge_API.py ``` ``` ngrok http 5001 ```

3. Change the fulfillment webhook URL on Dialogflow with newly generated https ngrok url like ```https://xxxx-xx-xxx-xx-xx.ngrok.io/webhook```

4. Run main API in repl.it server in https://replit.com/@ALKANAKISU/Comp491#.replit
To run use the following commands in the repl.it shell:
``` cd Scrape\ API/ ``` ``` python3 main.py ```

5. Lastly, run the flutter application:
``` cd flutterwebview ``` ``` flutter pub get ``` ``` flutter run ```

