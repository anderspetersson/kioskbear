// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'flow_models.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

ContentFlow _$ContentFlowFromJson(Map<String, dynamic> json) => ContentFlow(
      id: json['id'] as int,
      blockList:
          (json['block_set'] as List<dynamic>).map((e) => e as int).toList(),
      startBlock: Block.fromJson(json['start_block'] as Map<String, dynamic>),
      endBlock: Block.fromJson(json['end_block'] as Map<String, dynamic>),
    );

Map<String, dynamic> _$ContentFlowToJson(ContentFlow instance) =>
    <String, dynamic>{
      'id': instance.id,
      'start_block': instance.startBlock,
      'end_block': instance.endBlock,
      'block_set': instance.blockList,
    };

Block _$BlockFromJson(Map<String, dynamic> json) => Block(
      id: json['id'] as int,
      title: json['title'] as String,
      options:
          (json['options'] as List<dynamic>?)?.map((e) => e as int).toList(),
      scoredOptions: (json['scored_options'] as List<dynamic>?)
          ?.map((e) => e as int)
          .toList(),
    );

Map<String, dynamic> _$BlockToJson(Block instance) => <String, dynamic>{
      'id': instance.id,
      'title': instance.title,
      'options': instance.options,
      'scored_options': instance.scoredOptions,
    };

Option _$OptionFromJson(Map<String, dynamic> json) => Option(
      id: json['id'] as int,
      text: json['text'] as String,
      follow_up_block_id: json['follow_up_block_id'] as int?,
    );

Map<String, dynamic> _$OptionToJson(Option instance) => <String, dynamic>{
      'id': instance.id,
      'text': instance.text,
      'follow_up_block_id': instance.follow_up_block_id,
    };

ScoredOption _$ScoredOptionFromJson(Map<String, dynamic> json) => ScoredOption(
      id: json['id'] as int,
      text: json['text'] as String,
      score: json['score'] as int,
      follow_up_block_id: json['follow_up_block_id'] as int?,
    );

Map<String, dynamic> _$ScoredOptionToJson(ScoredOption instance) =>
    <String, dynamic>{
      'id': instance.id,
      'text': instance.text,
      'score': instance.score,
      'follow_up_block_id': instance.follow_up_block_id,
    };
