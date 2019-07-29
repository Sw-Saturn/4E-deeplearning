from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from label_image import *
import os
import json
import time

target_dir = './'
target_file = '*.jpg'


def solve_result():
    # 画像の保存名
    load_graph('./retrained_graph.pb')
    label_file = "retrained_labels.txt"
    input_height = 299
    input_width = 299
    input_mean = 0
    input_std = 255
    input_layer = "Placeholder"
    output_layer = "final_result"

    graph = load_graph('./retrained_graph.pb')
    t = read_tensor_from_image_file(
        './temp.jpg',
        input_height=input_height,
        input_width=input_width,
        input_mean=input_mean,
        input_std=input_std)

    input_name = "import/" + input_layer
    output_name = "import/" + output_layer
    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {
            input_operation.outputs[0]: t
        })
    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    final_dict = {}
    for i in top_k:
        results[i] = results[i] * 100
        final_dict[labels[i]] = str('{:.2f}'.format(results[i]))
        print(labels[i], results[i])

    with open('result.json', 'w') as f:
        json.dump(final_dict, f, indent=4)


# PatternMatchingEventHandler の継承クラスを作成
class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self, patterns):
        super(FileChangeHandler, self).__init__(patterns=patterns)

    # ファイル作成時のイベント
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s created' % filename)
        if filename == 'temp.jpg':
            solve_result()

    # ファイル変更時のイベント
    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s changed' % filename)
        if filename == 'temp.jpg':
            solve_result()

    # ファイル削除時のイベント
    def on_deleted(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s deleted' % filename)

    # ファイル移動時のイベント
    def on_moved(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print('%s moved' % filename)


# コマンド実行の確認
if __name__ == "__main__":
    # ファイル監視の開始
    event_handler = FileChangeHandler([target_file])
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
