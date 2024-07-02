# Live wire Segmentation Tool

![Livewire Seg Tool](./1.png) <!-- Replace with your image URL -->

## Overview

The **Livewire Segmentation Tool** is an interactive image segmentation application designed to assist users in identifying and marking regions of interest in images. It uses basic image processing techniques and user input to generate accurate segmentation paths.

## Features

- **Interactive Path Suggestion**: Provides real-time suggestions for path segments.
- **Image Processing**: Handles multiple image formats including `.jpg`, `.png`, and `.tif`.
- **Save and Load Functionality**: Supports saving segmented paths and regions for later use.
- **Polygon Editing**: Enables the creation and editing of multiple polygons on the image.
- **Mask Generation**: Allows the creation of masks based on the segmented regions.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or above
- `Pillow` for image handling
- `numpy` for numerical computations
- `matplotlib` for plotting and visualizations

### Installation

1. Clone the repository:

  ```bash
    git clone https://github.com/alborz-esf/live-wire.git
    cd live-wire
   ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

    > **Note**: Ensure `requirements.txt` includes the necessary dependencies: `Pillow`, `numpy`, `matplotlib`.

### Usage

1. Run the main script:

    ```bash
    python livewire_tool.py
    ```

2. Follow the instructions on the console to input your image directory.

    ```plaintext
    Drag your picture folder dir here (special UTF-8 in path is not available)->
    ```

3. The application will display the first image from the directory. Use the following controls:

    - **A**: Switch to the previous image and save the current track.
    - **D**: Switch to the next image and save the current track.
    - **Space**: Begin or end editing mode.
    - **Mouse**: Use the left button to add key points or move to auto-fit a curve.
    - **C**: Clear the curves on the canvas.
    - **B**: Move to the next curve.
    - **S**: Save the current image with segments.
    - **M**: Create a mask of the segmented regions.

4. In editing mode, click on the image to add points for the path. The tool will suggest a path based on your input.

5. Save your segmented regions to a text file using the `savefile` or `savedots` function.

## Files

| File Name           | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `livewire_tool.py`  | Main script to run the segmentation tool.            |
| `requirements.txt`  | Lists the dependencies required for the project.     |
| `README.md`         | This README file providing an overview of the project. |

## Functions

### `openfiles(img_loc)`

Opens and resizes an image for processing.

### `savefile()`

Saves the segmented path to a text file.

### `savedots()`

Saves the coordinates of all segmented polygons.

### `nextfile()`

Loads the next image in the directory.

### `lastfile()`

Loads the previous image in the directory.

### `create_mask()`

Generates a mask based on the segmented regions.

### `refresh_frame(rescale=False)`

Refreshes the display of the current image and segments.

### `button_pressed(event)`

Handles mouse button press events for adding points.

### `mouse_moved(event)`

Handles mouse movement for interactive path suggestion.

### `key_pressed(event)`

Handles keyboard events for various functionalities like switching files, saving, and toggling edit mode.

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code adheres to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please contact [your-email@example.com](mailto:your-email@example.com).

