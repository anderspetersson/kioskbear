import 'package:json_annotation/json_annotation.dart';

part 'flow_models.g.dart';

// UPDATE JSON MODELS WITH dart run build_runner build

@JsonSerializable()
class ContentFlow {
  final int id;

  @JsonKey(name: 'start_block')
  final Block startBlock;

  @JsonKey(name: 'end_block')
  final Block endBlock;

  @JsonKey(name: 'block_set')
  final List<int> blockList;

  ContentFlow(
      {required this.id,
      required this.blockList,
      required this.startBlock,
      required this.endBlock});

  factory ContentFlow.fromJson(Map<String, dynamic> json) =>
      _$ContentFlowFromJson(json);
}

@JsonSerializable()
class Block {
  final int id;
  final String title;
  final List<int>? options;

  @JsonKey(name: 'scored_options')
  final List<int>? scoredOptions;

  Block(
      {required this.id,
      required this.title,
      this.options,
      this.scoredOptions});

  factory Block.fromJson(Map<String, dynamic> json) => _$BlockFromJson(json);
}

@JsonSerializable()
class Option {
  final int id;
  final String text;
  final int? follow_up_block_id;
  Option({
    required this.id,
    required this.text,
    this.follow_up_block_id,
  });

  factory Option.fromJson(Map<String, dynamic> json) => _$OptionFromJson(json);
}

@JsonSerializable()
class ScoredOption {
  final int id;
  final String text;
  final int score;
  final int? follow_up_block_id;

  ScoredOption(
      {required this.id,
      required this.text,
      required this.score,
      this.follow_up_block_id}) {}

  factory ScoredOption.fromJson(Map<String, dynamic> json) =>
      _$ScoredOptionFromJson(json);
}
