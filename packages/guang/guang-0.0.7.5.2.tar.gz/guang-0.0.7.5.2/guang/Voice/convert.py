import os
from pydub import AudioSegment


def cvt2wav(orig_path, new_path, sr=16000):
    basename = os.path.basename(orig_path)
    sufname = basename.split('.')[-1]

    x = AudioSegment.from_file(orig_path, format=sufname)
    x = x.set_channels(1)
    x = x.set_frame_rate(sr)
    x = x.set_sample_width(2)
    x.export(new_path, format='wav')


if __name__ == "__main__":
    pass
