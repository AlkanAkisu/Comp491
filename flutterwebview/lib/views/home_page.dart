// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'dart:convert' as convert;
import 'dart:io';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:requests/requests.dart';
import 'package:http/http.dart' as http;
import 'package:mongo_dart/mongo_dart.dart' as mongo;

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final cookies = <Cookie>[];
  CookieManager cookieManager = CookieManager.instance();

  String bbCookie = '';
  String kusisCookie = '';

  InAppWebViewController? webViewController;

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
              child: Text(
                'BlackBoard Login Screen',
                style: TextStyle(fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
            ),
            SizedBox(
              height: 20,
            ),
            Expanded(
              child: InAppWebView(
                initialUrlRequest: URLRequest(
                  url: Uri.parse("https://ku.blackboard.com/"),
                ),
                onWebViewCreated: (controller) {
                  webViewController = controller;
                },
              ),
            ),
            TextButton(
              onPressed: () async {
                bbCookie = await GetBBCookies();
                print(bbCookie);
                var db = await mongo.Db.create("mongodb+srv://kusistant:SXBmDmSTogE89uXW@cluster0.bkabe.mongodb.net/userDB");
                await db.open();
                var usersCollection = db.collection('users');
                await usersCollection.insertOne({'id': '1', 'bbCookie': bbCookie, 'kusisCookie': kusisCookie});

                // await webViewController?.loadUrl(
                //     urlRequest:
                //         URLRequest(url: Uri.parse("https://kusis.ku.edu.tr")));
              },
              child: Text('Get BB data'),
            ),
            TextButton(
              onPressed: () async {
                kusisCookie = await GetKusisCookies();
                print(kusisCookie);
                var db = await mongo.Db.create("mongodb+srv://kusistant:SXBmDmSTogE89uXW@cluster0.bkabe.mongodb.net/userDB");
                await db.open();
                var usersCollection = db.collection('users');
                await usersCollection.updateOne(mongo.where.eq('id', '1'),mongo.modify.set('kusisCookie', kusisCookie));
              },
              child: Text('Get Kusis data'),
            ),
            TextButton(
              onPressed: () async {
                await ClearCookies();
              },
              child: Text('Clear Cookies'),
            ),
          ],
        ),
      ),
    );
  }

  Future<String> GetBBCookies() async {
    var cookies = await cookieManager.getCookies(
      url: Uri.parse("https://ku.blackboard.com/"),
    );
    var cookieStr = '';
    cookieStr = cookies.fold(
        cookieStr, (prev, elem) => prev += '${elem.name}=${elem.value}; ');
    return cookieStr;
  }

  Future<String> GetKusisCookies() async {
    var cookies = await cookieManager.getCookies(
      url: Uri.parse("https://kusis.ku.edu.tr"),
    );

    var cookieStr = '';
    cookieStr = cookies.fold(
        cookieStr, (prev, elem) => prev += '${elem.name}=${elem.value}; ');
    return cookieStr;
  }

  Future<void> ClearCookies() async {
    await cookieManager.deleteAllCookies();
  }
}
