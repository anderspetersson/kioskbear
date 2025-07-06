import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:kioskhero/flow/flow_provider.dart';
import 'package:provider/provider.dart';

import '../flow/flow_models.dart';
import '../flow/flow_screens.dart';
import '../providers.dart';
import '../utils/utf8.dart';

class EmojiButton extends StatefulWidget {
  final String emoji;
  final int ratingValue;
  int? follow_up_block_id;
  EmojiButton({Key? key, required this.emoji, required this.ratingValue, this.follow_up_block_id})
      : super(key: key);

  @override
  State<EmojiButton> createState() => _EmojiButtonState();
}

class _EmojiButtonState extends State<EmojiButton> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      flex: 1,
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: FittedBox(
          child: CupertinoButton(
            pressedOpacity: 0.9,
            onPressed: () {
              const url = 'http://localhost:8000/api/v1/ratings/';
              http.post(
                Uri.parse(url),
                headers: {
                  'Authorization': 'Token 68a7d4ce867d4608b031082fcdb7d4d967a31fd1',
                },
                body: {
                  'flow': '1',
                  'score': widget.ratingValue.toString(),
                },
              );
              if (widget.follow_up_block_id != null) {
                Provider.of<ScreenProvider>(context, listen: false).updateActiveScreen(
                  BlockScreen(
                    block: Provider.of<BlockProvider>(context, listen: false)
                        .getBlockFromId(widget.follow_up_block_id!),
                  ),
                );
              } else {
                if (Provider.of<FlowProvider>(context).flow == null) {
                  debugPrint('loading flow while clicked on button.');
                } else {
                  Provider.of<ScreenProvider>(context).updateActiveScreen(
                    BlockScreen(
                        block: Provider.of<FlowProvider>(context, listen: false).flow!.endBlock),
                  );
                }
              }
            },
            child: Text(widget.emoji,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 32.0,
                )),
          ),
        ),
      ),
    );
  }
}

class EmojiRow extends StatefulWidget {
  final List<int> options;

  const EmojiRow({super.key, required this.options});

  @override
  State<EmojiRow> createState() => _EmojiRowState();
}

class _EmojiRowState extends State<EmojiRow> {
  late ScoredOption optionsobj;

  Widget get_emojiButtonFromOptionId(int optionId) {
    optionsobj = Provider.of<BlockProvider>(context, listen: false).getScoredOptionFromId(optionId);
    if (optionsobj.follow_up_block_id != null) {
      return EmojiButton(
        emoji: utf8convert(optionsobj.text),
        ratingValue: optionsobj.score,
        follow_up_block_id: optionsobj.follow_up_block_id,
      );
    } else {
      if (Provider.of<FlowProvider>(context, listen: false).flow == null) {
        return const Text('Loading flow...');
      }
      return EmojiButton(
        emoji: utf8convert(optionsobj.text),
        ratingValue: optionsobj.score,
        follow_up_block_id: Provider.of<FlowProvider>(context, listen: false).flow!.endBlock.id,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint('emojirow');
    return Container(
      width: MediaQuery.of(context).size.width,
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Center(
          child: Row(
            children: <Widget>[
              for (var option in widget.options) get_emojiButtonFromOptionId(option),
            ],
          ),
        ),
      ),
    );
  }
}

class ChoiceButton extends StatefulWidget {
  final String text;
  int? follow_up_block_id;
  ChoiceButton({Key? key, required this.text, this.follow_up_block_id}) : super(key: key);

  @override
  State<ChoiceButton> createState() => _ChoiceButtonState();
}

class _ChoiceButtonState extends State<ChoiceButton> {
  @override
  Widget build(BuildContext context) {
    return Flexible(
      fit: FlexFit.tight,
      child: Container(
        padding: EdgeInsets.all(8.0),
        child: CupertinoButton(
          color: Colors.white,
          padding: EdgeInsets.all(24.0),
          pressedOpacity: 0.9,
          onPressed: () {
            if (widget.follow_up_block_id != null) {
              Provider.of<FlowProvider>(context, listen: false).resetTimer();
              Provider.of<ScreenProvider>(context, listen: false).updateActiveScreen(
                BlockScreen(
                  block: Provider.of<BlockProvider>(context, listen: false)
                      .getBlockFromId(widget.follow_up_block_id!),
                ),
              );
            } else {
              if (Provider.of<FlowProvider>(context).flow == null) {
                debugPrint('loading flow while clicked on button.');
              } else {
                Provider.of<ScreenProvider>(context).updateActiveScreen(
                  BlockScreen(
                      block: Provider.of<FlowProvider>(context, listen: false).flow!.endBlock),
                );
              }
            }
          },
          child: Text(utf8convert(widget.text),
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Colors.black,
                fontSize: 24.0,
              )),
        ),
      ),
    );
  }
}

class ButtonRow extends StatefulWidget {
  final List<int> options;

  const ButtonRow({super.key, required this.options});

  @override
  State<ButtonRow> createState() => _ButtonRowState();
}

class _ButtonRowState extends State<ButtonRow> {
  late Option optionsobj;

  Widget getChoiceButtonFromOptionId(int optionId) {
    optionsobj = Provider.of<BlockProvider>(context, listen: false).getOptionFromId(optionId);
    if (optionsobj.follow_up_block_id != null) {
      return ChoiceButton(
        text: optionsobj.text,
        follow_up_block_id: optionsobj.follow_up_block_id,
      );
    } else {
      if (Provider.of<FlowProvider>(context, listen: false).flow == null) {
        return const Text('Loading flow...');
      }
      return ChoiceButton(
        text: optionsobj.text,
        follow_up_block_id: Provider.of<FlowProvider>(context, listen: false).flow!.endBlock.id,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    debugPrint('emojirow');
    return Padding(
      padding: const EdgeInsets.all(32.0),
      child: Center(
        child: IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              for (var option in widget.options) getChoiceButtonFromOptionId(option),
            ],
          ),
        ),
      ),
    );
  }
}
