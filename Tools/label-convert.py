import os
import json
import base64


with open("sample.json") as json_file:
    form = json.loads(json_file.read())

folder = "train_images_label"
images = "train_images"
output = "train_labels"

files_path = [x for x in os.listdir("train_images_label") if x.split(".")[-1] == 'txt']

count = 0
for file in files_path:
    print("Đang xử lý: {}".format(os.path.join(folder, file)))
    count += 1
    with open(os.path.join(folder, file), 'r') as f:
        objects = f.readlines()
        if len(objects) < 2:
            print("Image {} not valid!\n".format(os.path.join(folder, file)))
            continue
    
    with open(os.path.join(images, file.replace(".txt", ".jpg")), "rb") as image_file:
        base64_img =  base64.b64encode(image_file.read()).decode("utf-8")
    
    points = objects[0].split(",")[:4]
    text = objects[0].split(",")[-1].strip("\n")
    form['shapes'][0]['points'][0][0] = float(points[0])
    form['shapes'][0]['points'][0][1] = float(points[1])
    form['shapes'][0]['points'][1][0] = float(points[2])
    form['shapes'][0]['points'][1][1] = float(points[3])
    form['shapes'][0]['description'] = text
    form['imageData'] = base64_img

    points = objects[1].split(",")[:4]
    text = objects[1].split(",")[-1].strip("\n")
    form['shapes'][1]['points'][0][0] = float(points[0])
    form['shapes'][1]['points'][0][1] = float(points[1])
    form['shapes'][1]['points'][1][0] = float(points[2])
    form['shapes'][1]['points'][1][1] = float(points[3])
    form['shapes'][1]['description'] = text

    form['imagePath'] = "train_images\\{}".format(file.replace(".txt", ".jpg"))
    
    with open(os.path.join(output, file.replace(".txt", ".json")), 'w', encoding='utf-8') as w:
        json.dump(form, w, ensure_ascii=False, indent=2)
        print("Done {}/{}\n".format(count, len(files_path)))