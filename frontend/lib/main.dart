import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sudoku Solver',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const SudokuScreen(),
    );
  }
}

class SudokuScreen extends StatefulWidget {
  const SudokuScreen({super.key});

  @override
  _SudokuScreenState createState() => _SudokuScreenState();
}

class _SudokuScreenState extends State<SudokuScreen> {
  List<List<int>> sudokuGrid = [];
  String? imagePath;

  Future<void> solveSudoku() async {
    if (imagePath == null) {
      print('Kein Bild ausgewählt.');
      return;
    }

    // Bild auswählen und an die API senden
    var uri = Uri.parse('http://10.0.2.2:5000/solve');
    var request = http.MultipartRequest('POST', uri);

    // Füge das Bild als Datei zum Request hinzu
    var imageFile = await http.MultipartFile.fromPath('image', imagePath!);
    request.files.add(imageFile);

    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var responseBody = await response.stream.bytesToString();
        // Antwort als JSON dekodieren
        setState(() {
          sudokuGrid = (jsonDecode(responseBody) as List)
              .map((row) => (row as List).map((cell) => cell as int).toList())
              .toList();
        });
      } else {
        print('Fehler: ${response.statusCode}');
      }
    } catch (e) {
      print('Fehler beim Senden der Anfrage: $e');
    }
  }

  Future<void> pickImage() async {
    // Mit ImagePicker ein Bild auswählen
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        imagePath = pickedFile.path;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Sudoku Solver')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (imagePath != null) ...[
              Image.file(File(imagePath!)),
              const SizedBox(height: 20),
            ],
            sudokuGrid.isEmpty
                ? const Text("Klicke auf den Button, um Sudoku zu lösen")
                : Column(
              children: sudokuGrid
                  .map((row) => Text(row.toString()))
                  .toList(),
            ),
          ],
        ),
      ),
      floatingActionButton: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: pickImage,
            child: const Icon(Icons.image),
            tooltip: 'Bild auswählen',
          ),
          const SizedBox(width: 20),
          FloatingActionButton(
            onPressed: solveSudoku,
            child: const Icon(Icons.camera),
            tooltip: 'Sudoku lösen',
          ),
        ],
      ),
    );
  }
}
