import 'package:flutter/material.dart';
import 'native_bridge.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OCR Scanner',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const OCRScreen(),
    );
  }
}

class OCRScreen extends StatefulWidget {
  const OCRScreen({super.key});

  @override
  _OCRScreenState createState() => _OCRScreenState();
}

class _OCRScreenState extends State<OCRScreen> {
  String _recognizedText = "Hier erscheint der erkannte Text";

  void processImage() {

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('OCR Scanner')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(_recognizedText, textAlign: TextAlign.center),
            ElevatedButton(
              onPressed: processImage,
              child: const Text('Bild verarbeiten'),
            ),
          ],
        ),
      ),
    );
  }
}
