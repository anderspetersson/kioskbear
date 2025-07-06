import 'package:flutter/material.dart';

class LoginForm extends StatelessWidget {
  @override
  build(BuildContext context) {
    return Container(
      alignment: Alignment.center,
      child: Column(
        children: [
          Flex(
            direction: Axis.vertical,
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.symmetric(vertical: 40.0, horizontal: 20.0),
                decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: const [
                      BoxShadow(
                        color: Colors.grey,
                        blurRadius: 10.0,
                        spreadRadius: 1.0,
                        offset: Offset(4.0, 4.0),
                      )
                    ]),
                child: Column(children: [
                  const Text(
                    'Login',
                    style: TextStyle(fontSize: 25.0, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 40.0),
                  TextFormField(
                    decoration: const InputDecoration(
                        prefixIcon: Icon(Icons.alternate_email), hintText: 'Email'),
                  ),
                  const SizedBox(height: 20.0),
                  TextFormField(
                    decoration: const InputDecoration(
                        prefixIcon: Icon(Icons.lock_outlined), hintText: 'Password'),
                  ),
                  const SizedBox(
                    height: 20.0,
                  ),
                  ElevatedButton(
                    child: const Padding(
                      padding: EdgeInsets.symmetric(horizontal: 48.0),
                      child: Text(
                        'Log in',
                        style: TextStyle(
                            color: Colors.white, fontWeight: FontWeight.bold, fontSize: 20.0),
                      ),
                    ),
                    onPressed: () {},
                  ),
                ]),
              )
            ],
          ),
        ],
      ),
    );
  }
}
