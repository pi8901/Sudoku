import 'dart:ffi' as ffi;
import 'dart:io';
import 'package:ffi/ffi.dart';

// Lade die C++-Bibliothek
final ffi.DynamicLibrary nativeLib = ffi.DynamicLibrary.open("OCR.dll"); // Windows


// Signatur der C++-Funktion
typedef ExtractTextC = ffi.Pointer<Utf8> Function(ffi.Pointer<Utf8>);
typedef ExtractTextDart = ffi.Pointer<Utf8> Function(ffi.Pointer<Utf8>);

// Verknüpfung mit der C++-Funktion
final ExtractTextDart extractText = nativeLib
    .lookup<ffi.NativeFunction<ExtractTextC>>('extract_text')
    .asFunction();

String getTextFromImage(String imagePath) {
  final pathPointer = imagePath.toNativeUtf8();
  ffi.Pointer<Utf8> resultPointer = extractText(pathPointer);
  String result = resultPointer.toDartString();
  calloc.free(pathPointer);
  return result;
}
