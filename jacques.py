# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: Жаконизатор
# Description: Жаконизатор
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# meta developer: @hikka_mods
# scope: Жаконизатор
# scope: Жаконизатор 0.0.1
# ---------------------------------------------------------------------------------

import io
import requests
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class JacquesMod(loader.Module):
    """Жаконизатор"""

    strings = {"name": "Жаконизатор", "usage": "Write <code>.help Жаконизатор</code>"}

    strings_ru = {"usage": "Напиши <code>.help Жаконизатор</code>"}

    def __init__(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "font",
                "https://github.com/Codwizer/ReModules/blob/main/assets/OpenSans-Light.ttf?raw=true",
                lambda: "добавьте ссылку на нужный вам шрифт",
            ),
            loader.ConfigValue(
                "location",
                "center",
                "Можно указать left, right или center",
                validator=loader.validators.Choice(["left", "right", "center"]),
            ),
        )

    @loader.command(
        ru_doc="<реплай на сообщение/свой текст>",
        en_doc="<reply to the message/your own text>",
    )
    async def ionicmd(self, message):
        ufr = requests.get(self.config["font"]).content
        f = ufr

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not args:
            if not reply:
                await utils.answer(message, self.strings("usage", message))
                return
            else:
                txt = reply.raw_text
        else:
            txt = utils.get_args_raw(message)
        pic = requests.get(
            "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/IMG_20231128_152538.jpg"
        )
        pic.raw.decode_content = True
        img = Image.open(io.BytesIO(pic.content)).convert("RGB")

        W, H = img.size
        text = "\n".join(wrap(txt, 19))
        t = text + "\n"
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(io.BytesIO(f), 32, encoding="UTF-8")
        w, h = draw.multiline_textsize(t, font=font)
        imtext = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(imtext)
        draw.multiline_text(
            (10, 10), t, (0, 0, 0), font=font, align=self.config["location"]
        )
        imtext.thumbnail((350, 195))
        w, h = 350, 195
        img.paste(imtext, (10, 10), imtext)
        out = io.BytesIO()
        out.name = "hikka_mods.jpg"
        img.save(out)
        out.seek(0)
        await message.client.send_file(message.to_id, out, reply_to=reply)
        await message.delete()
