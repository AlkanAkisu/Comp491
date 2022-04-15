import 'package:flutter/material.dart';
import 'package:flutterwebview/views/home_page.dart';
import 'dart:ui' as ui;
import 'dart:html';


void main() {
  // ignore: undefined_prefixed_name
  ui.platformViewRegistry.registerViewFactory(
      'hello-world-html',
          (int viewId) => IFrameElement()
        ..width = '640'
        ..height = '360'
        ..src = 'https://ku.blackboard.com/'
        ..style.border = 'none');
  runApp(const MyApp());
  // runApp(Directionality(
  //   textDirection: TextDirection.ltr,
  //   child: SizedBox(
  //     width: 640,
  //     height: 360,
  //     child: HtmlElementView(viewType: 'hello-world-html'),),));
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