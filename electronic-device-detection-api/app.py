from flask import Flask, request, jsonify
import os
import base64
from label_image import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def convert_b64_to_file(b64, outfile_path):
    """
    b64をデコードしてファイルに書き込む
    """
    s = base64.decodebytes(b64)
    with open(outfile_path,"wb") as f:
        f.write(s)


@app.route('/', methods=['POST'])
def result():
    # Bad request
    if not request.headers['Content-Type'] == 'application/json':
        return jsonify(res='failure'), 400
    # jsonはdict型なので即変換できないからlistに入れて処理している

    # jsonを取得
    data = request.json
    # keysを取得
    keys_array = list(data.keys())
    # valuesを取得
    values_array = list(data.values())
    """
    送ってくるjsonは一つ目の要素が{画像名:base64エンコード}としたもの
    """

    # 画像の保存名
    save_name = keys_array[0] + ".jpg"
    # コンバート
    convert_b64_to_file(bytes(values_array[0], "utf-8"), save_name)

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

    return jsonify(final_dict)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
