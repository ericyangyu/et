from typing import Tuple

import numpy as np
import ffmpeg
import matplotlib


def recommend_fps(num_potential_frames, num_desired_frames, min_secs: int, max_secs: int) -> Tuple[int, int]:
    """
    Recommend an iteration stepsize and framerate for a video. Minimum 1 fps. This should be used like
    ```
    iter_stepsize, fps = recommend_fps(num_iterations, 10, 5, 10)
    for i in range(iter_stepsize, num_iterations + iter_stepsize, iter_stepsize):
        subset_data = data[:i]
        ...
    make_video(frames, 'video.mp4', fps=fps)
    ```

    Parameters
    ----------
    num_potential_frames : int
        Number of potential frames that will be in the video.
    num_desired_frames : int
        Number of desired frames in the video.
    min_secs : int
        Minimum number of seconds the video should be.
    max_secs : int
        Maximum number of seconds the video should be.

    Returns
    -------
    int
        Recommended framerate for the video.
    """
    assert num_potential_frames >= num_desired_frames, "Number of potential frames should be greater than the number of desired frames."
    assert num_desired_frames > 0, "Number of desired frames should be greater than 0."

    iter_stepsize = num_potential_frames // num_desired_frames
    fps = max(1, min(num_desired_frames // min_secs, num_desired_frames // max_secs))
    return iter_stepsize, fps


def make_video(frames: list, save_path, fps: int = 60):
    """
    Make a video from a list of frames (RGB images).

    Parameters
    ----------
    frames : list
        List of frames to make a video from.
    num_secs : int
        Number of seconds to make the video.
    save_path : str
        Path to save the video.
    framerate : int
        Framerate of the video.
    """
    def vidwrite(fn, images, framerate=60, vcodec='libx264'):
        """
        Stolen from: https://github.com/kkroening/ffmpeg-python/issues/246
        """
        if not isinstance(images, np.ndarray):
            images = np.asarray(images)
        n, height, width, channels = images.shape
        process = (
            ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(width, height), r=framerate)
            .output(fn, pix_fmt='yuv420p', vcodec=vcodec)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        for frame in images:
            process.stdin.write(
                frame
                .astype(
                    np.uint8)
                .tobytes()
            )
        process.stdin.close()
        process.wait()

    vidwrite(save_path, frames, framerate=fps)

def extract_frame(fig: matplotlib.figure.Figure) -> np.ndarray:
    """
    Extract a frame from a canvas.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to extract the frame from.

    Returns
    -------
    np.ndarray
        RGB image frame extracted from the canvas as a numpy array.
    """
    fig.canvas.draw()
    width, height = (fig.get_size_inches() * fig.get_dpi()).astype(np.int32)
    return np.fromstring(fig.canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
