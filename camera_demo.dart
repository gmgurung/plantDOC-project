import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'camera demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSwatch(
  primarySwatch: MaterialColor(0xFF58B76D, {
      50: Color(0xFFDCEDD8), // Lightest shade
      100: Color(0xFFC5E0BD),
      200: Color(0xFF9DD9A2),
      300: Color(0xFF74D186),
      400: Color(0xFF5ECF75), // Main color
      500: Color(0xFF58B76D), // Main color
      600: Color(0xFF4E9F62),
      700: Color(0xFF448857),
      800: Color(0xFF3A704C),
      900: Color(0xFF2A5039), // Darkest shade
    }),
),

        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'camera demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  File? _image;
  final picker = ImagePicker();

  Future<void> _getImage(ImageSource source) async {
    var pickedFile = await picker.pickImage(source: source);

    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
      } else {
        print('No image selected.');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.secondary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            _image == null
                ? const Text('No image selected.')
                : Image.file(_image!),
            const SizedBox(height: 80),
            ElevatedButton(
              onPressed: () => _getImage(ImageSource.gallery),
              child: const Text('Pick Image from Gallery'),
            ),
            ElevatedButton(
              onPressed: () => _getImage(ImageSource.camera),
              child: const Text('Take a Photo'),
            ),

          ],
        ),
      ),
    );
  }
}
