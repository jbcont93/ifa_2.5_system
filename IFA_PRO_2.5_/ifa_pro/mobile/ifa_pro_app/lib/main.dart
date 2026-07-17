import 'package:flutter/material.dart';
import 'core/theme.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const IfaProApp());
}

class IfaProApp extends StatelessWidget {
  const IfaProApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'IFA PRO 2.5',
      debugShowCheckedModeBanner: false,
      theme: IfaTheme.dark,
      home: const LoginScreen(),
    );
  }
}
