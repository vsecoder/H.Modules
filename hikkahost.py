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
# Name: HikkaHost
# Description: Hikkahost manager.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: api HikkaHost
# scope: api HikkaHost 0.0.1
# ---------------------------------------------------------------------------------

import aiohttp
import json
from datetime import datetime, timedelta, timezone
from .. import loader, utils

__version__ = (1, 0, 0)


async def _request(path: str, token: str, method: str = "GET") -> dict:
    url = "http://158.160.84.24:5000" + path
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.request(
            method,
            url,
            headers={
                "Content-Type": "application/json",
                "token": token,
            },
            ssl=False,
        ) as response:
            return await response.json()


async def _stats(user_id, token):
    url = f"/api/host/{user_id}/stats"
    return await _request(url, token)


async def _host(user_id, token):
    url = f"/api/host/{user_id}"
    return await _request(url, token)


async def _status(user_id, token):
    url = f"/api/host/{user_id}/status"
    return await _request(url, token)


async def _logs(user_id, token):
    url = f"/api/host/{user_id}/logs/all"
    return await _request(url, token)


async def _action(user_id, token):
    url = f"/api/host/{user_id}?action=restart"
    return await _request(url, token, "PUT")


def bytes_to_megabytes(b: int):
    return round(b / 1024 / 1024, 1)


@loader.tds
class HikkahostMod(loader.Module):
    """Hikkahost manager."""

    MAX_RAM = 750

    strings = {
        "name": "HikkaHost",
        "info": (
            "<emoji document_id=5879770735999717115>👤</emoji> <b>Information panel</b>\n\n"
            "<emoji document_id=5974526806995242353>🆔</emoji> <b>Server ID:</b> <code>{server_id}</code>\n"
            "<emoji document_id=6005570495603282482>🔑</emoji> <b>ID:</b> <code>{id}</code>\n"
            "<emoji document_id=5874986954180791957>📶</emoji> <b>Status:</b> <code>{status}</code>\n"
            "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Subscription ends:</b> <code>{end_dates}</code> | <code>{days_end} days</code>\n\n"
            "<emoji document_id=5877260593903177342>⚙️</emoji> <b>CPU:</b> <code>{cpu_percent} %</code>\n"
            "<emoji document_id=5379652232813750191>💾</emoji> <b>RAM:</b> <code>{memory} / {max_ram} MB</code> <b>{ram_percent} %</b>"
        ),
        "logs": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>Here are your logs</b>"
        ),
        "restart": (
            "<emoji document_id=5789886476472815477>✅</emoji> <b>Restart request sent</b>\n"
            "This message remains unchanged after the restart"
        ),
        "loading_info": "<emoji document_id=5451646226975955576>⌛️</emoji> Loading...",
        "no_apikey": "<emoji document_id=5260342697075416641>🚫</emoji> You have not specified an API Key\nTo get a token.\n\n1. Go to the @hikkahost_bot\n2. Write /token\n3. Paste it into the config",
        "condition": "works",
    }

    strings_ru = {
        "info": (
            "<emoji document_id=5879770735999717115>👤</emoji> <b>Панель информации</b>\n\n"
            "<emoji document_id=5974526806995242353>🆔</emoji> <b>Server ID:</b> <code>{server_id}</code>\n"
            "<emoji document_id=6005570495603282482>🔑</emoji> <b>ID:</b> <code>{id}</code>\n"
            "<emoji document_id=5874986954180791957>📶</emoji> <b>Статус:</b> <code>{status}</code>\n"
            "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Подписка закончится:</b> <code>{end_dates}</code> | <code>{days_end} дней</code>\n\n"
            "<emoji document_id=5877260593903177342>⚙️</emoji> <b>CPU:</b> <code>{cpu_percent} %</code>\n"
            "<emoji document_id=5379652232813750191>💾</emoji> <b>RAM:</b> <code>{memory} / {max_ram} MB</code> <b>{ram_percent} %</b>"
        ),
        "logs": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>Вот ваши логи</b>"
        ),
        "restart": (
            "<emoji document_id=5789886476472815477>✅</emoji> <b>Запрос на рестарт отправил</b>\n"
            "Это сообщение не изменяется после рестарта"
        ),
        "loading_info": "<emoji document_id=5451646226975955576>⌛️</emoji> Загрузка...",
        "no_apikey": "<emoji document_id=5260342697075416641>🚫</emoji> Вы не указали Api Key\nЧтобы получить token.\n\n1. Перейдите в бота @hikkahost_bot\n2. Напишите /token\n3. Вставьте его в конфиг",
        "condition": "работает",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                validator=loader.validators.Hidden(),
            ),
        )

    @loader.command(
        ru_doc="Статус HikkaHost",
        en_doc="Status HikkaHost",
    )
    async def hinfocmd(self, message):
        message = await utils.answer(message, self.strings("loading_info"))
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        token = self.config["token"]
        user_id = token.split(":")[0]
        data = await _stats(user_id, token)
        datas = await _status(user_id, token)

        memory_stats = data["stats"]["memory_stats"]["usage"]
        memory = bytes_to_megabytes(memory_stats)
        cpu_stats_usage = data["stats"]["cpu_stats"]["cpu_usage"]["total_usage"]
        system_cpu_usage = data["stats"]["cpu_stats"]["system_cpu_usage"]

        host = await _host(user_id, token)
        server_id = host["host"]["server_id"]
        target_data = datetime.fromisoformat(
            host["host"]["end_date"].replace("Z", "+00:00")
        ).replace(tzinfo=timezone.utc)
        current_data = datetime.now(timezone.utc)
        days_end = (target_data - current_data).days
        end_dates = (current_data + timedelta(days=days_end)).strftime("%d-%m-%Y")

        if cpu_stats_usage and system_cpu_usage:
            cpu_percent = round((cpu_stats_usage / system_cpu_usage) * 100.0, 2)

        ram_percent = round(bytes_to_megabytes(memory_stats / self.MAX_RAM) * 100, 2)

        if "status" in datas and datas["status"] == "running":
            status = self.strings("condition")

        await utils.answer(
            message,
            self.strings("info").format(
                server_id=server_id,
                id=user_id,
                status=status,
                end_dates=end_dates,
                days_end=days_end,
                cpu_percent=cpu_percent,
                memory=memory,
                max_ram=self.MAX_RAM,
                ram_percent=ram_percent,
            ),
        )

    @loader.command(
        ru_doc="Логи HikkaHost",
        en_doc="Logs HikkaHost",
    )
    async def hlogscmd(self, message):
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        token = self.config["token"]
        user_id = token.split(":")[0]
        data = await _logs(user_id, token)

        files_log = data["logs"]

        with open("log.txt", "w") as log_file:
            json.dump(files_log, log_file)

        await utils.answer_file(message, "log.txt", self.strings("logs"))

    @loader.command(
        ru_doc="Рестарт HikkaHost",
        en_doc="Restart HikkaHost",
    )
    async def hrestartcmd(self, message):
        await utils.answer(message, self.strings("restart"))

        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        token = self.config["token"]
        user_id = token.split(":")[0]

        await _action(user_id, token)
