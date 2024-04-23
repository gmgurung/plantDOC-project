import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'dart:async';
import 'package:flutter/services.dart';
import 'dart:ui' as ui;
import 'package:image/image.dart' as img;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key});


// color scheme
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

// main body 

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

// converting image into numoy array
    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
        _convertAndPrintNumpy(_image!.path); // Convert and print numpy array
      } else {
        print('No image selected.');
      }
    });
  }

  Future<void> _convertAndPrintNumpy(String imagePath) async {
    Uint8List numpyArray = await convertImageToNumpy(imagePath);
    print(numpyArray);
  }

  Future<Uint8List> loadImage(String imagePath) async {
    final ByteData data = await rootBundle.load(imagePath);
    return data.buffer.asUint8List();
  }

  Future<Uint8List> convertImageToNumpy(String imagePath) async {
    // Load the image
    Uint8List imageData = await loadImage(imagePath);

    // Convert the image to a Flutter Image object
    ui.Image image = await decodeImageFromList(imageData);

    // Convert the Flutter Image object to an Image from the `image` package
    img.Image imgData = img.Image.fromBytes(image.width, image.height, await image.toByteData());

    // Convert the image to a numpy array
    List<List<int>> numpyArray = [];
    for (int y = 0; y < imgData.height; y++) {
      List<int> row = [];
      for (int x = 0; x < imgData.width; x++) {
        row.add(imgData.getPixel(x, y));
      }
      numpyArray.add(row);
    }

    // Flatten the 2D array to a 1D array
    List<int> flatArray = numpyArray.expand((row) => row).toList();

    // Convert the 1D array to Uint8List
    Uint8List result = Uint8List.fromList(flatArray);

    return result;
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
