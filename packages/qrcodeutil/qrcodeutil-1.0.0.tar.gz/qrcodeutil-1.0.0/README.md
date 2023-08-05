# QR Code Decoder Python Library

The **QR Code Decoder Python Library** is a pure Python implementation of QR code decoding.

The few existing Python implementations, such as [`qrtools`](https://github.com/primetang/qrtools), actually depends on other libraries (e.g., [`Zbar`](http://zbar.sourceforge.net/index.html)), which your grandmother won't be able to install the same way on Windows, Mac, and Linux, in just one click, for sure. And you should consider most of the users, and even your pairs, like your grandmother.

This Python library is not intended to be used for real-time QR code decoding. It takes a few seconds per image.
