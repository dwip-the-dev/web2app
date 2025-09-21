# Web2App Builder 🚀

A powerful tool to convert any website into a standalone desktop application for Windows and Linux. Built with Electron for full web compatibility.

![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![Electron](https://img.shields.io/badge/Electron-28.0.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)

## Features ✨

- **Full Web Compatibility**: Uses Electron with Chromium engine - supports all modern web features (CSS3, JavaScript ES6+, WebGL, etc.)
- **Cross-Platform**: Build Windows (.exe) and Linux (.AppImage) applications from any platform
- **Professional Packaging**: Creates professional installers using electron-builder
- **Customizable**: Set custom window size, application name, and icons
- **Security**: Built with security best practices including context isolation
- **Standalone**: Applications don't require a browser to run

## Prerequisites 📋

### System Requirements
- Python 3.8+
- Node.js 16+
- npm (comes with Node.js)

### Platform-Specific Dependencies
**Linux:**
```bash
sudo apt-get install fakeroot rpm
```

**Windows:** No additional dependencies needed

**macOS:** Xcode command line tools (if building on macOS)

## Installation 🛠️

1. **Clone the repository:**
```bash
git clone https://github.com/dwip-the-dev/web2app.git
cd web2app
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage 🚀

Run the builder script:

```bash
python main.py
```

Follow the interactive prompts:

1. **Enter website URL** - The web address you want to convert to an app
2. **Enter app name** - The name of your desktop application
3. **Icon file path** (optional) - Path to your application icon (.ico for Windows, .png for Linux)
4. **Window dimensions** - Custom width and height for your app window
5. **Target platform** - Choose between Windows (.exe) or Linux (.AppImage)

## Example 💡

```bash
$ python main.py
💀💀 Full Electron Web2App Builder 💀💀
Enter the website URL: https://example.com
Enter the app name: MyWebApp
Enter icon file path (optional): ./icon.ico
Enter window width: 1200
Enter window height: 800
Target platform (exe/linux): exe
```

## Output 📦

The builder will create:
- A complete Electron application structure in `build_YourAppName/`
- A standalone executable in the `dist/` folder:
  - Windows: `YourAppName Setup 1.0.0.exe`
  - Linux: `YourAppName-1.0.0.AppImage`

## Project Structure 📁

```
web2app-builder/
├── main.py              # Main builder script
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── build_AppName/      # Generated Electron app (created during build)
    ├── package.json
    ├── main.js
    ├── preload.js
    ├── icon.ico/png
    └── dist/           # Final built application
```

## How It Works 🔧

1. **Scaffolding**: Creates a complete Electron application structure
2. **Dependency Management**: Automatically installs Electron and build tools
3. **Packaging**: Uses electron-builder to create professional installers
4. **Security**: Implements context isolation and secure preload scripts
5. **Distribution**: Generates standalone executables that don't require Node.js

## Security 🔒

The generated applications include:
- Context isolation enabled
- Node integration disabled
- Secure preload scripts
- External link handling (opens in default browser)
- Navigation restrictions to prevent phishing

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

If you have any questions or issues:

1. Check the [Issues](https://github.com/dwip-the-dev/web2app/issues) page
2. Create a new issue if your problem isn't already listed

## Acknowledgments 🙏

- [Electron](https://electronjs.org/) - For the amazing framework that makes this possible
- [electron-builder](https://github.com/electron-userland/electron-builder) - For professional application packaging
- [Python](https://python.org) - For the versatile scripting language

---

**Note**: This tool is designed for legitimate purposes. Please ensure you have the right to convert and distribute any website you transform into an application.
