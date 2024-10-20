import numpy as np
import ffmpeg
import matplotlib.figure

from loguru import logger
from typing import Tuple, Dict, Any

from prettytable import PrettyTable


def pprint_table(data: Dict[Any, Dict[Any, Any]]) -> None:
    """
    Pretty print a 2-D table of data.

    ```
    data = {
        'Category 1': {
            'Metric 1': 1,
        }
    }
    ```

    Parameters
    ----------
    data : list
        2-D list of data to pretty print. The shape is expected to be
    """
    # Get all listed metrics across methods
    metrics = set()
    for method in data:
        metrics |= set(data[method].keys())
    metrics = [''] + sorted(list(metrics))

    t = PrettyTable(list(metrics))
    for method in data:
        row = [method] + [data[method][metric] if data[method].get(metric) is not None else '' for metric in metrics[1:]]
        # Round floats by 3 decimal places
        row = [round(x, 3) if isinstance(x, float) else x for x in row]
        t.add_row(row)

    logger.info('\n' + t.__repr__())

def convert_mp4_to_gif(mp4_path: str, gif_path: str = None):
    """
    Convert an mp4 video to a gif.

    Parameters
    ----------
    mp4_path : str
        Path to the mp4 video.
    gif_path : str
        Path to save the gif.
    """
    if gif_path is None:
        gif_path = mp4_path.replace('.mp4', '.gif')
    ffmpeg.input(mp4_path).output(gif_path).run()
    logger.info(f'Converted {mp4_path} to {gif_path}.')

def recommend_fps(num_potential_frames, num_desired_frames, min_secs: int, max_secs: int) -> Tuple[int, int, int]:
    """
    Recommend an iteration stepsize and framerate for a video. Minimum 1 fps. This should be used like
    ```
    iter_stepsize, fps = recommend_fps(num_iterations, 10, 5, 10)
    for i in range(iter_stepsize, num_iterations + iter_stepsize, iter_stepsize):
        subset_data = data[:i]
        ...
    make_video(frames, 'video.mp4', fps=fps)
    ```

    Note that if the number of desired frames is not easy to compute given the number of potential frames, then we
    overestimate (e.g. for 15 potential frames and 10 desired frames, the stepsize is 2 and number of collected frames
    is ceil(15/2) = 8, which is less than 10).

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
        Recommended iteration stepsize for the video.
    int
        Recommended framerate for the video.
    int
        Number of frames that will be in the video.
    """
    assert num_potential_frames >= num_desired_frames, "Number of potential frames should be greater than the number of desired frames."
    assert max_secs >= min_secs, "Maximum number of seconds should be greater than or equal to the minimum number of seconds."
    assert num_desired_frames > 0, "Number of desired frames should be greater than 0."

    iter_stepsize = np.ceil(num_potential_frames / num_desired_frames).astype(np.int32).item()
    fps = max(1, min(num_desired_frames // min_secs, num_desired_frames // max_secs))
    num_frames = np.ceil(num_potential_frames / iter_stepsize).astype(np.int32).item()
    if num_frames != num_desired_frames:
        logger.info(f'Number of desired frames is not easy to compute given the number of potential frames. '
                    f'Overestimating the number of frames to {num_frames}.')
    return iter_stepsize, fps, num_frames


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
