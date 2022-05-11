import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:flutterwebview/views/chat_main.dart';
import 'package:flutterwebview/views/chat_page.dart';
import 'package:flutterwebview/views/home_page.dart';
// import 'dart:ui' as ui;
// ignore: avoid_web_libraries_in_flutter
// import 'dart:html';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {

    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'KUsistant',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}
