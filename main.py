# -*- coding: utf-8 -*-
import os
import sys
import platform
import subprocess
import json
import shutil
import tempfile
from pathlib import Path

def detect_platform():
    """Detect the current operating system"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    return "unknown"

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    # Check if Node.js and npm are installed
    try:
        node_version = subprocess.check_output(["node", "--version"], stderr=subprocess.STDOUT, text=True)
        print(f"✅ Node.js {node_version.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("💀 Node.js is not installed")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    try:
        npm_version = subprocess.check_output(["npm", "--version"], stderr=subprocess.STDOUT, text=True)
        print(f"✅ npm {npm_version.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("💀 npm is not installed")
        return False
    
    return True

def create_electron_app(app_name, url, icon_path=None, width=1024, height=768):
    """Create an Electron application"""
    app_dir = f"build_{app_name}"
    os.makedirs(app_dir, exist_ok=True)
    
    # Create package.json
    package_json = {
        "name": app_name.lower().replace(" ", "-"),
        "version": "1.0.0",
        "description": f"{app_name} - Web App",
        "main": "main.js",
        "scripts": {
            "start": "electron .",
            "build": "electron-builder",
            "dist": "npm run build -- --publish=never"
        },
        "author": "Web2App Builder",
        "license": "MIT",
        "devDependencies": {
            "electron": "^28.0.0",
            "electron-builder": "^24.0.0"
        },
        "build": {
            "appId": f"com.web2app.{app_name.lower().replace(' ', '-')}",
            "productName": app_name,
            "directories": {
                "output": "dist"
            },
            "files": [
                "main.js",
                "preload.js",
                "package.json"
            ],
            "win": {
                "target": "nsis",
                "icon": "icon.ico" if icon_path and icon_path.endswith('.ico') else None
            },
            "linux": {
                "target": "AppImage",
                "icon": "icon.png" if icon_path and icon_path.endswith('.png') else None
            },
            "mac": {
                "target": "dmg",
                "icon": "icon.icns" if icon_path and icon_path.endswith('.icns') else None
            }
        }
    }
    
    with open(os.path.join(app_dir, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)
    
    # Create main.js
    main_js = f'''
const {{ app, BrowserWindow, shell }} = require('electron');
const path = require('path');

let mainWindow;

function createWindow () {{
  // Create the browser window
  mainWindow = new BrowserWindow({{
    width: {width},
    height: {height},
    webPreferences: {{
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    }},
    icon: path.join(__dirname, '{'icon.ico' if icon_path and icon_path.endswith('.ico') else 'icon.png' if icon_path and icon_path.endswith('.png') else 'icon.icns' if icon_path and icon_path.endswith('.icns') else ''}'),
    show: false
  }});

  // Load the URL
  mainWindow.loadURL('{url}');

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {{
    mainWindow.show();
  }});

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({{ url }}) => {{
    shell.openExternal(url);
    return {{ action: 'deny' }};
  }});

  // Emitted when the window is closed
  mainWindow.on('closed', function () {{
    mainWindow = null;
  }});
}}

// This method will be called when Electron has finished initialization
app.whenReady().then(createWindow);

// Quit when all windows are closed
app.on('window-all-closed', function () {{
  if (process.platform !== 'darwin') app.quit();
}});

app.on('activate', function () {{
  if (mainWindow === null) createWindow();
}});

// Security: Prevent navigation
app.on('web-contents-created', (event, contents) => {{
  contents.on('will-navigate', (event, navigationUrl) => {{
    const parsedUrl = new URL(navigationUrl);
    
    if (parsedUrl.origin !== new URL('{url}').origin) {{
      event.preventDefault();
      shell.openExternal(navigationUrl);
    }}
  }});
}});
'''
    
    with open(os.path.join(app_dir, "main.js"), "w") as f:
        f.write(main_js)
    
    # Create preload.js
    preload_js = '''
// Preload script for security
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // You can add APIs here if needed
});
'''
    
    with open(os.path.join(app_dir, "preload.js"), "w") as f:
        f.write(preload_js)
    
    # Copy icon if provided
    if icon_path and os.path.exists(icon_path):
        icon_ext = os.path.splitext(icon_path)[1].lower()
        dest_icon = os.path.join(app_dir, f"icon{icon_ext}")
        shutil.copy2(icon_path, dest_icon)
        print(f"✅ Icon copied: {dest_icon}")
    
    return app_dir

def install_electron_dependencies(app_dir):
    """Install Electron dependencies"""
    print("Installing Electron dependencies...")
    
    try:
        # Change to app directory
        original_cwd = os.getcwd()
        os.chdir(app_dir)
        
        # Install dependencies
        subprocess.run(["npm", "install"], check=True, capture_output=True)
        
        # Return to original directory
        os.chdir(original_cwd)
        
        print("✅ Electron dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"💀 Failed to install Electron dependencies: {e}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return False

def build_electron_app(app_dir, target_platform):
    """Build the Electron app for the target platform"""
    print(f"Building Electron app for {target_platform}...")
    
    try:
        # Change to app directory
        original_cwd = os.getcwd()
        os.chdir(app_dir)
        
        # Build for target platform
        if target_platform == "exe":
            build_cmd = ["npm", "run", "build", "--", "--win"]
        elif target_platform == "linux":
            build_cmd = ["npm", "run", "build", "--", "--linux"]
        else:
            build_cmd = ["npm", "run", "build"]
        
        subprocess.run(build_cmd, check=True, capture_output=True)
        
        # Return to original directory
        os.chdir(original_cwd)
        
        print("✅ Electron app built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"💀 Failed to build Electron app: {e}")
        if e.stderr:
            print(f"Error: {e.stderr.decode()}")
        return False

def find_built_app(app_dir, app_name, target_platform):
    """Find the built application"""
    dist_dir = os.path.join(app_dir, "dist")
    
    if not os.path.exists(dist_dir):
        return None
    
    # Look for the built application
    if target_platform == "exe":
        # Look for .exe or installer
        for item in os.listdir(dist_dir):
            if item.endswith(".exe") and app_name.lower() in item.lower():
                return os.path.join(dist_dir, item)
    elif target_platform == "linux":
        # Look for .AppImage
        for item in os.listdir(dist_dir):
            if item.endswith(".AppImage") and app_name.lower() in item.lower():
                return os.path.join(dist_dir, item)
    
    # If not found, return the first executable file
    for item in os.listdir(dist_dir):
        if (item.endswith(".exe") or item.endswith(".AppImage") or 
            item.endswith(".dmg") or item.endswith(".deb")):
            return os.path.join(dist_dir, item)
    
    return None

def main():
    print("💀💀 Full Electron Web2App Builder 💀💀")
    print("This tool creates standalone Electron applications from websites")
    print("Full CSS, JavaScript, and modern web features supported! 🚀")
    
    # Check dependencies
    if not check_dependencies():
        print("💀 Required dependencies are missing")
        sys.exit(1)
    
    # 1. Website URL
    url = input("Enter the website URL: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        print(f"⚠️  Added https:// prefix: {url}")
    
    # 2. App name
    app_name = input("Enter the app name: ").strip()
    if not app_name:
        print("💀 Invalid app name")
        sys.exit(1)
    
    # 3. Icon file
    icon_path = input("Enter icon file path (optional, press Enter to skip): ").strip()
    if icon_path and not os.path.exists(icon_path):
        print("💀 Icon file not found")
        sys.exit(1)
    elif not icon_path:
        print("⚠️  No icon specified - using default")
    
    # 4. Window size
    try:
        width = int(input("Enter window width (default: 1024): ").strip() or "1024")
        height = int(input("Enter window height (default: 768): ").strip() or "768")
    except ValueError:
        print("⚠️  Invalid size, using defaults")
        width, height = 1024, 768
    
    # 5. Target platform
    current_platform = detect_platform()
    print(f"🖥️  Detected platform: {current_platform}")
    
    target_platform = input("Target platform (exe/linux): ").strip().lower()
    if target_platform not in ("exe", "linux"):
        print("💀 Invalid platform")
        sys.exit(1)
    
    # Create Electron app
    print("🚀 Creating Electron application...")
    app_dir = create_electron_app(app_name, url, icon_path, width, height)
    print(f"✅ Electron app structure created: {app_dir}")
    
    # Install dependencies
    if not install_electron_dependencies(app_dir):
        print("💀 Failed to install dependencies")
        sys.exit(1)
    
    # Build the app
    if not build_electron_app(app_dir, target_platform):
        print("💀 Failed to build Electron app")
        sys.exit(1)
    
    # Find the built app
    built_app = find_built_app(app_dir, app_name, target_platform)
    
    if built_app and os.path.exists(built_app):
        print(f"🎉 Electron app built successfully!")
        print(f"📁 Output file: {built_app}")
        print(f"📦 Size: {os.path.getsize(built_app) / (1024*1024):.2f} MB")
        
        # Additional notes
        print("\n📝 Notes:")
        print("- Your app uses Electron with full Chromium engine")
        print("- All modern web features are supported (CSS3, JavaScript ES6+, etc.)")
        print("- The app is completely standalone and doesn't require a browser")
        print("- You can distribute this app to others")
    else:
        print("⚠️  Build completed but could not locate the output file")
        print("Checking dist directory...")
        
        dist_dir = os.path.join(app_dir, "dist")
        if os.path.exists(dist_dir):
            print("Dist directory contents:")
            for item in os.listdir(dist_dir):
                item_path = os.path.join(dist_dir, item)
                if os.path.isfile(item_path):
                    print(f"  {item} ({os.path.getsize(item_path) / (1024*1024):.2f} MB)")
                else:
                    print(f"  {item}/ (directory)")
        
        print("\n💡 Try running 'npm run build' manually in the app directory")
        print(f"App directory: {app_dir}")

if __name__ == "__main__":
    main()
