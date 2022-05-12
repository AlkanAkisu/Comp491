// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables
import 'dart:convert' as convert;
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
// import 'package:webview_cookie_manager/webview_cookie_manager.dart';
// import 'package:webview_flutter/webview_flutter.dart';
// import 'package:http/http.dart' as http;
import 'package:flutter_inappwebview/flutter_inappwebview.dart';
import 'package:flutterwebview/views/chat_main.dart';
import 'package:flutterwebview/views/chat_page.dart';
import 'package:requests/requests.dart';
import 'package:http/http.dart' as http;
import 'package:mongo_dart/mongo_dart.dart' as mongo;
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final Future<SharedPreferences> _prefs = SharedPreferences.getInstance();

  final cookies = <Cookie>[];
  CookieManager cookieManager = CookieManager.instance();
  String bbCookie = '';
  String kusisCookie = '';
  String mongoName =
      'mongodb+srv://kusistantt:Av8zzmtP3uiCbj3p@cluster0.bkabe.mongodb.net/userDB';

  InAppWebViewController? webViewController;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _prefs.then((SharedPreferences prefs) async {
      var userID = prefs.getInt('userID');
      if (userID == null) {
        var id = Random().nextInt(9000) + 1000;
        await prefs.setInt("userID", id);
        userID = id;
      }
      print('The user id is $userID');
      return userID;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.amber,
      appBar: AppBar(
        title: Text('KUsistant'),
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
                var db = await mongo.Db.create(mongoName);
                await db.open();
                var usersCollection = db.collection('users');
                var id = (await _prefs).getInt('userID');
                await usersCollection.insertOne({
                  'id': id,
                  'bbCookie': bbCookie,
                  'kusisCookie': kusisCookie
                });
              },
              child: Text('Get BB data'),
            ),
            TextButton(
              onPressed: () async {
                kusisCookie = await GetKusisCookies();
                print(kusisCookie);
                var db = await mongo.Db.create(mongoName);
                await db.open();
                var usersCollection = db.collection('users');
                var id = (await _prefs).getInt('userID');
                await usersCollection.updateOne(mongo.where.eq('id', id),
                    mongo.modify.set('kusisCookie', kusisCookie));
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ChatMain()),
                );
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
    await webViewController?.loadUrl(
        urlRequest: URLRequest(url: Uri.parse("https://kusis.ku.edu.tr")));
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
