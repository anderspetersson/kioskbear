import 'dart:convert';

import 'package:http/http.dart' as http;

import 'flow_models.dart';

class BlockService {
  Future<List<Block>> getAll() async {
    final url = Uri.parse(
      'http://localhost:8000/api/v1/blocks/',
    );
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Token 68a7d4ce867d4608b031082fcdb7d4d967a31fd1',
      },
    );
    if (response.statusCode == 200) {
      final json = jsonDecode(response.body) as List;
      final blocks = json.map((data) {
        return Block.fromJson(data);
      }).toList();
      return blocks;
    } else {
      return [];
    }
  }

  Future<List<Option>> getAllOptions() async {
    final url = Uri.parse(
      'http://localhost:8000/api/v1/options/',
    );
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Token 68a7d4ce867d4608b031082fcdb7d4d967a31fd1',
      },
    );
    if (response.statusCode == 200) {
      final json = jsonDecode(response.body) as List;
      final options = json.map((data) {
        return Option.fromJson(data);
      }).toList();
      return options;
    } else {
      return [];
    }
  }

  Future<List<ScoredOption>> getAllScoredOptions() async {
    final url = Uri.parse(
      'http://localhost:8000/api/v1/scored-options/',
    );
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Token 68a7d4ce867d4608b031082fcdb7d4d967a31fd1',
      },
    );
    if (response.statusCode == 200) {
      final json = jsonDecode(response.body) as List;
      final scoredoptions = json.map((data) {
        return ScoredOption.fromJson(data);
      }).toList();
      return scoredoptions;
    } else {
      return [];
    }
  }
}

class FlowService {
  Future<ContentFlow> getFlow() async {
    final url = Uri.parse(
      'http://localhost:8000/api/v1/flows/1/',
    );
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Token 68a7d4ce867d4608b031082fcdb7d4d967a31fd1',
      },
    );
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = await json.decode(response.body);
      return ContentFlow.fromJson(data);
    } else {
      throw 'Could not load flow';
    }
  }
}
