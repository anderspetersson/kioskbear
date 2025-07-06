import 'dart:async';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:kioskhero/components/components.dart';
import 'package:kioskhero/flow/flow_provider.dart';
import 'package:provider/provider.dart';

import '../providers.dart';
import '../utils/utf8.dart';
import 'flow_models.dart';

class BlockScreen extends StatefulWidget {
  final Block block;
  const BlockScreen({super.key, required this.block});

  @override
  State<BlockScreen> createState() => _BlockScreenState();
}

class _BlockScreenState extends State<BlockScreen> {
  Timer? countDownTimer;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      Timer.periodic(
        const Duration(seconds: 1),
        (timer) {
          if (Provider.of<FlowProvider>(context, listen: false).timeout > 0) {
            Provider.of<FlowProvider>(context, listen: false).tickTimer();
            debugPrint(Provider.of<FlowProvider>(context, listen: false)
                .timeout
                .toString());
          } else {
            timer.cancel();
            Provider.of<FlowProvider>(context, listen: false).resetTimer();
            Provider.of<ScreenProvider>(context, listen: false)
                .updateActiveScreen(
              SubmitRatingScreen(),
            );
          }
        },
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    if (widget.block.options != null) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
              child: Padding(
            padding: EdgeInsets.all(48.0),
            child: AutoSizeText(
              utf8convert(widget.block.title),
              style: TextStyle(fontSize: 48.0),
              maxLines: 1,
            ),
          )),
          ButtonRow(options: widget.block.options!)
        ],
      );
    } else if (widget.block.scoredOptions != null) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
              child: Padding(
            padding: EdgeInsets.all(48.0),
            child: AutoSizeText(
              utf8convert(widget.block.title),
              style: TextStyle(fontSize: 48.0),
              maxLines: 1,
            ),
          )),
          EmojiRow(options: widget.block.scoredOptions!)
        ],
      );
    } else {
      return Text('No content');
    }
  }
}

class SubmitRatingScreen extends StatefulWidget {
  const SubmitRatingScreen({
    super.key,
  });

  @override
  State<SubmitRatingScreen> createState() => _SubmitRatingScreenState();
}

class _SubmitRatingScreenState extends State<SubmitRatingScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((timeStamp) {
      Provider.of<FlowProvider>(context, listen: false).getMyFlow();
      Provider.of<BlockProvider>(context, listen: false).getAllBlocks();
      Provider.of<BlockProvider>(context, listen: false).getAllScoredOptions();
      Provider.of<BlockProvider>(context, listen: false).getAllOptions();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (Provider.of<FlowProvider>(context).isLoading ||
        Provider.of<BlockProvider>(context).isLoadingOptions ||
        Provider.of<BlockProvider>(context).isLoadingBlocks) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    } else {
      if (Provider.of<FlowProvider>(context).flow == null) {
        return const Center(
          child: CircularProgressIndicator(),
        );
      }
      Block block = Provider.of<BlockProvider>(context).getBlockFromId(
          Provider.of<FlowProvider>(context).flow!.startBlock.id);

      return Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Center(
              child: Padding(
            padding: EdgeInsets.all(48.0),
            child: AutoSizeText(
              utf8convert(block.title),
              style: const TextStyle(fontSize: 48.0),
              maxLines: 1,
            ),
          )),
          block.scoredOptions != null
              ? EmojiRow(options: block.scoredOptions!)
              : block.options != null
                  ? Text('show options')
                  : Text('both options and scored options null'),
        ],
      );
    }
  }
}
