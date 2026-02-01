================================================================
  SudaPy Portable Windows Bundle
================================================================

REQUIREMENTS
  - Windows 10 or 11, 64-bit
  - No Python, pip, conda, or Visual Studio needed

QUICK START
  1. Extract this entire zip to a short path, e.g. C:\SudaPy
     (avoid paths with spaces or non-ASCII characters)
  2. Open a Command Prompt (cmd.exe)
  3. Navigate to the extracted folder:
       cd C:\SudaPy
  4. Run the health check:
       scripts\sudapy_doctor.bat
  5. Try a command:
       scripts\run_sudapy.bat crs suggest --lon 32.5 --lat 15.6

WHAT'S INSIDE
  scripts\
    run_sudapy.bat       -- Main launcher (forwards args to sudapy CLI)
    sudapy_doctor.bat    -- Double-click health check
    sudapy_env\          -- Self-contained Python + all libraries

TROUBLESHOOTING
  - "Cannot find bundled Python" -- Make sure you extracted the FULL
    zip contents. Windows may fail to extract deeply nested paths if
    the destination path is too long. Use a short path like C:\SudaPy.
  - Antivirus warnings -- Some antivirus software flags conda-packed
    environments. Add the SudaPy folder to your exclusion list.
  - For more help, visit:
    https://github.com/Osman-Geomatics93/sudapy/issues

VERSION
  SudaPy 1.2.0
================================================================
