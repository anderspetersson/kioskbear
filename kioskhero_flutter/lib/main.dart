import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import 'flow/flow_provider.dart';
import 'providers.dart';
import 'utils/theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.manual, overlays: [
    SystemUiOverlay.bottom,
  ]);
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => BlockProvider()),
        ChangeNotifierProvider(create: (context) => FlowProvider()),
        ChangeNotifierProvider(create: (context) => ScreenProvider()),
      ],
      child: MainApp(),
    ),
  );
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: lightGreen,
        colorScheme: ColorScheme(
            background: lightGreen,
            primary: lightGreen,
            onBackground: darkerGrey,
            onPrimary: Colors.white,
            brightness: Brightness.light,
            secondary: lightGrey,
            onSecondary: darkerGrey,
            error: Colors.red,
            onError: Colors.white,
            surface: lightGrey,
            onSurface: darkerGrey),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20.0),
            borderSide: BorderSide(color: lightGreen),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(20.0),
            borderSide: BorderSide(color: darkerGrey),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
              backgroundColor: lightGreen,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20.0),
              ),
              padding: EdgeInsets.symmetric(horizontal: 20.0),
              minimumSize: Size.fromHeight(54.0)),
        ),
      ),
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                Colors.white,
                Colors.white54,
              ],
            ),
          ),
          child: SafeArea(
            child: Provider.of<ScreenProvider>(context).activeScreen,
          ),
        ),
      ),
    );
  }
}
