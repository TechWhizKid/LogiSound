# LogiSound

_**A program that allows the user to select a unique sound effect that matches an image that pops up when the user signs in.**_

![Static Badge](https://img.shields.io/badge/Version-v1.0-blue)

---

## Get Started

To get started with LogiSound, you can clone the project using _**git:**_

```bash
git clone https://github.com/TechWhizKid/LogiSound.git
```

Next, install the required dependencies using _**pip:**_

```bash
pip install -r requrements.txt
```

**_or_**

```bash
pip install pygame pywin32
```

#### And then:

Open `\templates\...\` and run `build.vbs` to generate a file called `LogiSound.dat`. This file will be used by the app if it is placed in the same directory as the LogiSound executable or LogiSound python script. To create your own `LogiSound.dat`, follow these steps:

**Step 1**: Place your chosen image and sound file in the same folder.<br>
**Step 2**: Create a configuration file named `config.ini` and open it for editing.<br>
**Step 3**: Add a section named `[LogiSound_Config]` in the `config.ini` file.<br>
**Step 4**: Write the configuration file according to the commented instructions.<br>

```ini
[LogiSound_Config]
REQUIRED = ["config.ini", "image.png", "sound.mp3"] // The files that are essential for the program.
IMAGE_FILE = image.png     // The image that will be displayed on the screen, must be included in `REQUIRED`.
SOUND_FILE = sound.mp3     // The sound that will be played along with the image, must be included in `REQUIRED`.
REPEAT_SOUND = 1           // The number of repetitions of the sound before the program terminates.
SOUND_VOLUME = 1.5         // The volume level of the sound file in integer or boolean.
WINDOW_WIDTH = 800         // The width of the window that contains the image.
WINDOW_HEIGHT = 462        // The height of the window that contains the image.
IMG_ROUNDNESS = 25         // The degree of curvature of the image corners.
WIN_ROUNDNESS = 45         // The degree of curvature of the window edges. (not same as the image)
```

**Step 5**: Open the terminal in working dir and execute the command `tar -cf LogiSound.dat config.ini image.png sound.mp3`.

- **Note**: replace `image.png` and `sound.mp3` with your file's name.

**Step 6**: Move the generated `LogiSound.dat` file to the same folder as the `LogiSound` script or executable.

The setup is complete and you can run `LS_setup.vbs` to configure it to run when you log in. **Note**: The current folder will be used as the installation directory.

---
