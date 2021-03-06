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
        primarySwatch: Colors.red,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'KUsistant'),
      debugShowCheckedModeBanner: false,
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
      print('init1');
      dialogFlowtter = DialogFlowtter.fromJson({
        "type": "service_account",
        "project_id": "kusistant-mwit",
        "private_key_id": "1cd0f67f06f522937a8d89e2f56adc1d779d6867",
        "private_key":
            "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCm0kxIWxQZLKtV\nFpMRdvGzhfM1AhqhEQRpR1CTTva20giq4aSCBu0JBFcTkjS3VLeMnsyK7GUbZK3N\ncDDHBbEeaohk9Hbyt7Tj8K6Jc+4dybgHW7W8o1wjaD3lkbRVkLxm5cwA5zUZnhFU\npZADUU51FeBYBiP9Dyt5hxiU2zYljd0gg+U6W9HLMhyLPOjta5MqD1KHYfvXqTDP\nQ8tCTW8R2SRcIlQp0cvc0mb1XagLc4fmCdqyn06hBdqnmFtiBdIuHaJLJUpDAaV4\nV4bE1fVe36g/Zv99CSaHdRtmUk8K9dpvAynxzpj6lt9qzP6IziHterfgz05kpJha\ns3unOgrZAgMBAAECggEAAZT99zOx6Zk0WL65j1FW8nJjP43xDbT5Gzx7ZaI6kbpF\nLcWtBzSkm9DIOJ3K1TA++1zoKKscPFnEki2tsL17lAPDnl15IU0fsIewSApq6Cpp\nDdzPSOYtsgJDkAFFOgiA2OL1/84xgTgwBuL5Dib/vPmDoqIQRk6WBXWEBKldhpah\nYZ3dibtxe9nOkFVlQSWMgpExlnJ9iGtLyx/SMW1+uh4F70p/YTnu7b8I78j6W+GZ\nyJXyq5RGfMn9nwhbWSKydqupQbQikPXNPjN9HuuCCXjSQjQSf2TRY2Yr+JBgAfH8\n8rSdS5G6d3wnPxNATNXONjFHkgUprIH99Gqyl0W32QKBgQDjnCBpDNGpVDOPau4S\nVT9y7FflYR04dZ2A7QAMFP7pEu6RbipPE42TdzwWAPvW9UTjpRsIRiAEFtLaIOQo\n7EEoE8EK0wswc4sCulrQ1qm+0kG91iF5HBpNW4hLrhQelqoEe+va+ZuizwWOqz8B\n4xERCIoD0PB0l23DRhFpYRi21QKBgQC7oR7WwdVysV2H62ULgc3w0vLiEqu/gdU6\nUTnvrfM47EcGi8HIpoLEKkmgUiBDp5oU1VR1HaO3qyknPF0gwE3+mS11VioN025Q\nXBBZfrLsnsySdX4US2JFnp3HYmx/0gG8iZ4AbPcDrNtdAucClaFy7czCWvKK2eo7\nrtRSIcFN9QKBgQCxOFsz8Ds/MMSEoqmDtMSWYtd9TkRGNa3ROLeUsLRaHdeLfM+M\nipjtfSVXrKRqFsbwyRlnM9Kx3GOIW5vLEUkaP2dLWk+YBh7ynM8hVEMOxP9TJGsj\ntXH1UZOp+XzI5F605xgZg8he1/pnv4ZrnbUoIhH0LrdK0K0yIlhkSKnJkQKBgHYj\nyBgu6igSV7MKW5A4RiSZnocMfInTxR+4H0O0Ao5X74zGmNivR20et0c0Ds6qjFEL\n1eb8J6axJfNnhbfmffWOG1pjS41zEGWW4lCHfz+P6X1ab2113cW6TtxJM8nzwFYn\nTI42Df6Ja4IQHsa40nRcGO5Td55IAb1coqGoUV+1AoGAMex4CS1J+HEaKpFa/FzB\n94vqvWbqK4b3l6xNab0QW/Y5hrJcnlVh2M3fbXfIz1Exr76sCyDVR5FmXX8MIKPz\n7HEy3l5x6abKjIHIU/J7dk83xiB/iPVc+kWzYFtrEtzLSE+iZirb6aRPHs8OhUB3\nOTNhvZ5bEMuH1UD1d7AQRW8=\n-----END PRIVATE KEY-----\n",
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
      print('init2');
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
            color: Color.fromRGBO(71, 79, 82, 1),
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
