#include <iostream>
#include <opencv2.4/opencv/cv.hpp>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <string>

extern "C" {
    __declspec(dllexport) const char* extract_text(const char* image_path) {
        cv::Mat image = cv::imread(image_path, cv::IMREAD_GRAYSCALE);
        if (image.empty()) {
            return "Fehler: Bild konnte nicht geladen werden.";
        }

        // Bild vorverarbeiten
        cv::threshold(image, image, 150, 255, cv::THRESH_BINARY);

        // OCR mit Tesseract
        tesseract::TessBaseAPI tess;
        tess.Init(NULL, "eng", tesseract::OEM_LSTM_ONLY);
        tess.SetImage(image.data, image.cols, image.rows, 1, image.step);
        std::string result = tess.GetUTF8Text();

        // String als C-String zurückgeben
        return result.c_str();
    }
}
