import 'package:flutter/material.dart';
import 'package:flutterwebview/views/home_page.dart';
// import 'dart:ui' as ui;
// ignore: avoid_web_libraries_in_flutter
// import 'dart:html';

void main() {
  // ignore: undefined_prefixed_name
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}
