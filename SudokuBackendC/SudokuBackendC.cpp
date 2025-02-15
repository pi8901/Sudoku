#include <iostream>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <string>

extern "C" {
    __declspec(dllexport) const char* extract_text(const char* image_path) {

        // OCR mit Tesseract
        tesseract::TessBaseAPI tess;
        tess.Init(NULL, "eng", tesseract::OEM_LSTM_ONLY);
        std::string result = "Hello World";

        // String als C-String zurückgeben
        return result.c_str();
    }
}
