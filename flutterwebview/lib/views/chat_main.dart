import 'dart:io';

import 'package:dialog_flowtter/dialog_flowtter.dart';
import 'package:flutter/material.dart';
import 'package:flutterwebview/views/chat_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ChatMain extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'KUsistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'KUsistant'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, this.title}) : super(key: key);

  final String? title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  late DialogFlowtter dialogFlowtter;
  final TextEditingController _controller = TextEditingController();
  String cookie = 'Not initialized';
  final Future<SharedPreferences> _prefs = SharedPreferences.getInstance();

  List<Map<String, dynamic>> messages = [];

  @override
  void initState() {
    super.initState();
    _prefs.then((prefs) async {
      var sessionID = prefs.getInt('userID');
      dialogFlowtter =  DialogFlowtter.fromJson({
        "type": "service_account",
        "project_id": "kusistant-mwit",
        "private_key_id": "7e33af6badc9efd94b7a380c31fb42807c72843d",
        "private_key":
            "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3xGvGbc7lUd8k\n4p4pIQNYkwjWGb5n4aeejb9cc/flJydvx+S/VJRBt+cqD468RByKsI60j7MjJoLx\n+EVXaMO2c/FNbE5zUeFZGg+R2lKHjOvws78NphJWM+bpQPpGNbL7lXZFznE3zqTI\n+beQichbkre7JdaiRUK/B/zMxElFMZola5BpyQmgYRD36RVKRv5eiAeIs9zS9mgo\nLl7CU6XAmIOMSEFmu4eJSpLZs7BxbtVLTbBA1uMxer0wMx1WR8WEEP60BXE+RX0J\nMWBuqilVoD8XA5XNQGDkBipLu8Hs+UYXpdkPWVZdW1pd+ppXjngoiWJlZ0TygR3w\nMPclmfGPAgMBAAECggEAEJtZDAEPYezgqAIsvdXEaiQ7d7Gy4ctkLPFtWisGu3gq\n2bCsTNgVX80BQG1QflX/aE8lTk7wJtyLl9dSWOBYU2wt4cvIWSaMoVM4FfuvWp2T\nEtkDinW4EX82Pl0HYQHoT1EF87AAzkTH4nuiqZax+wiKvwhf2aE9s2rC3zRb1LtL\nsIQhQz8g0J3wgOijLSsSagRsXPukj6NoZSgmCCb7ybTZn8R7eNX7wW1xKvnaA/s4\nUyHxIZ/pJsiZ9h0SyFgM2AOhvdP9S9M9Q8CMRSBWbUgQuxlzhfBW3LlQ4cSyGiAh\nOLUvF04w9mXOo0b2AWdb9jMHmBycPrOHqPdOBec42QKBgQD6o6h9z/8CT2kr21YY\nV39kSobYq8MUZTTphORKX9bP78Nf63xetud3c3iINwQRSiOTXH3VmLQTr6Naa8K/\nPjx5sbYyCjrhQjwTmORmPP4vSf5poe3u2Tad8dmoB4MSyUKaRrQ23yxOwpK756TW\nuNpdzLdnP1aD1yxBttgoEnN4aQKBgQC7sp0yDWCktaDbMrMDnQg9xG83qdOluoDO\nme3k6SIAH/MwF+t+hVGKgJPhQEiS3Prjmcbfn/FqAasXWiAlfo818nNGfp8CBSJT\nwv+J7mMu/au7V6P3E1bGgmLnJmSQJ6ibqDVarEM8W1xnWMPNgLCK74U47sWXnnFO\n6/Q/FVgbNwKBgFwhMFweyqP0wLoIQ9tqvj8FTg/zAyBKG2sDGE9mbzW78lsd2neO\nUAMOhO29G1enovAV/YM4QGlEFI22Mr3NiLlK46f9LquCh0bE2p/iJ6UGU+hMR4OW\ngIcKUXF8YWfUZxECkFfjLQw+ZWWAvozXIh18lKX1GD4aKAB3z3jbX2qRAoGAco3a\nfrfHaf8oA1/3/ZaTdw8ySaiucZFYF7++f10B0U2uoIWYxokbcQp0Np+DK48O2GX8\nCHOXZXlLMF9jCz8orGYikL2q0hLMFo8GYupJQl6ztw0QFzWIWnMtZaH68jgiIY4R\nshs8ldO0m6aDKiMGnGT+y/Z+RcD/qok7clzWfxUCgYAYXuN4JO7iDaZPXUPIAcsg\nV3vLyV+fPezA9HpSRgQ0yBYXEweNSAWFgwaz8e5hY1DEUJStk0oT4GP9mJIJb3c7\nJpNTxNEPGKQ1i3QfeDrQ0u06r3k8XPR2m+ufaAcAXa8wE3qivZc4ZBm7YV7gnjoP\n7dRL+aIV2K9Ubb+WpVOFlg==\n-----END PRIVATE KEY-----\n",
        "client_email":
            "service-account@kusistant-mwit.iam.gserviceaccount.com",
        "client_id": "103908028969573835041",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url":
            "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url":
            "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40kusistant-mwit.iam.gserviceaccount.com"
      }, sessionId: '$sessionID');
      print('init');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title ?? 'KUsistant'),
      ),
      body: Column(
        children: [
          Expanded(child: ChatBody(messages: messages)),
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 10,
              vertical: 5,
            ),
            color: Colors.blue,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                  ),
                ),
                IconButton(
                  color: Colors.white,
                  icon: const Icon(Icons.send),
                  onPressed: () {
                    sendMessage(_controller.text);
                    _controller.clear();
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void sendMessage(String text) async {
    if (text.isEmpty) return;
    setState(() {
      var map = Map.fromEntries((<String, String>{'cookie': cookie}).entries);
      print(map);
      addMessage(
        Message(
          text: DialogText(text: [text]),
        ),
        true,
      );
    });

    DetectIntentResponse response = await dialogFlowtter.detectIntent(
      queryInput: QueryInput(text: TextInput(text: text)),
    );

    if (response.message == null) return;
    setState(() {
      addMessage(response.message!);
    });
  }

  void addMessage(Message message, [bool isUserMessage = false]) {
    messages.add({
      'message': message,
      'isUserMessage': isUserMessage,
    });
  }

  @override
  void dispose() {
    dialogFlowtter.dispose();
    super.dispose();
  }
}
