import arc
import os
import extism
import json

def handler(req, context):

    markup = "<my-header>Hello World</my-header>"
    element_path = './elements'
    elements = read_elements(element_path)
    initialState = {}
    data = {"markup":markup, "elements":elements, "initialState":initialState}
    payload = json.dumps(data, indent=4)

    manifest = {"wasm": [{"path": "./enhance-ssr.wasm"}]}
    with extism.Plugin(manifest, wasi=True) as plugin:
        rendered = plugin.call(
            "ssr",
            payload,
            parse = lambda output: json.loads(bytes(output).decode('utf-8'))
        )

    return arc.http.res(req, {"html": rendered['document']})


def read_elements(directory):
    elements = {}
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            key = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                elements[key] = file.read()
    return elements


