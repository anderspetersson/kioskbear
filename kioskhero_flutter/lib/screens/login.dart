import 'package:flutter/material.dart';
import 'package:kioskhero/screens/localwidgets/login_form.dart';

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constrains) => ListView(children: [
        Container(
          padding: const EdgeInsets.all(20.0),
          constraints: BoxConstraints(minHeight: constrains.maxHeight),
          child: LoginForm(),
        ),
      ]),
    );
  }
}
