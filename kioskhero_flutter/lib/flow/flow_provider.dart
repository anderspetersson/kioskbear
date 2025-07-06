import 'dart:async';

import 'package:flutter/cupertino.dart';

import 'flow_models.dart';
import 'flow_services.dart';

class BlockProvider extends ChangeNotifier {
  final _service = BlockService();
  List<Block> _blocks = [];
  List<ScoredOption> _scored_options = [];
  List<Option> _options = [];

  List<Block> get blocks => _blocks;
  List<ScoredOption> get scoredoptions => _scored_options;
  List<Option> get options => _options;
  bool isLoadingBlocks = false;
  bool isLoadingOptions = false;

  Future<void> getAllBlocks() async {
    isLoadingBlocks = true;
    notifyListeners();
    final response = await _service.getAll();
    _blocks = response;
    isLoadingBlocks = false;
    notifyListeners();
  }

  Future<void> getAllOptions() async {
    isLoadingOptions = true;
    notifyListeners();
    final response = await _service.getAllOptions();
    _options = response;
    isLoadingOptions = false;
    notifyListeners();
  }

  Future<void> getAllScoredOptions() async {
    isLoadingOptions = true;
    notifyListeners();
    final response = await _service.getAllScoredOptions();
    _scored_options = response;
    isLoadingOptions = false;
    notifyListeners();
  }

  getBlockFromId(int id) {
    return _blocks.firstWhere((b) => b.id == id);
  }

  getOptionFromId(int id) {
    return _options.firstWhere((o) => o.id == id);
  }

  getScoredOptionFromId(int id) {
    return _scored_options.firstWhere((so) => so.id == id);
  }
}

class FlowProvider extends ChangeNotifier {
  final _service = FlowService();
  ContentFlow? flow;
  bool isLoading = false;
  int timeout = 30;

  Future<void> getMyFlow() async {
    isLoading = true;
    debugPrint('loading flow');
    notifyListeners();
    final response = await _service.getFlow();
    flow = response;
    isLoading = false;
    notifyListeners();
  }

  void resetTimer() {
    timeout = 30;
    notifyListeners();
  }

  void tickTimer() {
    timeout--;
    notifyListeners();
  }
}
