from PIL import Image, ImageFont, ImageDraw
from jinja2 import Template
import time
import os


class specimen:
    def __init__(self, text_config, image_config):
        self.text_config = text_config
        self.image_config = image_config

    def save_image(self, filename, image, readings):
        with open(filename, 'wb') as file:
            file.write(image.getvalue())

        msg = self.format(readings)

        img = Image.open(filename, "r").convert("RGBA")
        img_draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(
            'roboto/Roboto-Regular.ttf', self.text_config["size"])
        colour = (self.text_config["colour"]["red"], self.text_config["colour"]
                  ["green"], self.text_config["colour"]["blue"])

        text_size = img_draw.textsize(msg, font)

        pos = (10, 20)
        bg_size = (text_size[0]+30, text_size[1]+50)
        bg_img = Image.new('RGBA', img.size, (0, 0, 0, 0))

        bg_draw = ImageDraw.Draw(bg_img)
        overlay_transparency = 150
        bg_draw.rectangle((pos[0], pos[1], bg_size[0], bg_size[1]), fill=(
            0, 0, 0, overlay_transparency), outline=(255, 255, 255))
        bg_draw.text(xy=(pos[0]+10, pos[1]+10),
                     text=msg, fill=colour, font=font)

        out = Image.alpha_composite(img, bg_img)
        print("Saving {}..".format(filename))
        r = out.convert('RGB')
        r.save(filename, "JPEG")
        print("Saved {}..OK".format(filename))

    def format(self, readings):
        degree_symbol = u"\u00b0"
        msg = "#growlab - {}\n".format(readings["time"])
        if "temperature" in readings:
            msg = msg + \
                " Temperature: {:5.2f}{}C \n".format(
                    readings["temperature"], degree_symbol)
        if "pressure" in readings:
            msg = msg + " Pressure: {:05.2f} hPa ({:d} mmHg) \n".format(
                readings["pressure"], readings["pressure_mmhg"])
        if "humidity" in readings:
            msg = msg + " Humidity: {:05.2f}% \n".format(readings["humidity"])
        if "light" in readings:
            msg = msg + " Light: {:5.2f} lx \n".format(readings["light"])
        if "camera_mode" in readings:
            msg = msg + \
                " IR-CUT Cam: {:s} \n".format(readings["camera_mode"])

        return msg.rstrip() + " "

    def save_html(self, input_filename, output_path, readings, is_image_taken):
        img_file_path = output_path + "/preview.jpg"
        if is_image_taken:
            img = Image.open(input_filename, "r")
            img = img.resize(
                (int(self.image_config["width"]/2), int(self.image_config["height"]/2)), Image.ANTIALIAS)
            img.save(img_file_path, "JPEG")
        elif os.path.exists(img_file_path):
            os.remove(img_file_path)

        template_text = ""
        with open("index.jinja", 'r') as file:
            template_text = file.read()

        template = Template(template_text)
        degree_symbol = u"\u00b0"

        vals = {}
        vals["time"] = readings["time"]
        if "temperature" in readings:
            vals["temperature"] = "{:5.2f}{}C".format(
                readings["temperature"], degree_symbol)
        else:
            vals["temperature"] = "N/A"

        if "humidity" in readings:
            vals["humidity"] = "{:05.2f}%".format(readings["humidity"])
        else:
            vals["humidity"] = "N/A"

        if "pressure" in readings:
            vals["pressure"] = "{:05.2f} hPa ({:d} mmHg)".format(
                readings["pressure"], readings["pressure_mmhg"])
        else:
            vals["pressure"] = "N/A"

        if "light" in readings:
            vals["light"] = "{:5.2f} lx".format(
                readings["light"])
        else:
            vals["light"] = "N/A"
        if "camera_mode" in readings:
            vals["camera_mode"] = "{:s}".format(readings["camera_mode"])
        else:
            vals["camera_mode"] = "N/A"

        vals["uid"] = "{}".format(time.time())

        html = template.render(vals)
        with open(output_path+"/index.html", "w") as html_file:
            html_file.write(html)
            print("Wrote {}..OK".format(output_path+"/index.html"))
