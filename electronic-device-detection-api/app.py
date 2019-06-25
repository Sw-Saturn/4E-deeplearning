from flask import Flask, render_template, request
import subprocess,os,json
from label_image import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('api_index.html')


@app.route('/result', methods=['GET','POST'])
def result():
    # submitした画像が存在したら処理する
    if request.files['image']:
        request.files['image'].save('./temp.jpg')

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
            print(labels[i], results[i])
            final_dict[labels[i]] = str(results[i])

        # render_template('./result.html')
        return render_template('result.html', title='予想クラス', predict_Confidence=final_dict)


if __name__ == '__main__':
    app.run()
