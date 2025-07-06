import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'flow/flow_models.dart';
import 'screens/login.dart';

class ScreenProvider extends ChangeNotifier {
  late List<Block> blocks;
  Widget activeScreen = LoginScreen();
  bool feedbackEnabled = true;
  Map<String, dynamic> _map = {};
  bool _error = false;
  Map<String, dynamic> get map => _map;

  Future<void> get fetchBlocks async {
    final response = await http.get(
      Uri.parse('http://localhost:8000/api/v1/blocks/'),
    );

    if (response.statusCode == 200) {
      try {
        _map = jsonDecode(response.body);
        _error = false;
      } catch (e) {
        _error = true;
        _map = {};
      }
    } else {
      _error = true;
      _map = {};
    }
    notifyListeners();
  }

  void setFeedbackEnabled() {
    feedbackEnabled = true;
    notifyListeners();
  }

  void setFeedbackDisabled() {
    feedbackEnabled = false;
    notifyListeners();
  }

  void updateActiveScreen(Widget widget) {
    activeScreen = widget;
    notifyListeners();
  }
}
