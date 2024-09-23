import numpy as np
import ffmpeg
import matplotlib


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
