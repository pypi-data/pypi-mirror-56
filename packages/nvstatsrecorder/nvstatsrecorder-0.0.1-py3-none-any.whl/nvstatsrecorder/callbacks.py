import tensorflow.compat.v2 as tf
from .recorders import NVStatsRecorder, NVLinkStatsRecorder


class NVStats(tf.keras.callbacks.Callback):
    def __init__(self, gpu_index=0, interval=1):
        self.gpu_index = int(gpu_index)
        self.interval = float(interval)

    def on_train_begin(self, logs=None):
        self.recorder = NVStatsRecorder(gpu_index=self.gpu_index)
        self.recorder.start(interval=self.interval)

    def on_train_end(self, logs=None):
        self.recorder.stop()
        self.data = self.recorder.get_data()


class NVLinkStats(tf.keras.callbacks.Callback):
    def __init__(self, sudo_password, gpus):
        self.sudo_password = str(sudo_password)
        self.gpu_list = [int(i) for i in gpus]

    def on_train_begin(self, logs=None):
        self.recorder = NVLinkStatsRecorder(self.sudo_password,
                                            self.gpu_list)
        self.recorder.start(interval=1)

    def on_train_end(self, logs=None):
        self.recorder.stop()
        self.data = self.recorder.get_data()
