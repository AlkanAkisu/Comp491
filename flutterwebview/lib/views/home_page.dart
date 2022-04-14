// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'dart:convert' as convert;
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:webview_cookie_manager/webview_cookie_manager.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final cookieManager = WebviewCookieManager();
  final cookies = <Cookie>[];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.amber,
      appBar: AppBar(
        title: Text('WebView Test Screen'),
        ),
      body: Container(
      child: Column(
        children: [
          SizedBox(
            height: 20,
            ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text('BlackBoard Login Screen', 
            style: TextStyle(fontWeight: FontWeight.bold), 
            textAlign: TextAlign.center,
            ),
          ),
          SizedBox(
            height: 20,
            ),
            AspectRatio(
              aspectRatio: 1,
              child: WebView(
                initialUrl: 'https://ku.blackboard.com/',
                javascriptMode: JavascriptMode.unrestricted,
                onPageFinished: (_) async {
                var response = await http.post(
                  Uri.https('ku.blackboard.com','webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1')
                );
                var jsonResponse = response.headers;
                if(jsonResponse!=null)
                  print(jsonResponse);
                  
                },
              ),
              )
        ],
      ),
      ),
    );
  }
}